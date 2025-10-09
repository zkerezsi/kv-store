from pytest import CaptureFixture
import pytest
from unittest.mock import MagicMock

from src.control_interface.cli import KVStoreCLI


@pytest.fixture
def mock_kv_store():
    kv_store = MagicMock()
    return kv_store


@pytest.fixture
def cli(mock_kv_store: MagicMock):
    return KVStoreCLI(mock_kv_store)


def test_set_command(
    cli: KVStoreCLI, mock_kv_store: MagicMock, capsys: CaptureFixture[str]
):
    cli.execute_command("set myKey myValue")

    mock_kv_store.set.assert_called_once_with("myKey", "myValue")

    captured = capsys.readouterr()
    assert captured.out.strip() == "myKey=myValue"


def test_update_command_success(
    cli: KVStoreCLI, mock_kv_store: MagicMock, capsys: CaptureFixture[str]
):
    mock_kv_store.update.return_value = True
    cli.execute_command("update myKey myNewValue")

    mock_kv_store.update.assert_called_once_with("myKey", "myNewValue")
    captured = capsys.readouterr()
    assert captured.out.strip() == "myKey=myNewValue"


def test_update_command_not_found(
    cli: KVStoreCLI, mock_kv_store: MagicMock, capsys: CaptureFixture[str]
):
    mock_kv_store.update.return_value = False
    cli.execute_command("update myKey myNewValue")

    captured = capsys.readouterr()
    assert captured.out.strip() == "myKey not found"


def test_get_command_found(
    cli: KVStoreCLI, mock_kv_store: MagicMock, capsys: CaptureFixture[str]
):
    mock_kv_store.get.return_value = "myValue"
    cli.execute_command("get myKey")

    mock_kv_store.get.assert_called_once_with("myKey")
    captured = capsys.readouterr()
    assert captured.out.strip() == "myKey=myValue"


def test_get_command_not_found(
    cli: KVStoreCLI, mock_kv_store: MagicMock, capsys: CaptureFixture[str]
):
    mock_kv_store.get.return_value = None
    cli.execute_command("get myKey")

    mock_kv_store.get.assert_called_once_with("myKey")
    captured = capsys.readouterr()
    assert captured.out.strip() == "myKey not found"


def test_delete_command_success(
    cli: KVStoreCLI, mock_kv_store: MagicMock, capsys: CaptureFixture[str]
):
    mock_kv_store.delete.return_value = True
    cli.execute_command("delete myKey")

    mock_kv_store.delete.assert_called_once_with("myKey")
    captured = capsys.readouterr()
    assert captured.out.strip() == "myKey deleted"


def test_delete_command_not_found(
    cli: KVStoreCLI, mock_kv_store: MagicMock, capsys: CaptureFixture[str]
):
    mock_kv_store.delete.return_value = False
    cli.execute_command("delete myKey")

    mock_kv_store.delete.assert_called_once_with("myKey")
    captured = capsys.readouterr()
    assert captured.out.strip() == "myKey not found"


def test_list_command(
    cli: KVStoreCLI, mock_kv_store: MagicMock, capsys: CaptureFixture[str]
):
    mock_kv_store.list.return_value = [("key1", "value1"), ("key2", "value2")]
    cli.execute_command("list")

    mock_kv_store.list.assert_called_once()
    captured = capsys.readouterr()
    assert captured.out.strip() == "key1=value1\nkey2=value2"


def test_unknown_command(cli: KVStoreCLI, capsys: CaptureFixture[str]):
    cli.execute_command("unknown")
    captured = capsys.readouterr()
    assert (
        captured.out.strip()
        == "Unknown command. Please use 'set', 'update', 'get', 'delete', 'list'."
    )


def test_invalid_command_format(cli: KVStoreCLI, capsys: CaptureFixture[str]):
    cli.execute_command("set myKey")
    captured = capsys.readouterr()
    assert (
        captured.out.strip()
        == "Invalid command format. Please use: set <key> <value>, update <key> <value>, get <key>, delete <key>, list."
    )
