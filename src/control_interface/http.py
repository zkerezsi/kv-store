from aiohttp import web

from src.kv_store.kv_store import KVStore

routes = web.RouteTableDef()


@routes.put("/{key}")
async def handleSet(request: web.Request):
    key = request.match_info.get("key", "")
    value = request.query.get("value")
    if value is None:
        return web.Response(status=400, text="value not provided in request")
    request.app[kv_store].set(key, value)
    return web.Response(text=f"{key}={value}")


@routes.post("/{key}")
async def handleUpdate(request: web.Request):
    key = request.match_info.get("key", "")
    value = request.query.get("value")
    if value is None:
        return web.Response(status=400, text="value not provided in request")
    updated = request.app[kv_store].update(key, value)
    if updated:
        return web.Response(text=f"{key}={value}")
    else:
        return web.Response(status=404, text=f"{key} not found")


@routes.get("/{key}")
async def handleGet(request: web.Request):
    key = request.match_info.get("key", "")
    value = request.app[kv_store].get(key)
    if value is None:
        return web.Response(status=404, text=f"{key} not found")
    return web.Response(text=value)


@routes.delete("/{key}")
async def handleDelete(request: web.Request):
    key = request.match_info.get("key", "")
    deleted = request.app[kv_store].delete(key)
    if deleted:
        return web.Response(status=200, text=f"{key} deleted")
    else:
        return web.Response(status=404, text=f"{key} not found")


@routes.get("/")
async def handleList(request: web.Request):
    result = request.app[kv_store].list()
    if len(result) == 0:
        return web.Response(text="empty")
    response = web.StreamResponse(status=200)
    response.headers["Content-Type"] = "text/plain"
    await response.prepare(request)
    for key, value in result:
        await response.write(f"{key}={value}\n".encode("utf-8"))
    await response.write_eof()
    return response


app = web.Application()
kv_store = web.AppKey("kv_store", KVStore)
app.add_routes(routes)
