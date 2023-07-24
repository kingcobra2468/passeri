from pathlib import Path
import datetime

from falcon.media.validators import jsonschema
from falcon import HTTPBadRequest
from tzlocal import get_localzone
import pytz

from schemas import load_schema
from youtube.downloader import YoutubeDownloader
from mail.request import MailQueueRequest


class Mp3LedgerResource:
    """DirectDownloadResource handles the resource that downloads a given Youtube
    video and downloads it to the recipient's device.
    """

    def __init__(self, ledger=None):
        self._ledger = ledger

    def on_get(self, req, resp):
        recipient = req.get_param('recipient')
        since = req.get_param('since')
        query = {}

        if since:
            query['inserted_at'] = {
                "$gt": self.__parse_time_as_local_utc(since)}
        if recipient:
            query['recipient'] = recipient

        resp.media = self._ledger.get_all(query)

    def __parse_time_as_local_utc(self, input_time):
        try:
            datetime_obj = datetime.strptime(
                input_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            raise HTTPBadRequest('Date is not in UTC format')

        utc_timezone = pytz.timezone('UTC')
        return utc_timezone.localize(datetime_obj)
