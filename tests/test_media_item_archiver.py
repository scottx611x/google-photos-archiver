from pathlib import Path
from typing import List

import pytest

from google_photos_archiver.archivers import DiskArchiver
from google_photos_archiver.media_item import MediaItem
from google_photos_archiver.media_item_archiver import (
    MediaItemArchiver,
    get_new_media_item_archivals,
)
from tests.conftest import MockSuccessResponse

TEST_MEDIA_CONTENT = bytes("I'm a test photo or a video!", "utf-8")


@pytest.fixture()
def _test_media_items(
    mocker, test_photo_media_item, test_video_media_item
) -> List[MediaItem]:
    media_items = [test_photo_media_item, test_video_media_item]

    mocker.patch(
        "google_photos_archiver.rest_client.requests.get",
        side_effect=[
            MockSuccessResponse(TEST_MEDIA_CONTENT),
            MockSuccessResponse(TEST_MEDIA_CONTENT),
        ],
    )
    return media_items


class TestMediaItemArchiver:
    @pytest.mark.parametrize("has_album_path", [True, False])
    def test_start_with_disk_archiver(
        self, _test_media_items, test_media_item_recorder, tmp_path, has_album_path
    ):
        start_args = [_test_media_items]
        test_album_path = Path(tmp_path, "test_album")

        if has_album_path:
            start_args.append(test_album_path)

        completed_media_item_archivals = MediaItemArchiver(
            archiver=DiskArchiver(
                base_download_path=tmp_path, recorder=test_media_item_recorder
            ),
        ).start(*start_args)

        assert get_new_media_item_archivals(completed_media_item_archivals) == 2

        for media_item in _test_media_items:
            assert test_media_item_recorder.lookup(media_item) is True
            media_item_path = media_item.get_download_path(tmp_path)
            with media_item_path.open("rb") as f:
                assert f.read() == TEST_MEDIA_CONTENT

            if has_album_path:
                media_item_path_in_album = Path(test_album_path, media_item.filename)
                assert media_item_path_in_album.is_symlink()
                assert media_item_path_in_album.resolve() == media_item_path.resolve()


def test_get_new_media_item_archivals(
    _test_media_items,
    test_media_item_recorder,
    tmp_path,
):
    completed_media_item_archivals = MediaItemArchiver(
        archiver=DiskArchiver(
            base_download_path=tmp_path, recorder=test_media_item_recorder
        ),
    ).start(_test_media_items)
    assert get_new_media_item_archivals(completed_media_item_archivals) == 2
