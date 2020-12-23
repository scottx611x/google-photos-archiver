import json
from unittest.mock import MagicMock

import pytest
from pytest_socket import disable_socket
from requests import Response

from src.media_item import VideoProcessingStatus


def pytest_runtest_setup():
    disable_socket()


TEST_ID = "abc123"
TEST_URL = "http://www.example.com"
TEST_PHOTO_MIMETYPE = "image/jpeg"
TEST_PHOTO_FILENAME = "test.jpg"
TEST_VIDEO_MIMETYPE = "video/mp4"
TEST_VIDEO_FILENAME = "test.mp4"
TEST_CREATION_TIME = "2020-12-22T01:23:45Z"
TEST_WIDTH = "1024"
TEST_HEIGHT = "2048"
TEST_CAMERA_MAKE = "TEST_CAMERA_MAKE"
TEST_CAMERA_MODEL = "TEST_CAMERA_MODEL"
TEST_FOCAL_LENGTH = 1.23
TEST_APERTURE_F_NUMBER = 1.23
TEST_ISO_EQUIVALENT = 123

TEST_FPS = 30
TEST_VIDEO_PROCESSING_STATUS = VideoProcessingStatus.READY.value


@pytest.fixture()
def test_photo_media_item_dict():
    return {
        "id": TEST_ID,
        "productUrl": TEST_URL,
        "baseUrl": TEST_URL,
        "mimeType": TEST_PHOTO_MIMETYPE,
        "filename": TEST_PHOTO_FILENAME,
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
    }


@pytest.fixture()
def test_video_media_item_dict():
    return {
        "id": TEST_ID,
        "productUrl": TEST_URL,
        "baseUrl": TEST_URL,
        "mimeType": TEST_VIDEO_MIMETYPE,
        "filename": TEST_VIDEO_FILENAME,
        "mediaMetadata": {
            "creationTime": TEST_CREATION_TIME,
            "width": TEST_WIDTH,
            "height": TEST_HEIGHT,
            "video": {
                "cameraMake": TEST_CAMERA_MAKE,
                "cameraModel": TEST_CAMERA_MODEL,
                "fps": TEST_FPS,
                "status": TEST_VIDEO_PROCESSING_STATUS,
            },
        },
    }


class MockResponse(Response):
    def __init__(self, content: bytes, status_code: int):
        super().__init__()
        self.encoding = "utf-8"
        self._content = content
        self.status_code = status_code

        self.raw = MagicMock()
        self.raw.data = self._content


class MockSuccessResponse(MockResponse):
    def __init__(
        self,
        content=bytes(json.dumps({"message": "Success"}), "utf-8"),
        status_code=200,
    ):
        super().__init__(content, status_code)


class MockFailureResponse(MockResponse):
    def __init__(
        self,
        content=bytes(json.dumps({"message": "Failure"}), "utf-8"),
        status_code=400,
    ):
        super().__init__(content, status_code)
