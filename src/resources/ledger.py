from datetime import datetime

from falcon import HTTPBadRequest
import pytz


class Mp3LedgerResource:
    """A resource for retrieving request records.
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
        """Parses the input time as UTC format.

        Args:
            input_time (str): The input time.

        Raises:
            HTTPBadRequest: Raised if the time is not UTC compliant.

        Returns:
            datetime: The UTC time.
        """
        try:
            datetime_obj = datetime.strptime(
                input_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            raise HTTPBadRequest('Date is not in UTC format')

        utc_timezone = pytz.timezone('UTC')
        return utc_timezone.localize(datetime_obj)
