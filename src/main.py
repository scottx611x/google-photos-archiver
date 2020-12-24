from pathlib import Path

from src.archivers import DiskArchiver
from src.media_item_archiver import MediaItemArchiver
from src.oauth_handler import GoogleOauthHandler
from src.rest_client import GooglePhotosApiRestClient

if __name__ == "__main__":
    google_photos_api_rest_client = GooglePhotosApiRestClient(
        GoogleOauthHandler(Path("../client_secret.json"), Path("../refresh_token"))
    )

    MediaItemArchiver(
        media_items=google_photos_api_rest_client.get_media_items_paginated(limit=20),
        archiver=DiskArchiver(download_path=Path("../downloaded_media")),
    ).start()
