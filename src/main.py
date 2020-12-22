from pathlib import Path

from src.oauth_handler import GoogleOauthHandler
from src.photo_downloader import GooglePhotoDownloader
from src.rest_client import GooglePhotosApiRestClient

if __name__ == "__main__":
    google_photos_api_rest_client = GooglePhotosApiRestClient(
        GoogleOauthHandler(Path("../client_secret.json"), Path("../refresh_token"))
    )

    GooglePhotoDownloader(
        google_photos_api_rest_client.get_media_items_paginated(limit=101),
        Path("../downloaded_media"),
    ).download()
