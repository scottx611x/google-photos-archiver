import enum
from dataclasses import dataclass
from typing import Any, Dict, Optional

# pylint: disable=invalid-name

# Ref: https://developers.google.com/photos/library/guides/access-media-items


class VideoProcessingStatus(enum.Enum):
    """
    https://developers.google.com/photos/library/reference/rest/v1/mediaItems#VideoProcessingStatus
    """

    UNSPECIFIED = "UNSPECIFIED"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"


@dataclass
class CameraMetadata:
    cameraMake: str
    cameraModel: str


@dataclass
class PhotoMetadata(CameraMetadata):
    focalLength: float
    apertureFNumber: float
    isoEquivalent: int

    exposureTime: Optional[str] = None


@dataclass
class VideoMetadata(CameraMetadata):
    fps: int
    status: VideoProcessingStatus


@dataclass
class MediaMetadata:
    creationTime: str
    width: str
    height: str


@dataclass
class PhotoMediaMetadata(MediaMetadata):
    photo: Optional[PhotoMetadata] = None


@dataclass
class VideoMediaMetadata(MediaMetadata):
    video: Optional[VideoMetadata]


@dataclass
class MediaItem:
    id: str
    productUrl: str
    baseUrl: str
    mimeType: str
    filename: str

    mediaMetadata: MediaMetadata

    description: Optional[str] = None

    @property
    def downloadUrl(self):
        """
        Ref: https://developers.google.com/photos/library/guides/access-media-items
        """
        if isinstance(self.mediaMetadata, PhotoMediaMetadata):
            return self.baseUrl + "=d"
        return self.baseUrl + "=dv"


def create_media_item(media_item_dict: Dict[str, Any]) -> MediaItem:
    media_metadata_dict = media_item_dict["mediaMetadata"]

    photo_metadata = media_metadata_dict.get("photo", {})
    video_metadata = media_metadata_dict.get("video", {})

    if photo_metadata:
        photo_metadata: Optional[PhotoMetadata] = (
            PhotoMetadata(**photo_metadata) if photo_metadata else None
        )
        del media_metadata_dict["photo"]

        media_metadata: MediaMetadata = PhotoMediaMetadata(
            **media_metadata_dict, photo=photo_metadata
        )
    else:
        video_metadata: Optional[VideoMetadata] = (
            VideoMetadata(**video_metadata) if video_metadata else None
        )
        del media_metadata_dict["video"]
        media_metadata: MediaMetadata = VideoMediaMetadata(
            **media_metadata_dict, video=video_metadata
        )

    del media_item_dict["mediaMetadata"]
    return MediaItem(**media_item_dict, mediaMetadata=media_metadata)
