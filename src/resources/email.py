from ytmp3.request import ConversionRequest

from falcon.media.validators import jsonschema

from schemas import load_schema


class EmailResource:
    def __init__(self, transit_pool):
        self._transit_pool = transit_pool

    @jsonschema.validate(load_schema('ytmp3_email'))
    def on_post(self, req, resp):
        data = req.get_media()
        request = ConversionRequest(data['recipient_email'], data['links'])
        self._transit_pool.push(request)

        resp.media = {'status': 'success'}
