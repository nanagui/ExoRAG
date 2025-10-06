"""Background workers for ingestion and maintenance tasks."""

from __future__ import annotations

import asyncio
import logging
from contextlib import suppress

from .dependencies import ensure_corpus_indexed

LOGGER = logging.getLogger(__name__)


class IngestionQueue:
    """Simple asynchronous queue for ingestion jobs."""

    def __init__(self) -> None:
        self._queue: asyncio.Queue = asyncio.Queue()
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._worker())

    async def stop(self) -> None:
        if self._task is None:
            return
        self._task.cancel()
        with suppress(asyncio.CancelledError):
            await self._task
        self._task = None

    async def enqueue(self, func, *args, **kwargs) -> None:
        await self._queue.put((func, args, kwargs))

    async def _worker(self) -> None:
        while True:
            func, args, kwargs = await self._queue.get()
            try:
                result = func(*args, **kwargs)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as exc:  # pragma: no cover
                LOGGER.exception("Ingestion task failed", exc_info=exc)
            finally:
                self._queue.task_done()


class BackgroundScheduler:
    """Simple asyncio-based scheduler for periodic tasks."""

    def __init__(self, embedding_refresh_interval: int = 3600) -> None:
        self.embedding_refresh_interval = embedding_refresh_interval
        self._tasks: list[asyncio.Task] = []
        self.ingestion_queue = IngestionQueue()

    async def start(self) -> None:
        await self.ingestion_queue.start()
        self._tasks.append(asyncio.create_task(self._run_embedding_refresh()))

    async def stop(self) -> None:
        await self.ingestion_queue.stop()
        for task in self._tasks:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
        self._tasks.clear()

    async def _run_embedding_refresh(self) -> None:
        while True:
            try:
                ensure_corpus_indexed()
            except Exception as exc:  # pragma: no cover
                LOGGER.exception("Failed to refresh embeddings", exc_info=exc)
            await asyncio.sleep(self.embedding_refresh_interval)


SCHEDULER = BackgroundScheduler()


__all__ = ["BackgroundScheduler", "SCHEDULER", "IngestionQueue"]
