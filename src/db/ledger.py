from pymongo import MongoClient

from db.mp3 import Mp3


class Mp3RequestLedger:
    def __init__(self, mongodb_host, mongodb_port=27017):
        self._client = MongoClient(
            host=mongodb_host, port=mongodb_port, uuidRepresentation='standard')
        self._db = self._client['passeri']
        self._mp3_col = self._db['mp3s']
        # self._mp3_col.delete_many({})

    def insert(self, link, recipient=None):
        song = Mp3(link=link, recipient=recipient)
        self._mp3_col.insert_one(song.model_dump())

    def get_all(self, query):
        requests = list(self._mp3_col.find(query, projection={'_id': False}))

        for request in requests:
            request['inserted_at'] = request['inserted_at'].isoformat()

        return requests
