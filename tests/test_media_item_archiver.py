from pathlib import Path

from src.archivers import DiskArchiver
from src.media_item_archiver import MediaItemArchiver
from tests.conftest import MockSuccessResponse


class TestMediaItemArchiver:
    def test_start_with_disk_archiver(
        self, mocker, test_photo_media_item, test_video_media_item, tmp_path
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

        MediaItemArchiver(
            media_items=media_items, archiver=DiskArchiver(download_path=tmp_path)
        ).start()

        for media_item in media_items:
            with Path(
                tmp_path,
                str(media_item.creationTime.year),
                str(media_item.creationTime.month),
                str(media_item.creationTime.day),
                media_item.filename,
            ).open("rb") as f:
                assert f.read() == fake_media_content
