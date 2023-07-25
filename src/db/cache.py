from threading import Lock
import pathlib

from cachetools import LRUCache


class FileCache(LRUCache):
    """An LRU cache for files. Popped files are
    deleted from the system.
    """

    def __init__(self, maxsize):
        """Constructor.

        Args:
            maxsize (int): The maximum size of the cache
        """
        super().__init__(maxsize, None)
        self._lock = Lock()

    def popitem(self):
        """Pops and deletes an file from the cache.

        Returns:
            (str, str): The link, file path pair.
        """
        key, value = super().popitem()
        pathlib.Path(value).unlink()

        return key, value

    def lock(self):
        """Locks the underlying buffer such that an operation
        can be performed.

        Returns:
            bool: Whether the locking operation was successful.
        """
        return self._lock.acquire()

    def unlock(self):
        """Unlocks the underlying buffer such that an operation
        can be performed.

        Returns:
            bool: Whether the unlocking operation was successful.
        """
        return self._lock.release()

    def is_locked(self):
        """Gets the status of the underlying buffer lock.

        Returns:
            bool: Whether the mutex is locked.
        """
        return self._lock.locked()
