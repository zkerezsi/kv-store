from typing import List, Tuple
from unittest.mock import MagicMock, mock_open, patch
import pytest
from src.persister.csv_persister import CSVPersister, dict_to_csv_str


FILENAME = "store.csv"


@pytest.fixture
def persister():
    return CSVPersister(FILENAME)


test_data = {"key1": "value1", "key2": "value2"}


def test_csv_persister_load(persister: CSVPersister):
    read_data = dict_to_csv_str(test_data)
    mock_file: MagicMock = mock_open(read_data=read_data)
    with patch("builtins.open", mock_file), patch("os.path.exists", return_value=True):
        kv_store_data = persister.load()
        assert kv_store_data["key1"] == "value1"
        assert kv_store_data["key2"] == "value2"


def test_csv_persister_save(persister: CSVPersister):
    mock_file: MagicMock = mock_open()
    with patch("builtins.open", mock_file):
        persister.save(test_data)
    mock_file.assert_called_once_with(FILENAME, "w")
    write_calls: List[Tuple[str]] = mock_file().write.call_args_list
    written_content = "".join(call[0][0] for call in write_calls)
    assert written_content == dict_to_csv_str(test_data)
