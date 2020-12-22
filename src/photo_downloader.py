from typing import List

import requests

from src.media_item import MediaItem, VideoMediaMetadata, VideoProcessingStatus


class GooglePhotoDownloader:
    def __init__(self, media_items: List[MediaItem]):
        self.media_items = media_items

    def download(self):
        for media_item in self.media_items:

            if isinstance(media_item.mediaMetadata, VideoMediaMetadata):
                if media_item.mediaMetadata.video.status != VideoProcessingStatus.READY:
                    continue

            response: requests.Response = requests.get(
                media_item.downloadUrl, stream=True
            )
            response.raise_for_status()

            self._write_to_disk(media_item, response)

    def _write_to_disk(self, media_item: MediaItem, response: requests.Response):
        with open(media_item.filename, "wb") as f:
            f.write(response.raw.data)
