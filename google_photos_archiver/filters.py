from dataclasses import asdict, dataclass
from typing import Dict, List


class Filter:
    def get_filter(self) -> Dict:
        raise NotImplementedError("Subclasses of Filter must implement `get_filter`")


@dataclass
class Date:
    year: int = 0
    month: int = 0
    day: int = 0

    def __eq__(self, other: "Date"):
        return all(
            [self.year == other.year, self.month == other.month, self.day == other.day]
        )


@dataclass
# pylint: disable=invalid-name
class DateRange:
    startDate: Date
    endDate: Date

    def __eq__(self, other: "DateRange"):
        return all([self.startDate == other.startDate, self.endDate == other.endDate])


class DateFilter(Filter):
    def __init__(self, dates: List[Date] = None, date_ranges: List[DateRange] = None):
        if dates is None:
            dates = []

        if date_ranges is None:
            date_ranges = []

        if len(dates) > 5:
            raise RuntimeError("A maximum of 5 Dates can be included per request.")

        if len(date_ranges) > 5:
            raise RuntimeError("A maximum of 5 DateRanges can be included per request.")

        self.dates = dates
        self.date_ranges = date_ranges

    def __eq__(self, other: "DateFilter"):
        return all([self.dates == other.dates, self.date_ranges == other.date_ranges])

    def get_filter(self) -> Dict:
        return {
            "dateFilter": {
                "dates": [asdict(date) for date in self.dates],
                "ranges": [asdict(date_range) for date_range in self.date_ranges],
            }
        }
