from dataclasses import asdict

import pytest

from src.filters import Date, DateFilter, DateRange


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
                [
                    Date(year=2021, month=1, day=1),
                    Date(year=2021, month=2, day=2),
                    Date(year=2021, month=3, day=3),
                    Date(year=2021, month=4, day=4),
                    Date(year=2021, month=5, day=5),
                    Date(year=2021, month=6, day=6),
                ],
                None,
            ),
            (
                None,
                [
                    DateRange(
                        startDate=Date(year=2021, month=1, day=1),
                        endDate=Date(year=2021, month=2, day=2),
                    ),
                    DateRange(
                        startDate=Date(year=2021, month=3, day=3),
                        endDate=Date(year=2021, month=4, day=4),
                    ),
                    DateRange(
                        startDate=Date(year=2021, month=5, day=5),
                        endDate=Date(year=2021, month=6, day=6),
                    ),
                    DateRange(
                        startDate=Date(year=2021, month=7, day=7),
                        endDate=Date(year=2021, month=8, day=8),
                    ),
                    DateRange(
                        startDate=Date(year=2021, month=9, day=9),
                        endDate=Date(year=2021, month=10, day=10),
                    ),
                    DateRange(
                        startDate=Date(year=2021, month=11, day=11),
                        endDate=Date(year=2021, month=12, day=12),
                    ),
                ],
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
                    Date(year=2021, month=1, day=1),
                ],
                None,
                {
                    "dateFilter": {
                        "dates": [{"year": 2021, "month": 1, "day": 1}],
                        "ranges": [],
                    }
                },
            ),
            (
                None,
                [
                    DateRange(
                        startDate=Date(year=2021, month=1, day=1),
                        endDate=Date(year=2021, month=2, day=2),
                    )
                ],
                {
                    "dateFilter": {
                        "dates": [],
                        "ranges": [
                            {
                                "startDate": {"year": 2021, "month": 1, "day": 1},
                                "endDate": {"year": 2021, "month": 2, "day": 2},
                            }
                        ],
                    }
                },
            ),
            (
                [
                    Date(year=2021, month=1, day=1),
                ],
                [
                    DateRange(
                        startDate=Date(year=2021, month=1, day=1),
                        endDate=Date(year=2021, month=2, day=2),
                    )
                ],
                {
                    "dateFilter": {
                        "dates": [{"year": 2021, "month": 1, "day": 1}],
                        "ranges": [
                            {
                                "startDate": {"year": 2021, "month": 1, "day": 1},
                                "endDate": {"year": 2021, "month": 2, "day": 2},
                            }
                        ],
                    }
                },
            ),
        ],
    )
    def test_get_filter(self, dates, date_ranges, expected_filter):
        assert (
            DateFilter(dates=dates, date_ranges=date_ranges).get_filter()
            == expected_filter
        )
