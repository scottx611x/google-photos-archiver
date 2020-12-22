from typing import List

from src.media_item import MediaItem


class GooglePhotoDownloader:
    def __init__(self, media_items: List[MediaItem]):
        self.media_items = media_items

    def download(self):
        for media_item in self.media_items:
            print(media_item)
