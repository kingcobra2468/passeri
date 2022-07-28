from functools import partial
import pathlib

from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from ytmp3.converter import Converter


class TransitPool:
    """TransitPool manages workers that asynchronously perform ytmp3 to
    email sendoff.
    """

    def __init__(self, email_client, download_path):
        """Constructor.

        Args:
            email_client (transit.email.client.EmailClient): The Email client.
            download_path (str): The path where mp3s will temporary be downloaded to. 
        """
        self._email_client = email_client
        self._request_queue = Queue()
        self._executor = ThreadPoolExecutor(max_workers=2)
        self._download_path = download_path

    def push(self, request):
        """Pushes a new YTMP3 to email request. Requests are executed asynchronously.

        Args:
            request (ytmp3.request.ConversionRequest): The meta of a given request.
        """
        future = self._executor.submit(
            TransitPool.worker, request, self._download_path
        )
        future.add_done_callback(
            partial(self.download_callback, request.recipient))

    def download_callback(self, recipient, future):
        """Awaits the file future. Sends the files once the future completes. 

        Args:
            recipient (str): The email of the recipient.
            future (Future): The future which holds the path mp3 file paths.
        """
        files = future.result()
        self._email_client.send_files(recipient, *files)

        for file in files:
            pathlib.Path(file).unlink()

    @staticmethod
    def worker(request, download_path):
        """Downloads all links in the request as mp3s to the designated download
        path.

        Args:
            request (ytmp3.request.ConversionRequest): The meta of a given request.
            download_path (str): The path where mp3s will temporary be downloaded to.

        Returns:
            List(str): A list of paths to the output mp3s. 
        """
        converter = Converter(request.links, download_path)
        return converter.download()
