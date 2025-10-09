import logging
from src.config import STORAGE_PATH, CLI_ENABLED
import src.logger  # type: ignore
import asyncio
import contextlib
from aiohttp import web

from src.control_interface.cli import KVStoreCLI
from src.control_interface.http import kv_store
from src.kv_store.basic_kv_store import BasicKVStore
from src.control_interface.http import app
from src.persister.persister_factory import persister_factory

logger = logging.getLogger("main")


async def background_tasks(app: web.Application):
    cli = KVStoreCLI(app[kv_store])
    cli_task = asyncio.create_task(cli.run())
    yield
    cli_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await cli_task


if __name__ == "__main__":
    logger.info("Starting the key-value store...")
    persister = persister_factory(STORAGE_PATH)
    app[kv_store] = BasicKVStore(persister)
    if CLI_ENABLED:
        app.cleanup_ctx.append(background_tasks)
    web.run_app(app, print=None, port=8080)
    logger.info("Graceful shutdown completed.")
