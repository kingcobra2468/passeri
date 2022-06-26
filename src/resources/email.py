from ytmp3.request import ConversionRequest


class EmailResource:
    def __init__(self, transit_pool):
        self._transit_pool = transit_pool

    def on_post(self, req, resp):
        data = req.get_media()
        request = ConversionRequest(data['recipient'], data['links'])
        self._transit_pool.push(request)

        resp.media = {'status': 'success'}
