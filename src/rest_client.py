from typing import Callable, Dict, Optional
from urllib.parse import urljoin

import requests
from requests import Response

from src.oauth_handler import GoogleOauthHandler


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


@for_all_methods(handle_request_errors)
class GooglePhotosApiRestClient:
    """
    Helper class for easily interacting with the Google Photos API REST interface
    Refer to: https://developers.google.com/photos/library/guides/get-started
    """

    def __init__(
        self,
        oauth_handler: GoogleOauthHandler,
        api_url: str = "https://photoslibrary.googleapis.com/v1/",
    ):
        self.oauth_handler = oauth_handler

        self.api_url = api_url
        self._auth_header: Dict[str, str] = {
            "Authorization": f"Bearer {self.oauth_handler.token}"
        }

    def get_media_items(
        self, page_size: int = 25, page_token: Optional[str] = None
    ) -> Response:
        """
        https://developers.google.com/photos/library/reference/rest/v1/mediaItems/list
        """
        media_items_url: str = urljoin(self.api_url, "mediaItems")

        get_media_items_params: Dict[str, str] = {"pageSize": page_size}
        if page_token is not None:
            get_media_items_params["pageToken"] = page_token

        get_media_items_response: Response = requests.get(
            media_items_url, headers=self._auth_header, params=get_media_items_params
        )
        get_media_items_response.raise_for_status()
        return get_media_items_response
