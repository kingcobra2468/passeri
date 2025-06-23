from functools import partial
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from youtube.downloader import YoutubeDownloader


class EmailDownloaderQueue:
    """Queue that distributes Youtube to mp3 email requests
    across multiple workers.
    """

    def __init__(self, mail_client, download_path, _cookies_file_path=None, cache=None):
        """Constructor.

        Args:
            mail_client (mail.client.MailClient): The email client.
            download_path (str): The mp3 download path.
            cache (db.cache.FileCache): The file cache.
        """
        self._mail_client = mail_client
        self._request_queue = Queue()
        self._executor = ThreadPoolExecutor(max_workers=2)
        self._download_path = download_path
        self._cookies_file_path = _cookies_file_path
        self._cache = cache

    def push(self, request):
        """Pushes a new Youtube to mp3 email request. Requests are
        executed asynchronously.

        Args:
            request (mail.request.MailQueueRequest): The request meta.
        """
        future = self._executor.submit(
            EmailDownloaderQueue.worker, request, self._download_path, self._cookies_file_path, self._cache
        )
        future.add_done_callback(
            partial(self.download_callback, request.recipient))

    def download_callback(self, recipient, future):
        """Callback that sends the files to the recipient once
        the mp3s are downloaded. 

        Args:
            recipient (str): The recipient email.
            future (Future): The future which holds the mp3 file paths.
        """
        youtube_downloader = future.result()
        files = youtube_downloader.get_files()
        self._mail_client.send_files(recipient, *files)

        if not self._cache is not None:
            youtube_downloader.clean()

    @staticmethod
    def worker(request, download_path, cookies_file_path, cache):
        """Worker that downloads the requested links as mp3s to the download
        path.

        Args:
            request (mail.request.MailQueueRequest): The request meta.
            download_path (str): The mp3 download path.

        Returns:
            List(str): A list of the downloaded mp3s. 
        """
        youtube_downloader = YoutubeDownloader(
            request.links, download_path, cookies_file_path, cache)
        youtube_downloader.download()

        return youtube_downloader
