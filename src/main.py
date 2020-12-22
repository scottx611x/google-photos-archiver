from pathlib import Path

from src.media_item import create_media_item
from src.oauth_handler import GoogleOauthHandler
from src.rest_client import GooglePhotosApiRestClient

if __name__ == "__main__":
    google_photos_api_rest_client = GooglePhotosApiRestClient(
        GoogleOauthHandler(Path("../client_secret.json"), Path("../refresh_token"))
    )
    l = [
        create_media_item(d)
        for d in google_photos_api_rest_client.get_media_items().json()["mediaItems"]
    ]
    print(l)
