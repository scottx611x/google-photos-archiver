import logging
import sys
from typing import Callable, Dict, Generator, Optional
from urllib.parse import urljoin

import requests
from requests import Response

from src.media_item import MediaItem, create_media_item
from src.oauth_handler import GoogleOauthHandler

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


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

        logger.info("Fetching %d MediaItems with page_token: %s", page_size, page_token)

        media_items_url: str = urljoin(self.api_url, "mediaItems")

        get_media_items_params: Dict[str, str] = {"pageSize": page_size}
        if page_token is not None:
            get_media_items_params["pageToken"] = page_token

        get_media_items_response: Response = requests.get(
            media_items_url, headers=self._auth_header, params=get_media_items_params
        )
        get_media_items_response.raise_for_status()
        return get_media_items_response

    def get_media_items_paginated(
        self, limit: Optional[int] = None
    ) -> Generator[MediaItem, None, None]:
        logger.info(
            "Fetching %s MediaItems", str(limit) if limit is not None else "all"
        )

        count = 0
        next_page_token = ""

        while next_page_token is not None:
            media_items_dict = self.get_media_items(
                page_size=100,
                page_token=None if next_page_token == "" else next_page_token,
            ).json()
            next_page_token = media_items_dict.get("nextPageToken")

            for media_item in media_items_dict["mediaItems"]:
                yield create_media_item(media_item)
                count += 1
                if count == limit:
                    return
