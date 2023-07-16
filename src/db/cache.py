from threading import Lock
import pathlib

from cachetools import LRUCache


class FileCache(LRUCache):
    """FileCache caches files via a LRU cache. Popped
    files are deleted from the system.

    Args:
        LRUCache (_type_): _description_
    """

    def __init__(self, maxsize, getsizeof=None):
        super().__init__(maxsize, getsizeof)
        self._lock = Lock()

    def popitem(self):
        key, value = super().popitem()
        print(f'popping {key}, {value}')
        pathlib.Path(value).unlink()

        return key, value

    def lock(self):
        return self._lock.acquire()

    def unlock(self):
        return self._lock.release()

    def is_locked(self):
        return self._lock.locked()
