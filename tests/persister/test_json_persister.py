from src.persister.json_persister import JSONPersister
from unittest.mock import patch, mock_open, MagicMock
from typing import List, Tuple
import json
import pytest

FILENAME = "store.json"


@pytest.fixture
def persister():
    return JSONPersister(FILENAME)


test_data = {"key1": "value1", "key2": "value2"}


def test_json_persister_load(persister: JSONPersister):
    mock_file: MagicMock = mock_open(read_data=json.dumps(test_data))
    with patch("builtins.open", mock_file), patch("os.path.exists", return_value=True):
        kv_store_data = persister.load()
        print(kv_store_data)
        assert kv_store_data["key1"] == "value1"
        assert kv_store_data["key2"] == "value2"


def test_json_persister_save(persister: JSONPersister):
    mock_file: MagicMock = mock_open()
    with patch("builtins.open", mock_file):
        persister.save(test_data)
    mock_file.assert_called_once_with(FILENAME, "w")
    write_calls: List[Tuple[str]] = mock_file().write.call_args_list
    written_content = "".join(call[0][0] for call in write_calls)
    assert written_content == json.dumps(test_data)
