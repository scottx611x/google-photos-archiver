from pathlib import Path
from typing import Any, Dict, Optional

import requests
from google.oauth2.credentials import Credentials as GoogleOauthCredentials
from google_auth_oauthlib.flow import InstalledAppFlow


class GoogleOauthHandler:
    """
    Gets a fresh token or refreshes an already existing token using Google's oauthlib's InstalledAppFlow

    Ref: https://googleapis.github.io/google-api-python-client/docs/oauth-installed.html
    """

    def __init__(self, client_secret_file_path: Path, refresh_token_path: Path):
        self._authorization_url = "https://www.googleapis.com/oauth2/v4/token"
        self._client_secret_file_path = client_secret_file_path
        self._refresh_token_path = refresh_token_path
        self._flow: InstalledAppFlow = self._get_flow()
        self._client_config: Dict[str, Any] = self._flow.client_config

        refresh_token = self.read_refresh_token()
        if refresh_token:
            self.token = self.refresh_existing_token(refresh_token).json()[
                "access_token"
            ]
        else:
            self.token = self._get_token()

    def _get_token(self):
        credentials: GoogleOauthCredentials = self._flow.run_local_server(
            host="localhost",
            port=8080,
            authorization_prompt_message="Please visit this URL: {url}",
            success_message="The auth flow is complete; you may close this window.",
            open_browser=True,
        )
        self._write_refresh_token(credentials)
        return credentials.token

    def _get_flow(self) -> InstalledAppFlow:
        return InstalledAppFlow.from_client_secrets_file(
            str(self._client_secret_file_path),
            scopes=["https://www.googleapis.com/auth/photoslibrary.readonly"],
        )

    def _write_refresh_token(self, credentials: GoogleOauthCredentials):
        with self._refresh_token_path.open("w") as f:
            f.write(credentials.refresh_token)

    def read_refresh_token(self) -> Optional[str]:
        try:
            with self._refresh_token_path.open() as f:
                return f.read()
        except FileNotFoundError:
            return None

    def refresh_existing_token(self, refresh_token: str) -> requests.Response:
        params = {
            "grant_type": "refresh_token",
            "client_id": self._client_config["client_id"],
            "client_secret": self._client_config["client_secret"],
            "refresh_token": refresh_token,
        }

        refresh_token_response = requests.post(self._authorization_url, data=params)
        refresh_token_response.raise_for_status()

        return refresh_token_response
