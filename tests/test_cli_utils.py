import click
import pytest

from src.cli_utils import Timer, validate_dates


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


def test_get_date_objects_from_filters():
    pass


def test_get_media_items():
    pass


def test_get_media_item_archiver():
    pass
