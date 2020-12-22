from dataclasses import dataclass
from typing import Any, Dict

# pylint: disable=invalid-name


@dataclass
class PhotoMetaData:
    cameraMake: str
    cameraModel: str
    focalLength: float
    apertureFNumber: float
    isoEquivalent: float


@dataclass
class MediaMetadata:
    creationTime: str
    width: str
    height: str
    photo: PhotoMetaData


@dataclass
class MediaItem:
    id: str
    productUrl: str
    baseUrl: str
    mimeType: str
    mediaMetadata: MediaMetadata
    filename: str


def create_media_item(media_item_dict: Dict[str, Any]) -> MediaItem:
    media_metadata_dict = media_item_dict["mediaMetadata"]
    photo_metadata: PhotoMetaData = PhotoMetaData(**media_metadata_dict["photo"])
    del media_metadata_dict["photo"]
    media_metadata: MediaMetadata = MediaMetadata(
        **media_metadata_dict, photo=photo_metadata
    )
    del media_item_dict["mediaMetadata"]
    return MediaItem(**media_item_dict, mediaMetadata=media_metadata)
