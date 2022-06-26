from functools import partial

from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from ytmp3.converter import Converter


class TransitPool:
    def __init__(self, gmail_client, download_path):
        self._gmail_client = gmail_client
        self._request_queue = Queue()
        self._executor = ThreadPoolExecutor(max_workers=2)
        self._download_path = download_path

    def push(self, request):
        future = self._executor.submit(
            TransitPool.worker, request, self._download_path
        )
        future.add_done_callback(
            partial(self.download_callback, request.recipient))

    def download_callback(self, recipient, future):
        files = future.result()
        self._gmail_client.send_files(recipient, *files)

    @staticmethod
    def worker(request, download_path):
        converter = Converter(request.links, download_path)
        return converter.download()
