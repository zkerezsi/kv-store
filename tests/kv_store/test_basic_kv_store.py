import pytest

from src.kv_store.basic_kv_store import BasicKVStore
from tests.mock.mock_persister import MockPersister


@pytest.fixture
def kv_store():
    initial_data = {"key1": "value1", "key2": "value2"}
    persister = MockPersister(initial_data)
    return BasicKVStore(persister)


def test_set(kv_store: BasicKVStore):
    kv_store.set("key3", "value3")
    assert kv_store.get("key3") == "value3"


def test_update_existing_key(kv_store: BasicKVStore):
    assert kv_store.update("key1", "new_value1") is True
    assert kv_store.get("key1") == "new_value1"


def test_update_non_existing_key(kv_store: BasicKVStore):
    assert kv_store.update("key3", "value3") is False
    assert kv_store.get("key3") is None


def test_get_existing_key(kv_store: BasicKVStore):
    assert kv_store.get("key1") == "value1"


def test_get_non_existing_key(kv_store: BasicKVStore):
    assert kv_store.get("key3") is None


def test_delete_existing_key(kv_store: BasicKVStore):
    assert kv_store.delete("key1") is True
    assert kv_store.get("key1") is None


def test_delete_non_existing_key(kv_store: BasicKVStore):
    assert kv_store.delete("key3") is False


def test_list_after_deletion(kv_store: BasicKVStore):
    result = kv_store.list()
    expected_result = [("key1", "value1"), ("key2", "value2")]
    assert result == expected_result, "List should contain all stored items."
