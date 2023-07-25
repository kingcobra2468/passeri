from os import getenv
import logging
import sys

from wsgiref.simple_server import make_server
from dotenv import load_dotenv
import falcon

from db.cache import FileCache
from db.ledger import Mp3RequestLedger
from resources.download import Mp3DownloadResource
from resources.ledger import Mp3LedgerResource
from mail.queue import EmailDownloaderQueue
from mail.client import MailClient

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
load_dotenv(override=True)


def error_serializer(req, resp, exception):
    """Serializes a given error to follow the conventions defined
    here https://github.com/omniti-labs/jsend .
    """
    resp.content_type = falcon.MEDIA_JSON
    resp.media = {'status': 'error', 'data': exception.to_dict()}


if __name__ == '__main__':
    email_address = getenv('PASSERI_EMAIL_ADDRESS')
    email_password = getenv('PASSERI_EMAIL_PASSWORD')
    mp3_download_path = getenv('PASSERI_DOWNLOAD_PATH')
    passeri_port = int(getenv('PASSERI_PORT'))
    is_request_logging_enabled = getenv(
        'PASSERI_REQUEST_LOGGING_ENABLED', False).lower() in ('true', '1', 't')

    cache_size = int(getenv('PASSERI_FILE_CACHE_SIZE', 1000))

    file_cache = FileCache(100000)
    request_ledger = None

    if is_request_logging_enabled:
        mongo_db_host = getenv('PASSERI_MONGO_DB_HOST')
        mongo_db_port = int(getenv('PASSERI_MONGO_DB_PORT'))
        request_ledger = Mp3RequestLedger(mongo_db_host, mongo_db_port)

    email_client = MailClient(email_address, email_password)
    email_download_queue = EmailDownloaderQueue(
        email_client, mp3_download_path, file_cache)

    mp3_download_resource = Mp3DownloadResource(
        mp3_download_path, email_download_queue, file_cache, request_ledger)
    mp3_ledger_resource = Mp3LedgerResource(request_ledger)

    app = falcon.App(cors_enable=True)
    app.add_route('/mp3s/download', mp3_download_resource)

    if is_request_logging_enabled:
        app.add_route('/mp3s', mp3_ledger_resource)

    app.set_error_serializer(error_serializer)

    with make_server('0.0.0.0', passeri_port, app) as httpd:
        logging.info(f'Serving on port {passeri_port}...')
        httpd.serve_forever()
