from src.GooglePhotosRESTClient import GooglePhotosApiRestClient


if __name__ == "__main__":
    google_photos_api_rest_client = GooglePhotosApiRestClient()
    print(google_photos_api_rest_client.get_media_items().json())
