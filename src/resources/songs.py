from pathlib import Path

from falcon.media.validators import jsonschema
from falcon import HTTPBadRequest

from schemas import load_schema
from youtube.downloader import YoutubeDownloader
from mail.request import MailQueueRequest


class SongDownloadResource:
    """DirectDownloadResource handles the resource that downloads a given Youtube
    video and downloads it to the recipient's device.
    """

    def __init__(self, download_path, email_download_queue):
        self.download_path = download_path
        self._email_download_queue = email_download_queue

    def on_get(self, req, resp):
        if 'link' not in req.params:
            raise HTTPBadRequest('The "link" query param was not provided.')

        link = req.params['link']
        # add caching logic here or inside of Converter
        youtube_downloader = YoutubeDownloader([link], self.download_path)
        file = youtube_downloader.download()[0]

        resp.downloadable_as = Path(file).name
        resp.stream = open(file, 'rb')

    @jsonschema.validate(load_schema('songs_to_email'))
    def on_post(self, req, resp):
        data = req.get_media()
        request = MailQueueRequest(data['recipient_email'], data['links'])
        self._email_download_queue.push(request)

        resp.media = {'status': 'success'}
