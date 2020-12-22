import enum
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

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
class PhotoMetadata:
    focalLength: float
    apertureFNumber: float
    isoEquivalent: int

    exposureTime: Optional[str] = None
    cameraMake: Optional[str] = None
    cameraModel: Optional[str] = None


@dataclass
class VideoMetadata:
    status: VideoProcessingStatus

    fps: Optional[int] = None
    cameraMake: Optional[str] = None
    cameraModel: Optional[str] = None


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


def _media_metadata_factory(
    media_item_dict,
) -> Union[PhotoMediaMetadata, VideoMediaMetadata]:
    media_metadata_dict = media_item_dict["mediaMetadata"]
    photo_metadata_dict = media_metadata_dict.get("photo")
    video_metadata_dict = media_metadata_dict.get("video")

    if photo_metadata_dict is not None:
        photo_metadata: Optional[PhotoMetadata] = (
            None if photo_metadata_dict == {} else PhotoMetadata(**photo_metadata_dict)
        )
        del media_metadata_dict["photo"]
        media_metadata = PhotoMediaMetadata(**media_metadata_dict, photo=photo_metadata)
    else:
        video_metadata: Optional[VideoMetadata] = (
            None if video_metadata_dict == {} else VideoMetadata(**video_metadata_dict)
        )
        del media_metadata_dict["video"]
        media_metadata = VideoMediaMetadata(**media_metadata_dict, video=video_metadata)

    del media_item_dict["mediaMetadata"]

    return media_metadata


def create_media_item(media_item_dict: Dict[str, Any]) -> MediaItem:
    return MediaItem(
        **media_item_dict, mediaMetadata=_media_metadata_factory(media_item_dict)
    )
