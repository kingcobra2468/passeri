from os import getenv
import logging
import sys

from wsgiref.simple_server import make_server
from dotenv import load_dotenv
import falcon

from resources.email import EmailResource
from resources.direct import DirectDownloadResource
from transit.pool import TransitPool
from transit.email.client import EmailClient

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
load_dotenv(override=True)


def error_serializer(req, resp, exception):
    """Serializes a given error to follow the conventions defined
    here https://github.com/omniti-labs/jsend .
    """
    resp.content_type = falcon.MEDIA_JSON

    resp.media = {'status': 'error', 'data': exception.to_dict()}


if __name__ == '__main__':
    email_client = EmailClient(
        getenv('PASSERI_EMAIL_ADDRESS'), getenv('PASSERI_EMAIL_PASSWORD'))
    transit_pool = TransitPool(email_client, getenv('PASSERI_DOWNLOAD_PATH'))

    email_resource = EmailResource(transit_pool)
    direct_download_resource = DirectDownloadResource(
        getenv('PASSERI_DOWNLOAD_PATH'))

    app = falcon.App(cors_enable=True)
    app.add_route('/ytmp3/email', email_resource)
    app.add_route('/ytmp3', direct_download_resource)
    app.set_error_serializer(error_serializer)

    port = int(getenv('PASSERI_PORT'))
    with make_server('0.0.0.0', port, app) as httpd:
        logging.info(f'Serving on port {port}...')

        httpd.serve_forever()
