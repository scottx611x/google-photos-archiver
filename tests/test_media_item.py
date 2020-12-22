import pytest

from src.media_item import MediaItem, MediaMetadata, PhotoMetaData, create_media_item

TEST_ID = "abc123"
TEST_URL = "http://www.example.com"
TEST_MIMETYPE = "image/jpeg"
TEST_FILENAME = "test.jpg"
TEST_CREATION_TIME = "2020-12-22T01:23:45Z"
TEST_WIDTH = "1024"
TEST_HEIGHT = "2048"
TEST_CAMERA_MAKE = "TEST_CAMERA_MAKE"
TEST_CAMERA_MODEL = "TEST_CAMERA_MODEL"
TEST_FOCAL_LENGTH = 1.23
TEST_APERTURE_F_NUMBER = 1.23
TEST_ISO_EQUIVALENT = 123

# pylint: disable=redefined-outer-name


@pytest.fixture()
def test_media_item():
    return {
        "id": TEST_ID,
        "productUrl": TEST_URL,
        "baseUrl": TEST_URL,
        "mimeType": TEST_MIMETYPE,
        "mediaMetadata": {
            "creationTime": TEST_CREATION_TIME,
            "width": TEST_WIDTH,
            "height": TEST_HEIGHT,
            "photo": {
                "cameraMake": TEST_CAMERA_MAKE,
                "cameraModel": TEST_CAMERA_MODEL,
                "focalLength": TEST_FOCAL_LENGTH,
                "apertureFNumber": TEST_APERTURE_F_NUMBER,
                "isoEquivalent": TEST_ISO_EQUIVALENT,
            },
        },
        "filename": TEST_FILENAME,
    }


def test_create_media_item(test_media_item):
    assert create_media_item(test_media_item) == MediaItem(
        id=TEST_ID,
        productUrl=TEST_URL,
        baseUrl=TEST_URL,
        mimeType=TEST_MIMETYPE,
        mediaMetadata=MediaMetadata(
            creationTime=TEST_CREATION_TIME,
            width=TEST_WIDTH,
            height=TEST_HEIGHT,
            photo=PhotoMetaData(
                cameraMake=TEST_CAMERA_MAKE,
                cameraModel=TEST_CAMERA_MODEL,
                focalLength=TEST_FOCAL_LENGTH,
                apertureFNumber=TEST_APERTURE_F_NUMBER,
                isoEquivalent=TEST_ISO_EQUIVALENT,
            ),
        ),
        filename=TEST_FILENAME,
    )
