import pytest

from src.rest_client import (GooglePhotosApiRestClient,
                             GooglePhotosApiRestClientError)
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
        "params,expected_params", [
            (
                None, dict(pageSize=25)
            ),
            (
                dict(page_size=123), dict(pageSize=123)
            ),
            (
                dict(page_token="abc"), dict(pageSize=25, pageToken="abc")
            ),
            (
                dict(page_size=123, page_token="abc"), dict(pageSize=123, pageToken="abc")
            ),


        ]
    )
    def test_get_media_items_params(self, mocker, google_photos_api_rest_client, params, expected_params):
        mock_get = mocker.patch(
            "src.rest_client.requests.get",
            return_value=MockSuccessResponse(),
        )
        if params is None:
            get_media_items_response = google_photos_api_rest_client.get_media_items()
        else:
            get_media_items_response = google_photos_api_rest_client.get_media_items(**params)
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
