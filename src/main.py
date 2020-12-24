import logging
import time
from pathlib import Path

from src.archivers import DiskArchiver
from src.media_item_archiver import MediaItemArchiver
from src.oauth_handler import GoogleOauthHandler
from src.rest_client import GooglePhotosApiRestClient

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    google_photos_api_rest_client = GooglePhotosApiRestClient(
        GoogleOauthHandler(Path("../client_secret.json"), Path("../refresh_token"))
    )

    start = time.perf_counter()

    completed_media_item_archivals = MediaItemArchiver(
        archiver=DiskArchiver(download_path=Path("../downloaded_media")),
        media_items=google_photos_api_rest_client.get_media_items_paginated(),
        max_threadpool_workers=50,
    ).start()

    end = time.perf_counter()
    logger.info(
        "Archived %d MediaItems in %s",
        len(list(completed_media_item_archivals)),
        f"{end - start:0.4f} seconds",
    )
