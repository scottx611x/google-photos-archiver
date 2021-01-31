from dataclasses import asdict

import pytest

from google_photos_archiver.filters import Date, DateFilter, DateRange
from tests.conftest import test_date, test_date_filter, test_date_range


class TestDateFilter:
    @pytest.mark.parametrize(
        "kwargs,expected_dict",
        [
            ({"year": 2021}, {"year": 2021, "month": 0, "day": 0}),
            ({"month": 12}, {"year": 0, "month": 12, "day": 0}),
            ({"day": 1}, {"year": 0, "month": 0, "day": 1}),
            (
                {"year": 2021, "month": 1, "day": 1},
                {"year": 2021, "month": 1, "day": 1},
            ),
        ],
    )
    def test_dates(self, kwargs, expected_dict):
        assert asdict(Date(**kwargs)) == expected_dict

    @pytest.mark.parametrize(
        "kwargs,expected_dict",
        [
            (
                {
                    "startDate": Date(year=2021, month=1, day=1),
                    "endDate": Date(year=2021, month=2, day=2),
                },
                {
                    "startDate": {"year": 2021, "month": 1, "day": 1},
                    "endDate": {"year": 2021, "month": 2, "day": 2},
                },
            )
        ],
    )
    def test_date_ranges(self, kwargs, expected_dict):
        assert asdict(DateRange(**kwargs)) == expected_dict

    @pytest.mark.parametrize(
        "dates,date_ranges",
        [
            (
                [test_date()] * 6,
                None,
            ),
            (
                None,
                [test_date_range()] * 6,
            ),
        ],
    )
    def test_date_and_ranges_invalid_length(self, dates, date_ranges):
        with pytest.raises(RuntimeError, match="A maximum of 5"):
            DateFilter(dates=dates, date_ranges=date_ranges)

    @pytest.mark.parametrize(
        "dates,date_ranges,expected_filter",
        [
            (
                [
                    test_date(),
                ],
                None,
                {
                    "dateFilter": {
                        "dates": [{"year": 2021, "month": 1, "day": 18}],
                        "ranges": [],
                    }
                },
            ),
            (
                None,
                [test_date_range()],
                {
                    "dateFilter": {
                        "dates": [],
                        "ranges": [
                            {
                                "startDate": {"year": 2021, "month": 1, "day": 18},
                                "endDate": {"year": 2021, "month": 1, "day": 19},
                            }
                        ],
                    }
                },
            ),
            (
                [
                    test_date(),
                ],
                [test_date_range()],
                test_date_filter().get_filter(),
            ),
        ],
    )
    def test_get_filter(self, dates, date_ranges, expected_filter):
        assert (
            DateFilter(dates=dates, date_ranges=date_ranges).get_filter()
            == expected_filter
        )
