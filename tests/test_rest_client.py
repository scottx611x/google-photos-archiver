import json

import pytest

from src.media_item import create_media_item
from src.rest_client import GooglePhotosApiRestClientError
from tests.conftest import MockFailureResponse, MockSuccessResponse, test_date_filter


class TestGooglePhotosApiRestClient:
    def test_get_media_items_success(self, google_photos_api_rest_client, mocker):
        mock_get = mocker.patch(
            "src.rest_client.requests.get",
            return_value=MockSuccessResponse(),
        )
        get_media_items_response = google_photos_api_rest_client.get_media_items()
        assert get_media_items_response.ok
        mock_get.assert_called_with(
            "https://photoslibrary.googleapis.com/v1/mediaItems",
            headers={"Authorization": "Bearer TEST_TOKEN"},
            params={"pageSize": 25},
        )

    @pytest.mark.parametrize(
        "params,expected_params",
        [
            (None, dict(pageSize=25)),
            (dict(page_size=123), dict(pageSize=123)),
            (dict(page_token="abc"), dict(pageSize=25, pageToken="abc")),
            (
                dict(page_size=123, page_token="abc"),
                dict(pageSize=123, pageToken="abc"),
            ),
        ],
    )
    def test_get_media_items_params(
        self, mocker, google_photos_api_rest_client, params, expected_params
    ):
        mock_get = mocker.patch(
            "src.rest_client.requests.get",
            return_value=MockSuccessResponse(),
        )
        if params is None:
            get_media_items_response = google_photos_api_rest_client.get_media_items()
        else:
            get_media_items_response = google_photos_api_rest_client.get_media_items(
                **params
            )
        assert get_media_items_response.ok
        mock_get.assert_called_with(
            "https://photoslibrary.googleapis.com/v1/mediaItems",
            headers={"Authorization": "Bearer TEST_TOKEN"},
            params=expected_params,
        )

    def test_get_media_items_failure(self, google_photos_api_rest_client, mocker):
        mock_get = mocker.patch(
            "src.rest_client.requests.get",
            return_value=MockFailureResponse(),
        )
        with pytest.raises(
            GooglePhotosApiRestClientError, match="Failed to execute: `get_media_items`"
        ):
            google_photos_api_rest_client.get_media_items()
        mock_get.assert_called_with(
            "https://photoslibrary.googleapis.com/v1/mediaItems",
            headers={"Authorization": "Bearer TEST_TOKEN"},
            params={"pageSize": 25},
        )

    def test_get_media_items_paginated(
        self,
        google_photos_api_rest_client,
        mocker,
        test_photo_media_item_dict,
        test_video_media_item_dict,
    ):
        mocker.patch(
            "src.rest_client.requests.get",
            side_effect=[
                MockSuccessResponse(
                    bytes(
                        json.dumps(
                            {
                                "mediaItems": [
                                    test_photo_media_item_dict,
                                ],
                                "nextPageToken": "abc123",
                            }
                        ),
                        "utf-8",
                    )
                ),
                MockSuccessResponse(
                    bytes(
                        json.dumps({"mediaItems": [test_video_media_item_dict]}),
                        "utf-8",
                    )
                ),
            ],
        )

        media_items = google_photos_api_rest_client.get_media_items_paginated(limit=2)

        photo_media_item = create_media_item(test_photo_media_item_dict)
        video_media_item = create_media_item(test_video_media_item_dict)

        assert list(media_items) == [photo_media_item, video_media_item]

    def test_search_media_items_success(self, google_photos_api_rest_client, mocker):
        mock_post = mocker.patch(
            "src.rest_client.requests.post",
            return_value=MockSuccessResponse(),
        )
        search_media_items_response = google_photos_api_rest_client.search_media_items()
        assert search_media_items_response.ok
        mock_post.assert_called_with(
            "https://photoslibrary.googleapis.com/v1/mediaItems:search",
            headers={"Authorization": "Bearer TEST_TOKEN"},
            params={"alt": "json"},
            json={"pageSize": 25},
        )

    @pytest.mark.parametrize(
        "_json,expected_json",
        [
            (None, dict(pageSize=25)),
            (dict(page_size=123), dict(pageSize=123)),
            (dict(page_token="abc"), dict(pageSize=25, pageToken="abc")),
            (
                dict(page_size=123, page_token="abc"),
                dict(pageSize=123, pageToken="abc"),
            ),
            (
                dict(filters=[test_date_filter()]),
                {"pageSize": 25, "filters": test_date_filter().get_filter()},
            ),
        ],
    )
    def test_search_media_items_params(
        self, mocker, google_photos_api_rest_client, _json, expected_json
    ):
        mock_get = mocker.patch(
            "src.rest_client.requests.post",
            return_value=MockSuccessResponse(),
        )
        if _json is None:
            search_media_items_response = (
                google_photos_api_rest_client.search_media_items()
            )
        else:
            search_media_items_response = (
                google_photos_api_rest_client.search_media_items(**_json)
            )
        assert search_media_items_response.ok
        mock_get.assert_called_with(
            "https://photoslibrary.googleapis.com/v1/mediaItems:search",
            headers={"Authorization": "Bearer TEST_TOKEN"},
            params={"alt": "json"},
            json=expected_json,
        )

    def test_search_media_items_failure(self, google_photos_api_rest_client, mocker):
        mock_get = mocker.patch(
            "src.rest_client.requests.post",
            return_value=MockFailureResponse(),
        )
        with pytest.raises(
            GooglePhotosApiRestClientError,
            match="Failed to execute: `search_media_items`",
        ):
            google_photos_api_rest_client.search_media_items()
        mock_get.assert_called_with(
            "https://photoslibrary.googleapis.com/v1/mediaItems:search",
            headers={"Authorization": "Bearer TEST_TOKEN"},
            params={"alt": "json"},
            json={"pageSize": 25},
        )

    def test_search_media_items_paginated(
        self,
        google_photos_api_rest_client,
        mocker,
        test_photo_media_item_dict,
        test_video_media_item_dict,
    ):
        mocker.patch(
            "src.rest_client.requests.post",
            side_effect=[
                MockSuccessResponse(
                    bytes(
                        json.dumps(
                            {
                                "mediaItems": [
                                    test_photo_media_item_dict,
                                ],
                                "nextPageToken": "abc123",
                            }
                        ),
                        "utf-8",
                    )
                ),
                MockSuccessResponse(
                    bytes(
                        json.dumps({"mediaItems": [test_video_media_item_dict]}),
                        "utf-8",
                    )
                ),
            ],
        )

        media_items = google_photos_api_rest_client.search_media_items_paginated(
            limit=2
        )

        photo_media_item = create_media_item(test_photo_media_item_dict)
        video_media_item = create_media_item(test_video_media_item_dict)

        assert list(media_items) == [photo_media_item, video_media_item]
