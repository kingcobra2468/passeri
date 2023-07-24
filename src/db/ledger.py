from pymongo import MongoClient
import time
from db.mp3 import Mp3


class Mp3RequestLedger:
    def __init__(self, mongodb_host, mongodb_port=27017):
        self._client = MongoClient(
            host=mongodb_host, port=mongodb_port, uuidRepresentation='standard')
        self._db = self._client['passeri']
        self._mp3_col = self._db['mp3s']
        #self._mp3_col.delete_many({})
    def insert(self, link, recipient=None):
        song = Mp3(link=link, recipient=recipient)
        self._mp3_col.insert_one(song.model_dump())

    def get_all(self, query):
        requests = list(self._mp3_col.find(query, projection={'_id': False}))

        for request in requests:
            request['inserted_at'] = request['inserted_at'].isoformat()

        return requests

"""
from datetime import datetime, timedelta
import pytz

local_datetime = datetime.utcnow() - timedelta(minutes=11)

# Convert the local datetime to UTC
#timezone = pytz.timezone('US/Pacific')  # Replace 'Your_Local_Timezone' with your actual local timezone
#local_datetime = timezone.localize(local_datetime)
#utc_datetime = local_datetime.astimezone(pytz.utc)

print(local_datetime)

x = Mp3RequestLedger('10.0.1.10')
y = Mp3(url='a', recipient='b')
x.insert(url='a', recipient='b')
r = x.get_all({
    "recipient": "b",
    "inserted_at": {"$gt": local_datetime}
})

print(r)
"""

x = Mp3RequestLedger('10.0.1.10')
print(x.get_all({}))