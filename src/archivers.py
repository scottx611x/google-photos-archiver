import logging
from pathlib import Path

from src.media_item import MediaItem
from src.media_item_recorder import MediaItemRecorder

logger = logging.getLogger(__name__)


class Archivable:
    def __init__(self, recorder: MediaItemRecorder):
        self.recorder = recorder

    def archive(self, media_item: MediaItem):
        raise NotImplementedError(
            f"{self.__class__.__name__} subclasses must implement an archive method"
        )


class DiskArchiver(Archivable):
    def __init__(self, download_path: Path, recorder: MediaItemRecorder):
        super().__init__(recorder)
        download_path.mkdir(parents=True, exist_ok=True)
        self.download_path = download_path

    def archive(self, media_item: MediaItem) -> MediaItem:
        _media_item_path_prefix = Path(
            self.download_path,
            str(media_item.creationTime.year),
            str(media_item.creationTime.month),
            str(media_item.creationTime.day),
        )
        _media_item_path_prefix.mkdir(parents=True, exist_ok=True)

        media_item_path = Path(_media_item_path_prefix, media_item.filename)

        if media_item_path.exists() and self.recorder.lookup(media_item):
            logger.info(
                "MediaItem at path: %s already exists. Skipping download.",
                str(media_item_path.absolute()),
            )
            return media_item

        logger.info(
            "Downloading MediaItem with id: %s to path: %s",
            media_item.id,
            str(media_item_path.absolute()),
        )

        media_item_raw_data: bytes = media_item.get_raw_data()

        with media_item_path.open("wb") as f:
            f.write(media_item_raw_data)

        self.recorder.add(media_item)

        return media_item


class AWSGlacierArchiver(Archivable):
    def archive(self, media_item: MediaItem):
        pass
