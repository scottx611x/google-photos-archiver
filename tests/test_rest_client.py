import json

import pytest

from src.filters import Date, DateFilter, DateRange
from src.media_item import create_media_item
from src.rest_client import GooglePhotosApiRestClient, GooglePhotosApiRestClientError
from tests.conftest import MockFailureResponse, MockSuccessResponse

TEST_TOKEN = "TEST_TOKEN"

# pylint: disable=redefined-outer-name


@pytest.fixture()
def google_photos_api_rest_client(mocker) -> GooglePhotosApiRestClient:
    # We'll test this separately
    mock_oauth_handler = mocker.patch("src.oauth_handler.GoogleOauthHandler")
    mock_oauth_handler.token = TEST_TOKEN

    return GooglePhotosApiRestClient(mock_oauth_handler)


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
        "json,expected_json",
        [
            (None, dict(pageSize=25)),
            (dict(page_size=123), dict(pageSize=123)),
            (dict(page_token="abc"), dict(pageSize=25, pageToken="abc")),
            (
                dict(page_size=123, page_token="abc"),
                dict(pageSize=123, pageToken="abc"),
            ),
            (
                dict(
                    filters=[
                        DateFilter(
                            dates=[
                                Date(year=2021, month=1, day=1),
                            ],
                            date_ranges=[
                                DateRange(
                                    startDate=Date(year=2021, month=1, day=1),
                                    endDate=Date(year=2021, month=2, day=2),
                                )
                            ],
                        )
                    ]
                ),
                {
                    "pageSize": 25,
                    "filters": {
                        "dateFilter": {
                            "dates": [{"year": 2021, "month": 1, "day": 1}],
                            "ranges": [
                                {
                                    "startDate": {"year": 2021, "month": 1, "day": 1},
                                    "endDate": {"year": 2021, "month": 2, "day": 2},
                                }
                            ],
                        }
                    },
                },
            ),
        ],
    )
    def test_search_media_items_params(
        self, mocker, google_photos_api_rest_client, json, expected_json
    ):
        mock_get = mocker.patch(
            "src.rest_client.requests.post",
            return_value=MockSuccessResponse(),
        )
        if json is None:
            search_media_items_response = (
                google_photos_api_rest_client.search_media_items()
            )
        else:
            search_media_items_response = (
                google_photos_api_rest_client.search_media_items(**json)
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
