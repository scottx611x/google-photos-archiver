import sqlite3
from pathlib import Path

from google_photos_archiver.media_item import MediaItem


class MediaItemRecorder:
    """
    Persists MediaItem ids to a sqlite db
    """

    def __init__(self, sqlite_db_path: Path):
        self.sqlite_db_path = sqlite_db_path

        with self.connection as _connection:
            _connection.execute(
                """CREATE TABLE IF NOT EXISTS media_items (media_item_id varchar unique primary key)"""
            )

    @property
    def connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.sqlite_db_path)

    def add(self, media_item: MediaItem):
        with self.connection as _connection:
            _connection.execute(
                "INSERT INTO media_items(media_item_id) values (?)", (media_item.id,)
            )

    def lookup(self, media_item: MediaItem) -> bool:
        with self.connection as _connection:
            media_item = _connection.execute(
                "SELECT * FROM media_items WHERE media_item_id = '%s'" % media_item.id
            ).fetchone()

        return media_item is not None
