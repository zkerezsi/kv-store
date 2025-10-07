from typing import List, Optional, Tuple
from abc import ABC, abstractmethod


class KVStore(ABC):
    @abstractmethod
    def set(self, key: str, value: str):
        """Stores the provided value under the provided key."""
        pass

    @abstractmethod
    def update(self, key: str, value: str) -> bool:
        """Updates the value stored under a given key if some value is stored under provided key already.
        Returns true when the update was successful."""
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        """Retrieves the value stored under the provided key if it exists."""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Removes the elements stored with the provided key, returns true if it
        existed and false if not."""
        pass

    @abstractmethod
    def list(self) -> List[Tuple[str, str]]:
        """List all keys and values stored."""
        pass
