from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from ytmp3.converter import Converter


class TransitPool:
    def __init__(self, gmail_client):
        self._gmail_client = gmail_client
        self._request_queue = Queue()
        self._executor = ThreadPoolExecutor(max_workers=2)

    def new_request(self, request):
        future_files = self._executor.submit(TransitPool.worker, request)
        files = future_files.result()
        self._gmail_client.send_files(request.recipient, *files)

    @staticmethod
    def worker(request):
        converter = Converter(request.links, "/home/erik")
        return converter.download()
