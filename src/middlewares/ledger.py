class RequestLedgerMiddleware:
    """Middleware to log user download requests.
    """

    def __init__(self, request_ledger):
        self._request_ledger = request_ledger

    def process_response(self, req, resp, resource, req_succeeded):
        if not req_succeeded:
            return

        if not self._request_ledger:
            return

        if 'links' not in req.context:
            return

        self.__log_request(req.context.links,
                           req.context.get('recipient_email', None))

    def __log_request(self, links, recipient):
        """Logs a request to the ledger.

        Args:
            links (List(str)): The links to download.
            recipient (str, optional): The email recipient of the link.
        """
        for link in links:
            self._request_ledger.insert(link, recipient)
