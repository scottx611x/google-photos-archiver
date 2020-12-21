from pathlib import Path

from src.rest_client import GooglePhotosApiRestClient
from src.oauth_handler import GoogleOauthHandler

if __name__ == "__main__":
    google_photos_api_rest_client = GooglePhotosApiRestClient(
        GoogleOauthHandler(Path("../client_secret.json"))
    )
    print(google_photos_api_rest_client.get_media_items().json())
