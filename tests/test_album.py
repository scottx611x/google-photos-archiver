import copy

from google_photos_archiver.album import (
    Album,
    SharedAlbumOptions,
    ShareInfo,
    create_album,
)


class TestAlbum:
    def test_create_album(self, test_album_dict):
        test_album_dict_copy = copy.deepcopy(test_album_dict)
        assert create_album(test_album_dict_copy) == Album(
            id=test_album_dict["id"],
            productUrl=test_album_dict["productUrl"],
            mediaItemsCount=test_album_dict["mediaItemsCount"],
            coverPhotoBaseUrl=test_album_dict["coverPhotoBaseUrl"],
            coverPhotoMediaItemId=test_album_dict["coverPhotoMediaItemId"],
            title=test_album_dict["title"],
            isWriteable=test_album_dict["isWriteable"],
            shareInfo=ShareInfo(
                sharedAlbumOptions=SharedAlbumOptions(
                    isCollaborative=test_album_dict["shareInfo"]["sharedAlbumOptions"][
                        "isCollaborative"
                    ],
                    isCommentable=test_album_dict["shareInfo"]["sharedAlbumOptions"][
                        "isCommentable"
                    ],
                ),
                shareableUrl=test_album_dict["shareInfo"]["shareableUrl"],
                shareToken=test_album_dict["shareInfo"]["shareToken"],
                isJoined=test_album_dict["shareInfo"]["isJoined"],
                isOwned=test_album_dict["shareInfo"]["isOwned"],
                isJoinable=test_album_dict["shareInfo"]["isJoinable"],
            ),
        )
