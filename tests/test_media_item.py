import copy

import pytest
import requests

from google_photos_archiver.media_item import (
    MediaItem,
    PhotoMediaMetadata,
    PhotoMetadata,
    VideoMediaMetadata,
    VideoMetadata,
    VideoProcessingStatus,
    create_media_item,
)
from tests.conftest import MockSuccessResponse


class TestMediaItem:
    def test_create_photo_media_item(self, test_photo_media_item_dict):
        test_photo_media_item_dict_copy = copy.deepcopy(test_photo_media_item_dict)
        photo_media_item = create_media_item(test_photo_media_item_dict)
        assert photo_media_item == MediaItem(
            id=test_photo_media_item_dict_copy["id"],
            productUrl=test_photo_media_item_dict_copy["productUrl"],
            baseUrl=test_photo_media_item_dict_copy["baseUrl"],
            mimeType=test_photo_media_item_dict_copy["mimeType"],
            mediaMetadata=PhotoMediaMetadata(
                creationTime=test_photo_media_item_dict_copy["mediaMetadata"][
                    "creationTime"
                ],
                width=test_photo_media_item_dict_copy["mediaMetadata"]["width"],
                height=test_photo_media_item_dict_copy["mediaMetadata"]["height"],
                photo=PhotoMetadata(
                    cameraMake=test_photo_media_item_dict_copy["mediaMetadata"][
                        "photo"
                    ]["cameraMake"],
                    cameraModel=test_photo_media_item_dict_copy["mediaMetadata"][
                        "photo"
                    ]["cameraModel"],
                    focalLength=test_photo_media_item_dict_copy["mediaMetadata"][
                        "photo"
                    ]["focalLength"],
                    apertureFNumber=test_photo_media_item_dict_copy["mediaMetadata"][
                        "photo"
                    ]["apertureFNumber"],
                    isoEquivalent=test_photo_media_item_dict_copy["mediaMetadata"][
                        "photo"
                    ]["isoEquivalent"],
                ),
            ),
            filename=test_photo_media_item_dict_copy["filename"],
        )

    def test_create_video_media_item(self, test_video_media_item_dict):
        test_video_media_item_dict_copy = copy.deepcopy(test_video_media_item_dict)
        video_media_item = create_media_item(test_video_media_item_dict)
        assert video_media_item == MediaItem(
            id=test_video_media_item_dict_copy["id"],
            productUrl=test_video_media_item_dict_copy["productUrl"],
            baseUrl=test_video_media_item_dict_copy["baseUrl"],
            mimeType=test_video_media_item_dict_copy["mimeType"],
            mediaMetadata=VideoMediaMetadata(
                creationTime=test_video_media_item_dict_copy["mediaMetadata"][
                    "creationTime"
                ],
                width=test_video_media_item_dict_copy["mediaMetadata"]["width"],
                height=test_video_media_item_dict_copy["mediaMetadata"]["height"],
                video=VideoMetadata(
                    cameraMake=test_video_media_item_dict_copy["mediaMetadata"][
                        "video"
                    ]["cameraMake"],
                    cameraModel=test_video_media_item_dict_copy["mediaMetadata"][
                        "video"
                    ]["cameraModel"],
                    fps=test_video_media_item_dict_copy["mediaMetadata"]["video"][
                        "fps"
                    ],
                    status=test_video_media_item_dict_copy["mediaMetadata"]["video"][
                        "status"
                    ],
                ),
            ),
            filename=test_video_media_item_dict_copy["filename"],
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
            "google_photos_archiver.rest_client.requests.get",
            return_value=MockSuccessResponse(mock_response_content),
        )

        assert test_photo_media_item.get_raw_data() == mock_response_content

    def test_get_raw_data_retries_on_connection_errors(
        self, mocker, test_photo_media_item
    ):
        mocker.patch("time.sleep")
        mock_response_content = bytes("abc123", "utf-8")
        mocker.patch(
            "google_photos_archiver.rest_client.requests.get",
            side_effect=[
                requests.ConnectionError(),
                requests.ConnectionError(),
                requests.ConnectionError(),
                requests.ConnectionError(),
                MockSuccessResponse(mock_response_content),
            ],
        )

        assert test_photo_media_item.get_raw_data() == mock_response_content

    def test_get_raw_data_retries_on_connection_errors_and_fails_after_too_many_attempts(
        self, mocker, test_photo_media_item
    ):
        mocker.patch("time.sleep")
        mocker.patch(
            "google_photos_archiver.rest_client.requests.get",
            side_effect=[
                requests.ConnectionError(),
                requests.ConnectionError(),
                requests.ConnectionError(),
                requests.ConnectionError(),
                requests.ConnectionError(),
                requests.ConnectionError(),
            ],
        )

        with pytest.raises(
            RuntimeError,
            match=f"Max attempts reached while trying to `get_raw_data` for: {test_photo_media_item.filename}",
        ):
            test_photo_media_item.get_raw_data()
