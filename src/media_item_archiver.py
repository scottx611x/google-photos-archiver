import logging
import sys
from typing import Iterable

from src.archivers import Archivable
from src.media_item import MediaItem

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


class MediaItemArchiver:
    def __init__(self, media_items: Iterable[MediaItem], archiver: Archivable):
        self.media_items = media_items
        self.archiver = archiver

    def start(self):
        for media_item in self.media_items:
            if media_item.is_ready:
                self.archiver.archive(media_item)
