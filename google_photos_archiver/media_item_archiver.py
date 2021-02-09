import concurrent
import logging
from concurrent.futures._base import Future
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable, Iterator, Optional

from google_photos_archiver.archivers import Archivable
from google_photos_archiver.media_item import MediaItem

logger = logging.getLogger(__name__)


class MediaItemArchiver:
    def __init__(
        self,
        archiver: Archivable,
        max_threadpool_workers: int = 25,
    ):
        self.archiver = archiver
        self.max_threadpool_workers = max_threadpool_workers

    def start(
        self, media_items: Iterable[MediaItem], album_path: Optional[Path] = None
    ) -> Iterator[Future]:
        with ThreadPoolExecutor(max_workers=self.max_threadpool_workers) as executor:
            return concurrent.futures.as_completed(
                [
                    executor.submit(self._archive, media_item, album_path)
                    for media_item in media_items
                ]
            )

    def _archive(
        self, media_item: MediaItem, album_path: Optional[Path] = None
    ) -> bool:
        if media_item.is_ready:
            return self.archiver.archive(media_item, album_path)
        return False


def get_new_media_item_archivals(
    completed_media_item_archivals: Iterator[Future],
) -> int:
    return sum(
        int(completed_media_item_archival.result())
        for completed_media_item_archival in completed_media_item_archivals
    )
