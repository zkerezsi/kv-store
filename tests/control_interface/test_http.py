import pytest
from pytest_aiohttp import AiohttpClient
from aiohttp import web
from aiohttp.test_utils import TestClient
from src.control_interface.http import routes
from tests.mock.mock_kv_store import MockKVStore
from src.control_interface.http import kv_store


@pytest.fixture
async def client(aiohttp_client: AiohttpClient):
    app = web.Application()
    app.add_routes(routes)
    initial_data = {"key1": "value1", "key2": "value2"}
    app[kv_store] = MockKVStore(initial_data)
    return await aiohttp_client(app)


async def test_set_valid(client: TestClient[web.Request, web.Application]):
    resp = await client.put("/key1?value=hello%20world")
    assert resp.status == 200
    assert await resp.text() == "key1=hello%20world"


async def test_set_missing_value(client: TestClient[web.Request, web.Application]):
    resp = await client.put("/test_key")
    assert resp.status == 400
    assert await resp.text() == "value not provided in request"


async def test_update_existing_key(client: TestClient[web.Request, web.Application]):
    resp = await client.post("/key1?value=new_value")
    assert resp.status == 200
    assert await resp.text() == "key1=new_value"


async def test_update_missing_value(client: TestClient[web.Request, web.Application]):
    resp = await client.post("/test_key")
    assert resp.status == 400
    assert await resp.text() == "value not provided in request"


async def test_update_nonexistent_key(client: TestClient[web.Request, web.Application]):
    resp = await client.post("/nonexistent_key?value=value")
    assert resp.status == 404
    assert await resp.text() == "nonexistent_key not found"


async def test_get_existing_key(client: TestClient[web.Request, web.Application]):
    resp = await client.get("/key1")
    assert resp.status == 200
    assert await resp.text() == "value1"


async def test_get_nonexistent_key(client: TestClient[web.Request, web.Application]):
    resp = await client.get("/nonexistent_key")
    assert resp.status == 404
    assert await resp.text() == "nonexistent_key not found"


async def test_delete_existing_key(client: TestClient[web.Request, web.Application]):
    resp = await client.delete("/key1")
    assert resp.status == 200
    assert await resp.text() == "key1 deleted"


async def test_delete_nonexistent_key(client: TestClient[web.Request, web.Application]):
    resp = await client.delete("/nonexistent_key")
    assert resp.status == 404
    assert await resp.text() == "nonexistent_key not found"


async def test_list_empty_store(client: TestClient[web.Request, web.Application]):
    await client.delete("/key1")
    await client.delete("/key2")
    resp = await client.get("/")
    assert resp.status == 200
    assert await resp.text() == ""


async def test_list_with_items(client: TestClient[web.Request, web.Application]):
    resp = await client.get("/")
    assert resp.status == 200
    assert await resp.text() == "key1=value1\nkey2=value2\n"
