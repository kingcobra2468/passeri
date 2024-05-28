from falcon import HTTPBadRequest

from youtube.downloader import YoutubeDownloader


class Mp3InfoResource:
    """A resource for mp3 info.
    """

    def on_get(self, req, resp):
        if 'link' not in req.params:
            raise HTTPBadRequest('The "link" query param was not provided.')

        req.context.link = req.params['link']
        file_name = YoutubeDownloader.get_file_name(req.context.link)

        resp.media = {
            'status': 'success',
            'data': {
                'filename': file_name
            }
        }