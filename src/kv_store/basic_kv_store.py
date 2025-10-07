from typing import Dict, Optional, Tuple, List

from src.kv_store.kv_store import KVStore
from src.persister.persister import Persister


class BasicKVStore(KVStore):
    kv_store: Dict[str, str] = {}
    persister: Persister

    def __init__(self, persister: Persister):
        self.persister = persister
        self.kv_store = self.persister.load()

    # PUT /{key}
    def set(self, key: str, value: str):
        self.kv_store[key] = value
        self.persister.save(self.kv_store)

    # POST /{key}
    def update(self, key: str, value: str) -> bool:
        if key in self.kv_store:
            self.kv_store[key] = value
            self.persister.save(self.kv_store)
            return True
        return False

    # GET /{key}
    def get(self, key: str) -> Optional[str]:
        try:
            return self.kv_store[key]
        except KeyError:
            return None

    # DELETE /{key}
    def delete(self, key: str) -> bool:
        if key in self.kv_store:
            del self.kv_store[key]
            self.persister.save(self.kv_store)
            return True
        return False

    # GET /
    def list(self) -> List[Tuple[str, str]]:
        return [(key, value) for key, value in self.kv_store.items()]
