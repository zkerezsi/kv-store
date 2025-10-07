import asyncio
import contextlib
from src.control_interface.cli import KVStoreCLI
from src.control_interface.http import kv_store
from src.kv_store.basic_kv_store import BasicKVStore
from src.persister.json_persister import JSONPersister
from src.control_interface.http import app
import logging
import src.logger  # type: ignore
from aiohttp import web

logger = logging.getLogger("main")


async def background_tasks(app: web.Application):
    persister = JSONPersister("store.json")
    app[kv_store] = BasicKVStore(persister)
    cli = KVStoreCLI(app[kv_store])
    cli_task = asyncio.create_task(cli.run())
    yield
    cli_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await cli_task
        logger.info("Graceful shutdown completed.")


if __name__ == "__main__":
    logger.info("Starting the key-value store...")
    app.cleanup_ctx.append(background_tasks)
    web.run_app(app, print=None, port=8080)
