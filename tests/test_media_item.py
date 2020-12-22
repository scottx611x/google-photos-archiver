from src.media_item import (
    MediaItem,
    PhotoMediaMetadata,
    PhotoMetadata,
    VideoMediaMetadata,
    VideoMetadata,
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
)


def test_create_photo_media_item(test_photo_media_item):
    photo_media_item = create_media_item(test_photo_media_item)
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
    assert photo_media_item.downloadUrl == photo_media_item.baseUrl + "=d"


def test_create_video_media_item(test_video_media_item):
    video_media_item = create_media_item(test_video_media_item)
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
    assert video_media_item.downloadUrl == video_media_item.baseUrl + "=dv"
