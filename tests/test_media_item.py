from typing import Any, Dict

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

TEST_FPS = 30
TEST_VIDEO_PROCESSING_STATUS = VideoProcessingStatus.READY

# pylint: disable=redefined-outer-name


@pytest.fixture()
def test_media_item():
    return {
        "id": TEST_ID,
        "productUrl": TEST_URL,
        "baseUrl": TEST_URL,
        "mimeType": TEST_MIMETYPE,
        "filename": TEST_FILENAME,
    }


@pytest.fixture()
def test_photo_media_item(test_media_item):
    test_media_item["mediaMetadata"] = {
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
    }
    return test_media_item


@pytest.fixture()
def test_video_media_item(test_media_item):
    test_media_item["mediaMetadata"]: Dict[str, Any] = {
        "creationTime": TEST_CREATION_TIME,
        "width": TEST_WIDTH,
        "height": TEST_HEIGHT,
        "video": {
            "cameraMake": TEST_CAMERA_MAKE,
            "cameraModel": TEST_CAMERA_MODEL,
            "fps": TEST_FPS,
            "status": TEST_VIDEO_PROCESSING_STATUS,
        },
    }
    return test_media_item


def test_create_photo_media_item(test_photo_media_item):
    photo_media_item = create_media_item(test_photo_media_item)
    assert photo_media_item == MediaItem(
        id=TEST_ID,
        productUrl=TEST_URL,
        baseUrl=TEST_URL,
        mimeType=TEST_MIMETYPE,
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
        filename=TEST_FILENAME,
    )
    assert photo_media_item.downloadUrl == photo_media_item.baseUrl + "=d"


def test_create_video_media_item(test_video_media_item):
    video_media_item = create_media_item(test_video_media_item)
    assert video_media_item == MediaItem(
        id=TEST_ID,
        productUrl=TEST_URL,
        baseUrl=TEST_URL,
        mimeType=TEST_MIMETYPE,
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
        filename=TEST_FILENAME,
    )
    assert video_media_item.downloadUrl == video_media_item.baseUrl + "=dv"
