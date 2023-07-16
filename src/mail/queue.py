from functools import partial
import pathlib

from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from youtube.downloader import YoutubeDownloader


class EmailDownloaderQueue:
    """EmailDownloaderQueue manages workers that asynchronously perform ytmp3 to
    email sendoff.
    """

    def __init__(self, mail_client, download_path, cache=None):
        """Constructor.

        Args:
            mail_client (mail.client.MailClient): The Email client.
            download_path (str): The path where mp3s will temporary be downloaded.
            cache (db.cache.FileCache): The file cache.
        """
        self._mail_client = mail_client
        self._request_queue = Queue()
        self._executor = ThreadPoolExecutor(max_workers=2)
        self._download_path = download_path
        self._cache = cache

    def push(self, request):
        """Pushes a new Youtube to mp3 email request. Requests are executed asynchronously.

        Args:
            request (mail.request.MailQueueRequest): The meta of a given request.
        """
        future = self._executor.submit(
            EmailDownloaderQueue.worker, request, self._download_path, self._cache
        )
        future.add_done_callback(
            partial(self.download_callback, request.recipient))

    def download_callback(self, recipient, future):
        """Awaits the file future. Sends the files once the future completes. 

        Args:
            recipient (str): The email of the recipient.
            future (Future): The future which holds the path mp3 file paths.
        """
        youtube_downloader = future.result()
        files = youtube_downloader.get_files()
        self._mail_client.send_files(recipient, *files)

        if not self._cache is not None:
            youtube_downloader.clean()

    @staticmethod
    def worker(request, download_path, cache):
        """Downloads all links in the request as mp3s to the designated download
        path.

        Args:
            request (mail.request.MailQueueRequest): The meta of a given request.
            download_path (str): The path where mp3s will temporary be downloaded to.

        Returns:
            List(str): A list of paths to the output mp3s. 
        """
        youtube_downloader = YoutubeDownloader(
            request.links, download_path, cache)
        youtube_downloader.download()

        return youtube_downloader
