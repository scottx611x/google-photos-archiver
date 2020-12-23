import pytest

from src.media_item import (
    MediaItem,
    PhotoMediaMetadata,
    PhotoMetadata,
    VideoMediaMetadata,
    VideoMetadata,
    VideoProcessingStatus,
    create_media_item,
)
from tests.conftest import (
    TEST_APERTURE_F_NUMBER,
    TEST_CAMERA_MAKE,
    TEST_CAMERA_MODEL,
    TEST_CREATION_TIME,
    TEST_FOCAL_LENGTH,
    TEST_FPS,
    TEST_HEIGHT,
    TEST_ID,
    TEST_ISO_EQUIVALENT,
    TEST_PHOTO_FILENAME,
    TEST_PHOTO_MIMETYPE,
    TEST_URL,
    TEST_VIDEO_FILENAME,
    TEST_VIDEO_MIMETYPE,
    TEST_VIDEO_PROCESSING_STATUS,
    TEST_WIDTH,
    MockSuccessResponse,
)

# pylint: disable=redefined-outer-name


@pytest.fixture()
def test_photo_media_item(test_photo_media_item_dict) -> MediaItem:
    return create_media_item(test_photo_media_item_dict)


@pytest.fixture()
def test_video_media_item(test_video_media_item_dict) -> MediaItem:
    return create_media_item(test_video_media_item_dict)


class TestMediaItem:
    def test_create_photo_media_item(self, test_photo_media_item_dict):
        photo_media_item = create_media_item(test_photo_media_item_dict)
        assert photo_media_item == MediaItem(
            id=TEST_ID,
            productUrl=TEST_URL,
            baseUrl=TEST_URL,
            mimeType=TEST_PHOTO_MIMETYPE,
            mediaMetadata=PhotoMediaMetadata(
                creationTime=TEST_CREATION_TIME,
                width=TEST_WIDTH,
                height=TEST_HEIGHT,
                photo=PhotoMetadata(
                    cameraMake=TEST_CAMERA_MAKE,
                    cameraModel=TEST_CAMERA_MODEL,
                    focalLength=TEST_FOCAL_LENGTH,
                    apertureFNumber=TEST_APERTURE_F_NUMBER,
                    isoEquivalent=TEST_ISO_EQUIVALENT,
                ),
            ),
            filename=TEST_PHOTO_FILENAME,
        )

    def test_create_video_media_item(self, test_video_media_item_dict):
        video_media_item = create_media_item(test_video_media_item_dict)
        assert video_media_item == MediaItem(
            id=TEST_ID,
            productUrl=TEST_URL,
            baseUrl=TEST_URL,
            mimeType=TEST_VIDEO_MIMETYPE,
            mediaMetadata=VideoMediaMetadata(
                creationTime=TEST_CREATION_TIME,
                width=TEST_WIDTH,
                height=TEST_HEIGHT,
                video=VideoMetadata(
                    cameraMake=TEST_CAMERA_MAKE,
                    cameraModel=TEST_CAMERA_MODEL,
                    fps=TEST_FPS,
                    status=TEST_VIDEO_PROCESSING_STATUS,
                ),
            ),
            filename=TEST_VIDEO_FILENAME,
        )

    def test_download_url(self, test_photo_media_item, test_video_media_item):
        assert test_photo_media_item.downloadUrl == test_photo_media_item.baseUrl + "=d"
        assert (
            test_video_media_item.downloadUrl == test_video_media_item.baseUrl + "=dv"
        )

    def test_media_item_is_ready(self, test_photo_media_item, test_video_media_item):
        assert test_photo_media_item.is_ready is True
        assert test_video_media_item.is_ready is True

        test_video_media_item.mediaMetadata.video.status = (
            VideoProcessingStatus.PROCESSING.value
        )

        assert test_video_media_item.is_ready is False

    def test_get_raw_data(self, mocker, test_photo_media_item):
        mock_response_content = bytes("abc123", "utf-8")

        mocker.patch(
            "src.rest_client.requests.get",
            return_value=MockSuccessResponse(mock_response_content),
        )

        assert test_photo_media_item.get_raw_data() == mock_response_content
