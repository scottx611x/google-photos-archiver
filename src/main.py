from pathlib import Path
from typing import List

from src.media_item import MediaItem, create_media_item
from src.oauth_handler import GoogleOauthHandler
from src.photo_downloader import GooglePhotoDownloader
from src.rest_client import GooglePhotosApiRestClient

if __name__ == "__main__":
    google_photos_api_rest_client = GooglePhotosApiRestClient(
        GoogleOauthHandler(Path("../client_secret.json"), Path("../refresh_token"))
    )
    media_items: List[MediaItem] = [
        create_media_item(d)
        for d in google_photos_api_rest_client.get_media_items(page_size=5).json()[
            "mediaItems"
        ]
    ]
    GooglePhotoDownloader(media_items).download()
