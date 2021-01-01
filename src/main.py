import logging
import time
from pathlib import Path

from src.archivers import DiskArchiver
from src.media_item_archiver import MediaItemArchiver, get_new_media_item_archivals
from src.media_item_recorder import MediaItemRecorder
from src.oauth_handler import GoogleOauthHandler
from src.rest_client import GooglePhotosApiRestClient

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    google_photos_api_rest_client = GooglePhotosApiRestClient(
        GoogleOauthHandler(Path("../client_secret.json"), Path("../refresh_token"))
    )

    start = time.perf_counter()

    completed_media_item_archivals = MediaItemArchiver(
        archiver=DiskArchiver(
            download_path=Path("../downloaded_media"),
            recorder=MediaItemRecorder(sqlite_db_path=Path("../media_items.db")),
        ),
        media_items=google_photos_api_rest_client.get_media_items_paginated(limit=200),
        max_threadpool_workers=100,
    ).start()

    end = time.perf_counter()

    new_media_item_archivals = get_new_media_item_archivals(
        completed_media_item_archivals
    )

    logger.info(
        "Archived %d new MediaItem(s) in %s",
        new_media_item_archivals,
        f"{end - start:0.4f} seconds",
    )
