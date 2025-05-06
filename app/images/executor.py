from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Callable, Any
import asyncio


class AsyncExecutor:
    def __init__(self, max_workers: int = 6, use_process: bool = False):
        self.executor = (ProcessPoolExecutor if use_process else ThreadPoolExecutor)(
            max_workers=max_workers
        )

    async def run(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, lambda: func(*args, **kwargs))

    def shutdown(self, wait: bool = True) -> None:
        self.executor.shutdown(wait=wait)
