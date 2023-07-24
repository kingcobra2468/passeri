from pathlib import Path

from falcon.media.validators import jsonschema
from falcon import HTTPBadRequest

from schemas import load_schema
from youtube.downloader import YoutubeDownloader
from mail.request import MailQueueRequest


class Mp3DownloadResource:
    """DirectDownloadResource handles the resource that downloads a given Youtube
    video and downloads it to the recipient's device.
    """

    def __init__(self, download_path, email_download_queue, cache=None, request_ledger=None):
        self._download_path = download_path
        self._email_download_queue = email_download_queue
        self._cache = cache
        self._request_ledger = request_ledger

    def on_get(self, req, resp):
        if 'link' not in req.params:
            raise HTTPBadRequest('The "link" query param was not provided.')

        req.context.links = [req.params['link']]
        # add caching logic here or inside of Converter
        youtube_downloader = YoutubeDownloader(
            req.context.links, self._download_path, self._cache)
        file = youtube_downloader.download()[0]

        resp.downloadable_as = Path(file).name
        resp.stream = open(file, 'rb')

        if self._request_ledger:
            self.__log_request(req.context.links)

    @jsonschema.validate(load_schema('mp3s_to_email'))
    def on_post(self, req, resp):
        data = req.get_media()
        req.context.links = data['links']
        req.context.recipient_email = data['recipient_email']

        request = MailQueueRequest(
            req.context.recipient_email, req.context.links)
        self._email_download_queue.push(request)

        resp.media = {'status': 'success'}

        if self._request_ledger:
            self.__log_request(req.context.links, req.context.recipient_email)

    def __log_request(self, links, recipient=None):
        for link in links:
            self._request_ledger.insert(link, recipient)
