from pathlib import Path

from src.GooglePhotosRESTClient import GooglePhotosApiRestClient


if __name__ == "__main__":
    google_photos_api_rest_client = GooglePhotosApiRestClient(Path("../client_secret.json"))
