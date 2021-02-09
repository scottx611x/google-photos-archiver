import logging
from enum import Enum
from typing import Any, Callable, Dict, Generator, List, Optional, Union
from urllib.parse import urljoin

import requests
from requests import Response

from google_photos_archiver.album import Album, create_album
from google_photos_archiver.filters import Filter
from google_photos_archiver.media_item import MediaItem, create_media_item
from google_photos_archiver.oauth_handler import GoogleOauthHandler

logger = logging.getLogger(__name__)


def handle_request_errors(decorated_function: Callable):
    """
    Decorator that handles for potential requests library errors that may occur when calling the wrapped function
    """

    def wrapper(self, *args, **kwargs):
        try:
            return decorated_function(self, *args, **kwargs)
        except requests.RequestException as err:
            error_message = None

            error_response_json = err.response.json()
            error_content = error_response_json.get("error")

            if error_content is not None:
                error_message = error_content.get("message")

            raise GooglePhotosApiRestClientError(
                f"Failed to execute: `{decorated_function.__name__}` {err}" + ""
                if error_message is None
                else " \n" + error_message
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


def create_album_or_media_item(
    album_or_media_item: Dict[str, Any]
) -> Union[Album, MediaItem]:
    try:
        return create_media_item(album_or_media_item)
    except (KeyError, TypeError):
        try:
            return create_album(album_or_media_item)
        except Exception as err:
            raise GooglePhotosApiRestClientError(
                f"Unable to `create_album_or_media_item` from {album_or_media_item}"
            ) from err


class PaginationResponseKey(Enum):
    Albums = "albums"
    MediaItems = "mediaItems"


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

    def _paginate(
        self,
        operation: Callable,
        response_key: PaginationResponseKey,
        page_size: int = 100,
        **kwargs,
    ) -> Generator[Union[Album, MediaItem], None, None]:
        next_page_token = ""

        while next_page_token is not None:
            response: Response = operation(
                page_size=page_size,
                page_token=None if next_page_token == "" else next_page_token,
                **kwargs,
            )
            response_data = response.json()
            next_page_token = response_data.get("nextPageToken")

            for album_or_media_item in response_data.get(response_key.value, []):
                yield create_album_or_media_item(album_or_media_item)

    def get_albums(
        self, page_size: int = 50, page_token: Optional[str] = None
    ) -> Response:
        """
        https://developers.google.com/photos/library/reference/rest/v1/albums/list
        """

        logger.info(
            "Fetching up to %d Albums with page_token: %s", page_size, page_token
        )

        albums_url: str = urljoin(self.api_url, "albums")

        get_albums_params: Dict[str, str] = {"pageSize": page_size}
        if page_token is not None:
            get_albums_params["pageToken"] = page_token

        get_albums_response: Response = requests.get(
            albums_url, headers=self._auth_header, params=get_albums_params
        )
        get_albums_response.raise_for_status()
        return get_albums_response

    def get_albums_paginated(self) -> Generator[Album, None, None]:
        logger.info("Fetching all Albums")
        return self._paginate(
            self.get_albums, PaginationResponseKey.Albums, page_size=50
        )

    def get_media_items(
        self, page_size: int = 25, page_token: Optional[str] = None
    ) -> Response:
        """
        https://developers.google.com/photos/library/reference/rest/v1/mediaItems/list
        """

        logger.info(
            "Fetching up to %d MediaItems with page_token: %s", page_size, page_token
        )

        media_items_url: str = urljoin(self.api_url, "mediaItems")

        get_media_items_params: Dict[str, str] = {"pageSize": page_size}
        if page_token is not None:
            get_media_items_params["pageToken"] = page_token

        get_media_items_response: Response = requests.get(
            media_items_url, headers=self._auth_header, params=get_media_items_params
        )
        get_media_items_response.raise_for_status()
        return get_media_items_response

    def get_media_items_paginated(self) -> Generator[MediaItem, None, None]:
        logger.info("Fetching MediaItems")
        return self._paginate(self.get_media_items, PaginationResponseKey.MediaItems)

    def search_media_items(
        self,
        page_size: int = 100,
        page_token: Optional[str] = None,
        filters: Optional[List[Filter]] = None,
        album_id: Optional[int] = None,
    ):
        """
        https://developers.google.com/photos/library/reference/rest/v1/mediaItems/search
        """
        logger.info(
            "Searching for MediaItems: filters: %s, album_id: %s", filters, album_id
        )

        search_media_items_url: str = urljoin(self.api_url, "mediaItems") + ":search"

        search_media_items_body: Dict[str, Any] = {"pageSize": page_size}

        if album_id is not None:
            search_media_items_body["albumId"] = album_id

        if page_token is not None:
            search_media_items_body["pageToken"] = page_token

        if filters is not None:
            search_media_items_body["filters"] = {
                k: v for f in filters for k, v in f.get_filter().items()
            }

        search_media_items_response: Response = requests.post(
            search_media_items_url,
            headers=self._auth_header,
            params={"alt": "json"},
            json=search_media_items_body,
        )
        search_media_items_response.raise_for_status()
        return search_media_items_response

    def search_media_items_paginated(
        self,
        filters: Optional[List[Filter]] = None,
        album_id: Optional[str] = None,
    ) -> Generator[MediaItem, None, None]:
        if album_id is not None:
            return self._paginate(
                self.search_media_items,
                PaginationResponseKey.MediaItems,
                album_id=album_id,
            )

        return self._paginate(
            self.search_media_items,
            PaginationResponseKey.MediaItems,
            filters=filters,
        )
