import asyncio
import sys
from src.kv_store.kv_store import KVStore


class KVStoreCLI:
    def __init__(self, kv_store: KVStore):
        self.kv_store = kv_store

    def execute_command(self, cmd: str):
        try:
            if cmd.startswith("set"):
                _, key, value = cmd.split()
                self.kv_store.set(key, value)
                print(f'{key}="{value}"')
            elif cmd.startswith("update"):
                _, key, value = cmd.split()
                if self.kv_store.update(key, value):
                    print(f"{key}={value}")
                else:
                    print(f"{key} not found")
            elif cmd.startswith("get"):
                _, key = cmd.split()
                value = self.kv_store.get(key)
                if value is not None:
                    print(f"{key}={value}")
                else:
                    print(f"{key} not found")
            elif cmd.startswith("delete"):
                _, key = cmd.split()
                if self.kv_store.delete(key):
                    print(f"{key} deleted")
                else:
                    print(f"{key} not found")
            elif cmd.startswith("list"):
                if len(self.kv_store.list()) == 0:
                    print("empty")
                for key, value in self.kv_store.list():
                    print(f"{key}={value}")
            else:
                print(
                    "Unknown command. Please use 'set', 'update', 'get', 'delete', 'list'."
                )
        except ValueError:
            print(
                "Invalid command format. Please use: set <key> <value>, update <key> <value>, get <key>, delete <key>, list."
            )

    async def run(self):
        try:
            print("Enter command (set/update/get/delete/list) or press Ctrl+C to quit:")
            loop = asyncio.get_running_loop()
            rstream = asyncio.StreamReader(limit=8192, loop=loop)
            protocol = asyncio.StreamReaderProtocol(rstream, loop=loop)
            await loop.connect_read_pipe(lambda: protocol, sys.stdin)
            while True:
                print("> ", end="", flush=True)
                line = (await rstream.readline()).decode()
                cmd = line.strip()
                self.execute_command(cmd)
        except asyncio.CancelledError:
            return
