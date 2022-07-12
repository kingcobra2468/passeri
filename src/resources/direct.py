from pathlib import Path

from falcon import HTTPBadRequest

from ytmp3.converter import Converter


class DirectDownloadResource:
    """DirectDownloadResource handles the resource that downloads a given Youtube
    video and downloads it to the recipient's device.
    """

    def __init__(self, download_path):
        self.download_path = download_path

    def on_get(self, req, resp):
        if 'link' not in req.params:
            raise HTTPBadRequest('The "link" query param was not provided.')

        link = req.params['link']
        converter = Converter([link], self.download_path)
        file = converter.download()[0]

        resp.downloadable_as = Path(file).name
        resp.stream = open(file, 'rb')
