from abc import ABC, abstractmethod
from typing import Dict


class Persister(ABC):
    @abstractmethod
    def save(self, data: Dict[str, str]):
        """Saves the key-value store."""
        pass

    @abstractmethod
    def load(self) -> Dict[str, str]:
        """Loads the key-value store."""
        pass
