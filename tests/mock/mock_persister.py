from typing import Dict, Optional

from src.persister.persister import Persister


class MockPersister(Persister):
    def __init__(self, initial_data: Optional[Dict[str, str]] = None):
        self.data = initial_data or {}

    def save(self, data: Dict[str, str]):
        self.data = data

    def load(self) -> Dict[str, str]:
        return self.data
