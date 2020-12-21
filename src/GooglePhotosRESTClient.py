from pathlib import Path
from urllib.parse import urljoin

import requests
from google.oauth2.credentials import Credentials as GoogleOauthCredentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from typing import Callable, Dict, Optional, Any

from requests import Response


def handle_request_errors(decorated_function: Callable):
    """
    Decorator that handles for potential requests library errors that may occur when calling the wrapped function
    """

    def wrapper(self, *args, **kwargs):
        try:
            return decorated_function(self, *args, **kwargs)
        except requests.RequestException as err:
            raise GooglePhotosApiRestClientError(
                f"Failed to execute: `{decorated_function.__name__}` {err}"
            ) from err

    return wrapper


def for_all_methods(decorator):
    """
    Ref: https://stackoverflow.com/a/6307868
    """

    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


class GooglePhotosApiRestClientError(RuntimeError):
    pass


class GoogleOauthHandler(object):
    def __init__(
        self,
        client_secret_file_path: Path,
    ):
        self._authorization_url = "https://www.googleapis.com/oauth2/v4/token"
        self._client_secret_file_path = client_secret_file_path
        self._flow: InstalledAppFlow = self._get_flow()
        self._client_config: Dict[str, Any] = self._flow.client_config

        refresh_token = self._read_refresh_token()
        if refresh_token:
            self.token = self.refresh_token(refresh_token).json()["access_token"]
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
        flow = InstalledAppFlow.from_client_secrets_file(
            str(self._client_secret_file_path),
            scopes=["https://www.googleapis.com/auth/photoslibrary.readonly"],
        )
        return flow

    def _read_refresh_token(self) -> Optional[str]:
        try:
            with open("../refresh_token") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def _write_refresh_token(self, credentials: GoogleOauthCredentials):
        with open("../refresh_token", "w") as f:
            f.write(credentials.refresh_token)

    def refresh_token(self, refresh_token: str) -> Response:
        params = {
            "grant_type": "refresh_token",
            "client_id": self._client_config["client_id"],
            "client_secret": self._client_config["client_secret"],
            "refresh_token": refresh_token
        }

        refresh_token_response = requests.post(self._authorization_url, data=params)
        refresh_token_response.raise_for_status()

        return refresh_token_response


@for_all_methods(handle_request_errors)
class GooglePhotosApiRestClient(GoogleOauthHandler):
    """
    Helper class for easily interacting with the Google Photos API REST interface
    Refer to: https://developers.google.com/photos/library/guides/get-started
    """

    def __init__(self, client_secret_file_path: Path, api_url: str = "https://photoslibrary.googleapis.com/v1/"):

        super().__init__(client_secret_file_path)
        self.api_url = api_url
        self._auth_header: Dict[str, str] = {
            "Authorization": f"Bearer {self.token}"
        }

    def get_media_items(self, page_size: int = 25, page_token: Optional[str] = None) -> Response:
        """
        https://developers.google.com/photos/library/reference/rest/v1/mediaItems/list
        """
        media_items_url: str = urljoin(self.api_url, "mediaItems")

        get_media_items_params: Dict[str, str] = {"pageSize": page_size}
        if page_token is not None:
            get_media_items_params["pageToken"] = page_token

        get_media_items_response: Response = requests.get(
            media_items_url,
            headers=self._auth_header,
            params=get_media_items_params
        )
        return get_media_items_response
