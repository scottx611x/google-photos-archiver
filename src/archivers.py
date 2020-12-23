import logging
from pathlib import Path

from src.media_item import MediaItem

logger = logging.getLogger(__name__)


class Archivable:
    def archive(self, media_item: MediaItem):
        raise NotImplementedError(
            f"{self.__class__.__name__} subclasses must implement an archive method"
        )


class DiskArchiver(Archivable):
    def __init__(self, download_path: Path):
        download_path.mkdir(parents=True, exist_ok=True)
        self.download_path = download_path

    def archive(self, media_item: MediaItem):
        media_item_path = Path(self.download_path, media_item.filename)

        if media_item_path.exists():
            logger.info(
                "MediaItem at path: %s already exists. Skipping download.",
                str(media_item_path.absolute()),
            )
            return

        logger.info(
            "Downloading MediaItem with id: %s to path: %s",
            media_item.id,
            str(media_item_path.absolute()),
        )

        media_item_raw_data: bytes = media_item.get_raw_data()

        with media_item_path.open("wb") as f:
            f.write(media_item_raw_data)


class AWSGlacierArchiver(Archivable):
    def archive(self, media_item: MediaItem):
        pass
