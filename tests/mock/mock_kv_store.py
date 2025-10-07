from typing import Dict, List, Optional, Tuple

from src.kv_store.kv_store import KVStore


class MockKVStore(KVStore):
    def __init__(self, initial_data: Dict[str, str] | None):
        self.kv_store: Dict[str, str] = initial_data or {}

    def set(self, key: str, value: str):
        self.kv_store[key] = value

    def update(self, key: str, value: str) -> bool:
        if key in self.kv_store:
            self.kv_store[key] = value
            return True
        return False

    def get(self, key: str) -> Optional[str]:
        return self.kv_store.get(key)

    def delete(self, key: str) -> bool:
        if key in self.kv_store:
            del self.kv_store[key]
            return True
        return False

    def list(self) -> List[Tuple[str, str]]:
        return [(key, value) for key, value in self.kv_store.items()]
