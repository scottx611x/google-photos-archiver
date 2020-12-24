import concurrent
import logging
from concurrent.futures._base import Future
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Iterable, Iterator

from src.archivers import Archivable
from src.media_item import MediaItem

logger = logging.getLogger(__name__)


class MediaItemArchiver:
    def __init__(
        self,
        media_items: Iterable[MediaItem],
        archiver: Archivable,
        max_threadpool_workers: int = 25,
    ):
        self.media_items = media_items
        self.archiver = archiver
        self.max_threadpool_workers = max_threadpool_workers

    def start(self) -> Iterator[Future]:
        with ThreadPoolExecutor(max_workers=self.max_threadpool_workers) as executor:
            return concurrent.futures.as_completed(
                [
                    executor.submit(self._archive, media_item)
                    for media_item in self.media_items
                ]
            )

    def _archive(self, media_item: MediaItem):
        if media_item.is_ready:
            return self.archiver.archive(media_item)
        return None
