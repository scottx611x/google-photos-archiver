import logging
from pathlib import Path
from typing import Optional

from google_photos_archiver.media_item import MediaItem
from google_photos_archiver.media_item_recorder import MediaItemRecorder

logger = logging.getLogger(__name__)


class Archivable:
    def __init__(self, recorder: MediaItemRecorder):
        self.recorder = recorder

    def archive(self, media_item: MediaItem, album_path: Optional[Path] = None) -> bool:
        raise NotImplementedError(
            f"{self.__class__.__name__} subclasses must implement an archive method"
        )


class DiskArchiver(Archivable):
    def __init__(self, base_download_path: Path, recorder: MediaItemRecorder):
        super().__init__(recorder)
        base_download_path.mkdir(parents=True, exist_ok=True)
        self.base_download_path = base_download_path

    def archive(self, media_item: MediaItem, album_path: Optional[Path] = None) -> bool:
        media_item_path = media_item.get_download_path(self.base_download_path)

        if album_path is not None:
            album_path.mkdir(parents=True, exist_ok=True)
            media_item_in_album = Path(album_path, media_item.filename)
            logger.info("Symlinking %s to %s", media_item_in_album, media_item_path)
            try:
                media_item_in_album.symlink_to(media_item_path)
            except FileExistsError:
                pass

        if media_item_path.exists() and self.recorder.lookup(media_item):
            logger.info(
                "MediaItem at path: %s already exists. Skipping download.",
                str(media_item_path.absolute()),
            )
            return False

        logger.info(
            "Downloading MediaItem with id: %s to path: %s",
            media_item.id,
            str(media_item_path.absolute()),
        )

        media_item_raw_data: bytes = media_item.get_raw_data()

        with media_item_path.open("wb") as f:
            f.write(media_item_raw_data)

        self.recorder.add(media_item)

        return True
