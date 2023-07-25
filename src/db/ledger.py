from pymongo import MongoClient

from db.mp3 import Mp3


class Mp3RequestLedger:
    """Ledger for storing request meta. 
    """
    def __init__(self, mongodb_host, mongodb_port=27017):
        """Constructor.

        Args:
            mongodb_host (str): The MongoDB host.
            mongodb_port (int, optional): The MongoDB port. Defaults to 27017.
        """
        self._client = MongoClient(
            host=mongodb_host, port=mongodb_port, uuidRepresentation='standard')
        self._db = self._client['passeri']
        self._mp3_col = self._db['mp3s']

    def clean(self):
        """Removes all records from the ledger.
        """
        self._mp3_col.delete_many({})

    def insert(self, link, recipient=None):
        """Inserts a new record into the ledger.

        Args:
            link (str): The input Youtube link.
            recipient (str, optional): The email recipient of the link. Defaults to None.
        """
        song = Mp3(link=link, recipient=recipient)
        self._mp3_col.insert_one(song.model_dump())

    def get_all(self, query={}):
        """Gets all records from the input query.

        Args:
            query (dict, optional): The input MongoDB query. Defaults to {}.

        Returns:
            List: The list of request records.
        """
        requests = list(self._mp3_col.find(query, projection={'_id': False}))

        for request in requests:
            request['inserted_at'] = request['inserted_at'].isoformat()[:-3]+'Z'

        return requests
