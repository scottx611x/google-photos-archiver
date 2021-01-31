from pathlib import Path

import click
import pytest

from google_photos_archiver.archivers import DiskArchiver
from google_photos_archiver.cli_utils import (
    Timer,
    get_date_objects_from_filters,
    get_media_item_archiver,
    get_media_items,
    validate_dates,
)
from google_photos_archiver.filters import Date, DateFilter, DateRange
from tests.conftest import test_date, test_date_range


def test_timer(mocker):
    mocker.patch("time.perf_counter", side_effect=[0.0, 5.0])
    with Timer() as timer:
        pass
    assert timer.time == 5.0


class MockParam:
    def __init__(self, name, value):
        self.human_readable_name = name
        self.value = value
        self.opts = [f"--{name.replace('_', '-')}"]


@pytest.mark.parametrize(
    "param,expected_failure",
    [
        (MockParam("date_filter", "2021/1/1"), False),
        (MockParam("date_filter", "2021/1/1,2021/1/1"), False),
        (MockParam("date_filter", "*/1/1"), False),
        (MockParam("date_filter", "2021/*/1"), False),
        (MockParam("date_filter", "2021/1/*"), False),
        (MockParam("date_filter", "2021/1/*,2021/2/*"), False),
        (MockParam("date_filter", "blah"), True),
        (MockParam("date_filter", "2021-1-*"), True),
        (
            MockParam(
                "date_filter", "2021/1/1,2021/1/2,2021/1/3,2021/1/4,2021/1/5,2021/1/6"
            ),
            True,
        ),
        (MockParam("date_range_filter", "2021/1/1-2021/2/1"), False),
        (MockParam("date_range_filter", "blah"), True),
        (MockParam("date_range_filter", "2021-1-1/2021-2-1"), True),
        (
            MockParam(
                "date_range_filter",
                "2021/1/1-2021/2/1,2021/2/1-2021/3/1,2021/3/1-2021/4/1,"
                "2021/4/1-2021/5/1,2021/5/1-2021/6/1,2021/6/1-2021/7/1",
            ),
            True,
        ),
    ],
)
def test_validate_dates(param, expected_failure):
    if expected_failure:
        with pytest.raises(click.BadParameter):
            validate_dates(None, param, param.value)
    else:
        assert validate_dates(None, param, param.value) == param.value


@pytest.mark.parametrize(
    "date_filter,date_range_filter,expected_result",
    [
        (
            "2021/1/*,2021/2/2",
            "2021/1/1-2021/2/1,2021/2/1-2021/3/1",
            (
                [Date(year=2021, month=1, day=0), Date(year=2021, month=2, day=2)],
                [
                    DateRange(
                        startDate=Date(year=2021, month=1, day=1),
                        endDate=Date(year=2021, month=2, day=1),
                    ),
                    DateRange(
                        startDate=Date(year=2021, month=2, day=1),
                        endDate=Date(year=2021, month=3, day=1),
                    ),
                ],
            ),
        ),
    ],
)
def test_get_date_objects_from_filters(date_filter, date_range_filter, expected_result):
    assert (
        get_date_objects_from_filters(date_filter, date_range_filter) == expected_result
    )


@pytest.mark.parametrize(
    "dates,date_ranges,limit,expected_call,expected_call_args",
    [
        ([], [], 10, "get_media_items_paginated", dict(limit=10)),
        (
            [test_date()],
            [],
            10,
            "search_media_items_paginated",
            dict(limit=10, filters=[DateFilter(dates=[test_date()], date_ranges=[])]),
        ),
        (
            [],
            [test_date_range()],
            10,
            "search_media_items_paginated",
            dict(
                limit=10,
                filters=[DateFilter(dates=[], date_ranges=[test_date_range()])],
            ),
        ),
        (
            [test_date()],
            [test_date_range()],
            10,
            "search_media_items_paginated",
            dict(
                limit=10,
                filters=[
                    DateFilter(dates=[test_date()], date_ranges=[test_date_range()])
                ],
            ),
        ),
    ],
)
# pylint: disable=too-many-arguments
def test_get_media_items(
    mocker,
    google_photos_api_rest_client,
    dates,
    date_ranges,
    limit,
    expected_call,
    expected_call_args,
):
    mocked_call = mocker.patch.object(google_photos_api_rest_client, expected_call)
    get_media_items(dates, date_ranges, google_photos_api_rest_client, limit)
    mocked_call.assert_called_with(**expected_call_args)


def test_get_media_item_archiver(
    tmp_path, test_photo_media_item, test_video_media_item
):
    def _media_item_generator():
        for media_item in [test_photo_media_item, test_video_media_item]:
            yield media_item

    download_path = Path(tmp_path, "download")
    sqlite_db_path = Path(tmp_path, "db.sqlite")
    max_threadpool_workers = 1
    media_item_archiver = get_media_item_archiver(
        download_path=download_path,
        max_threadpool_workers=max_threadpool_workers,
        media_items=_media_item_generator(),
        sqlite_db_path=sqlite_db_path,
    )

    assert isinstance(media_item_archiver.archiver, DiskArchiver)
    assert media_item_archiver.archiver.download_path == download_path
    assert media_item_archiver.archiver.recorder.sqlite_db_path == sqlite_db_path
