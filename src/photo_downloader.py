import logging
import sys
from pathlib import Path
from typing import Iterable

import requests

from src.media_item import MediaItem, VideoMediaMetadata, VideoProcessingStatus

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


class GooglePhotoDownloader:
    def __init__(self, media_items: Iterable[MediaItem], download_path: Path):
        self.media_items = media_items

        download_path.mkdir(parents=True, exist_ok=True)
        self.download_path = download_path

    def download(self):
        for media_item in self.media_items:
            media_item_path = Path(self.download_path, media_item.filename)

            if media_item_path.exists():
                logger.info(
                    "MediaItem at path: %s already exists. Skipping download.",
                    str(media_item_path.absolute()),
                )
                continue

            if isinstance(media_item.mediaMetadata, VideoMediaMetadata):
                video_processing_status = media_item.mediaMetadata.video.status
                if video_processing_status != VideoProcessingStatus.READY.value:
                    logger.info(
                        "Video MediaItem with id: %s is not READY. Current status: %s. Skipping download.",
                        media_item.id,
                        video_processing_status,
                    )
                    continue

            logger.info(
                "Downloading MediaItem with id: %s to path: %s",
                media_item.id,
                str(media_item_path.absolute()),
            )
            response: requests.Response = requests.get(
                media_item.downloadUrl, stream=True
            )
            response.raise_for_status()

            self._write_to_disk(media_item_path, response)

    @staticmethod
    def _write_to_disk(media_item_path: Path, response: requests.Response):
        with media_item_path.open("wb") as f:
            f.write(response.raw.data)
