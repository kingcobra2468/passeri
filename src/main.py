from os import getenv
import logging
import sys

from wsgiref.simple_server import make_server
from dotenv import load_dotenv
import falcon

from db.cache import FileCache
from resources.songs import SongDownloadResource
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
    song_download_path = getenv('PASSERI_DOWNLOAD_PATH')
    passeri_port = int(getenv('PASSERI_PORT'))
    cache_size = int(getenv('PASSERI_FILE_CACHE_SIZE', 1000))

    file_cache = FileCache(100000)

    email_client = MailClient(email_address, email_password)
    email_download_queue = EmailDownloaderQueue(
        email_client, song_download_path, file_cache)

    song_download_resource = SongDownloadResource(
        song_download_path, email_download_queue, file_cache)

    app = falcon.App(cors_enable=True)
    app.add_route('/songs/download', song_download_resource)
    app.set_error_serializer(error_serializer)

    with make_server('0.0.0.0', passeri_port, app) as httpd:
        logging.info(f'Serving on port {passeri_port}...')

        httpd.serve_forever()
