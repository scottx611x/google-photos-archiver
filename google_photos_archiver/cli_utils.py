import re
import time
from pathlib import Path
from typing import Generator, List, Optional, Tuple

import click

from google_photos_archiver.album import Album
from google_photos_archiver.archivers import DiskArchiver
from google_photos_archiver.filters import Date, DateFilter, DateRange
from google_photos_archiver.media_item import MediaItem
from google_photos_archiver.media_item_archiver import MediaItemArchiver
from google_photos_archiver.media_item_recorder import MediaItemRecorder
from google_photos_archiver.rest_client import GooglePhotosApiRestClient


class Timer:
    def __init__(self):
        self.time = None

    def __enter__(self):
        self.time = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.time = time.perf_counter() - self.time


def validate_dates(_, param, value):
    if value is None:
        return value

    if param.human_readable_name == "date_filter":
        regex = re.compile(
            r"(?P<year>\d{4}|\*)"
            r"/"
            r"(?P<month>\d{1,2}|\*)"
            r"/"
            r"(?P<day>\d{1,2}|\*)"
            r",?"
        )
        validation_error_message = (
            f"--date-filter must adhere to the following pattern: {regex.pattern}"
        )
    else:
        regex = re.compile(
            r"(?P<start_year>\d{4})"
            r"/"
            r"(?P<start_month>\d{1,2})"
            r"/"
            r"(?P<start_day>\d{1,2})"
            r"-"
            r"(?P<end_year>\d{4})"
            r"/"
            r"(?P<end_month>\d{1,2})"
            r"/"
            r"(?P<end_day>\d{1,2})"
            r",?"
        )
        validation_error_message = (
            f"--date-range-filter must adhere to the following pattern: {regex.pattern}"
        )

    if re.match(regex, value) is None:
        raise click.BadParameter(
            validation_error_message
            + ". See archive-media-items --help for more details"
        )

    entries = len(value.split(","))
    if entries > 5:
        raise click.BadParameter(
            f"Must provide 5 or less of {param.opts[0]}. Got {entries}"
        )

    return value


def get_date_objects_from_filters(
    date_filter: Optional[str], date_range_filter: Optional[str]
) -> Tuple[List[Date], List[DateRange]]:
    dates: List[Date] = []
    date_ranges: List[DateRange] = []

    if date_filter is not None:
        for date in date_filter.split(","):
            date = date.replace("*", "0")
            date_elements = date.split("/")
            dates.append(
                Date(
                    year=int(date_elements[0]),
                    month=int(date_elements[1]),
                    day=int(date_elements[2]),
                )
            )

    if date_range_filter is not None:
        for date_range in date_range_filter.split(","):
            start_date, end_date = date_range.split("-")
            start_year, start_month, start_day = start_date.split("/")
            end_year, end_month, end_day = end_date.split("/")

            date_ranges.append(
                DateRange(
                    startDate=Date(
                        year=int(start_year),
                        month=int(start_month),
                        day=int(start_day),
                    ),
                    endDate=Date(
                        year=int(end_year),
                        month=int(end_month),
                        day=int(end_day),
                    ),
                )
            )
    return dates, date_ranges


def get_media_items(
    google_photos_api_rest_client: GooglePhotosApiRestClient,
    dates: Optional[List[Date]] = None,
    date_ranges: Optional[List[DateRange]] = None,
    album: Optional[Album] = None,
) -> Generator[MediaItem, None, None]:
    if dates or date_ranges:
        media_items = google_photos_api_rest_client.search_media_items_paginated(
            filters=[DateFilter(dates=dates, date_ranges=date_ranges)],
        )
    elif album is not None:
        media_items = google_photos_api_rest_client.search_media_items_paginated(
            album_id=album.id,
        )
    else:
        media_items = google_photos_api_rest_client.get_media_items_paginated()
    return media_items


def get_media_item_archiver(
    download_path: str,
    max_threadpool_workers: int,
    sqlite_db_path: str,
) -> MediaItemArchiver:
    return MediaItemArchiver(
        archiver=DiskArchiver(
            base_download_path=Path(download_path),
            recorder=MediaItemRecorder(sqlite_db_path=Path(sqlite_db_path)),
        ),
        max_threadpool_workers=max_threadpool_workers,
    )
