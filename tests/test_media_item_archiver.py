from pathlib import Path

from src.archivers import DiskArchiver
from src.media_item_archiver import MediaItemArchiver, get_new_media_item_archivals
from tests.conftest import MockSuccessResponse


class TestMediaItemArchiver:
    # pylint: disable=too-many-arguments
    def test_start_with_disk_archiver(
        self,
        mocker,
        test_photo_media_item,
        test_video_media_item,
        test_media_item_recorder,
        tmp_path,
    ):
        media_items = [test_photo_media_item, test_video_media_item]
        fake_media_content = bytes("I'm a test photo or a video!", "utf-8")

        mocker.patch(
            "src.rest_client.requests.get",
            side_effect=[
                MockSuccessResponse(fake_media_content),
                MockSuccessResponse(fake_media_content),
            ],
        )

        completed_media_item_archivals = MediaItemArchiver(
            media_items=media_items,
            archiver=DiskArchiver(
                download_path=tmp_path, recorder=test_media_item_recorder
            ),
        ).start()

        assert get_new_media_item_archivals(completed_media_item_archivals) == 2

        for media_item in media_items:
            assert test_media_item_recorder.lookup(media_item) is True
            with Path(
                tmp_path,
                str(media_item.creationTime.year),
                str(media_item.creationTime.month),
                str(media_item.creationTime.day),
                media_item.filename,
            ).open("rb") as f:
                assert f.read() == fake_media_content


def test_get_new_media_item_archivals(
    mocker,
    test_media_item_recorder,
    test_photo_media_item,
    test_video_media_item,
    tmp_path,
):
    media_items = [test_photo_media_item, test_video_media_item]

    fake_media_content = bytes("I'm a test photo or a video!", "utf-8")

    mocker.patch(
        "src.rest_client.requests.get",
        side_effect=[
            MockSuccessResponse(fake_media_content),
            MockSuccessResponse(fake_media_content),
        ],
    )

    completed_media_item_archivals = MediaItemArchiver(
        media_items=media_items,
        archiver=DiskArchiver(
            download_path=tmp_path, recorder=test_media_item_recorder
        ),
    ).start()
    assert get_new_media_item_archivals(completed_media_item_archivals) == 2
