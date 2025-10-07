# KV-Store

- CLI
- TCP server interface

```py
class Prompt:
    def __init__(self):
        self.loop = asyncio.get_running_loop()
        self.q = asyncio.Queue()
        self.loop.add_reader(sys.stdin, self.got_input)

    def got_input(self):
        asyncio.ensure_future(self.q.put(sys.stdin.readline()), loop=self.loop)

    async def __call__(self, msg, end='\n', flush=False):
        print(msg, end=end, flush=flush)
        # https://docs.python.org/3/library/asyncio-task.html#coroutine
        task = asyncio.create_task(self.q.get())
        return (await task).rstrip('\n')
```
