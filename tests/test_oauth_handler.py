import json
from pathlib import Path

import pytest

from src.oauth_handler import GoogleOauthHandler
from tests.conftest import MockSuccessResponse

TEST_CLIENT_ID = "TEST_CLIENT_ID"
TEST_CLIENT_SECRET = "TEST_CLIENT_SECRET"
TEST_TOKEN = "TEST_TOKEN"
TEST_REFRESH_TOKEN = "TEST_REFRESH_TOKEN"


class MockCredentials:
    def __init__(self):
        self.token = TEST_TOKEN
        self.refresh_token = TEST_REFRESH_TOKEN


@pytest.fixture(autouse=True)
def mock_installed_app_flow(mocker):
    _mock_installed_app_flow = mocker.patch("src.oauth_handler.InstalledAppFlow")
    _mock_installed_app_flow.from_client_secrets_file().client_config = {
        "client_id": TEST_CLIENT_ID,
        "client_secret": TEST_CLIENT_SECRET,
    }
    _mock_installed_app_flow.from_client_secrets_file().run_local_server.return_value = (
        MockCredentials()
    )


class TestGoogleOauthHandler:
    def test_token_gets_set(self, tmp_path):
        google_oauth_handler = GoogleOauthHandler(
            Path(tmp_path, "client_secret.json"), Path(tmp_path, "refresh_token")
        )
        assert google_oauth_handler.token == TEST_TOKEN

    def test_refresh_token_is_stored(self, tmp_path):
        google_oauth_handler = GoogleOauthHandler(
            Path(tmp_path, "client_secret.json"), Path(tmp_path, "refresh_token")
        )
        assert google_oauth_handler.read_refresh_token() == TEST_REFRESH_TOKEN

    def test_token_gets_set_using_existing_refresh_token(self, mocker, tmp_path):
        new_access_token = "new_access_token"

        refresh_token_path = Path(tmp_path, "refresh_token")
        with refresh_token_path.open("w") as f:
            f.write(TEST_REFRESH_TOKEN)

        mock_post = mocker.patch(
            "src.oauth_handler.requests.post",
            return_value=MockSuccessResponse(
                bytes(json.dumps({"access_token": new_access_token}), "utf-8")
            ),
        )

        google_oauth_handler = GoogleOauthHandler(
            Path(tmp_path, "client_secret.json"), refresh_token_path
        )

        mock_post.assert_called_with(
            "https://www.googleapis.com/oauth2/v4/token",
            data={
                "grant_type": "refresh_token",
                "client_id": TEST_CLIENT_ID,
                "client_secret": TEST_CLIENT_SECRET,
                "refresh_token": TEST_REFRESH_TOKEN,
            },
        )

        assert google_oauth_handler.token == new_access_token
