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
    # pylint: disable=too-many-arguments
    def test_start_with_disk_archiver(
        self,
        _test_media_items,
        test_media_item_recorder,
        tmp_path,
    ):
        completed_media_item_archivals = MediaItemArchiver(
            media_items=_test_media_items,
            archiver=DiskArchiver(
                download_path=tmp_path, recorder=test_media_item_recorder
            ),
        ).start()

        assert get_new_media_item_archivals(completed_media_item_archivals) == 2

        for media_item in _test_media_items:
            assert test_media_item_recorder.lookup(media_item) is True
            with Path(
                tmp_path,
                str(media_item.creationTime.year),
                str(media_item.creationTime.month),
                str(media_item.creationTime.day),
                media_item.filename,
            ).open("rb") as f:
                assert f.read() == TEST_MEDIA_CONTENT


def test_get_new_media_item_archivals(
    _test_media_items,
    test_media_item_recorder,
    tmp_path,
):
    completed_media_item_archivals = MediaItemArchiver(
        media_items=_test_media_items,
        archiver=DiskArchiver(
            download_path=tmp_path, recorder=test_media_item_recorder
        ),
    ).start()
    assert get_new_media_item_archivals(completed_media_item_archivals) == 2
