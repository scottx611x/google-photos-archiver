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


def _create_shared_album_options(
    share_info_dict: Dict[str, Any]
) -> Optional[SharedAlbumOptions]:
    shared_album_options_dict = share_info_dict.get("sharedAlbumOptions")

    if shared_album_options_dict is None:
        return shared_album_options_dict

    del share_info_dict["sharedAlbumOptions"]

    return SharedAlbumOptions(**shared_album_options_dict)


def _create_share_info(album_dict: Dict[str, Any]) -> Optional[ShareInfo]:
    share_info_dict = album_dict.get("shareInfo")

    if share_info_dict is None:
        return share_info_dict

    del album_dict["shareInfo"]

    return ShareInfo(
        sharedAlbumOptions=_create_shared_album_options(share_info_dict),
        **share_info_dict
    )


def create_album(album_dict: Dict[str, Any]) -> Album:
    return Album(shareInfo=_create_share_info(album_dict), **album_dict)
