from dataclasses import dataclass
from typing import Any, Dict, Optional

# pylint: disable=invalid-name


@dataclass
class SharedAlbumOptions:
    """
    https://developers.google.com/photos/library/reference/rest/v1/albums#Album.SharedAlbumOptions
    """

    isCollaborative: bool
    isCommentable: bool


@dataclass
class ShareInfo:
    """
    https://developers.google.com/photos/library/reference/rest/v1/albums#Album.ShareInfo
    """

    sharedAlbumOptions: SharedAlbumOptions
    shareableUrl: str
    shareToken: str
    isJoined: bool
    isOwned: bool
    isJoinable: bool


@dataclass
class Album:
    """
    https://developers.google.com/photos/library/reference/rest/v1/albums#Album
    """

    # pylint: disable=too-many-instance-attributes

    id: str
    productUrl: str
    mediaItemsCount: str
    coverPhotoBaseUrl: str
    coverPhotoMediaItemId: str
    title: Optional[str] = None
    isWriteable: Optional[bool] = None
    shareInfo: Optional[ShareInfo] = None


def create_album(album_dict: Dict[str, Any]) -> Album:
    return Album(**album_dict)
