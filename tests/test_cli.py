import pytest
from click.testing import CliRunner

from src.cli import cli


@pytest.mark.parametrize(
    "options,option_name",
    [
        (
            [
                "--date-filter",
                "2021/1/18",
                "--date-range-filter",
                "2021/1/18-2021/1/19",
            ],
            "date_filters_set",
        ),
        ([], "no_options_set"),
    ],
)
def test_archive_media_items(
    mocker, google_photos_api_rest_client, options, option_name
):
    get_media_item_archiver_mock = mocker.patch("src.cli.get_media_item_archiver")
    get_new_media_item_archivals_mock = mocker.patch(
        "src.cli.get_new_media_item_archivals"
    )

    max_media_items = 10

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["archive-media-items", "--max-media-items", max_media_items, *options],
        obj={"google_photos_api_rest_client": google_photos_api_rest_client},
    )

    assert result.exit_code == 0

    if option_name == "date_filters_set":
        assert (
            f"Beginning archival of up to {max_media_items} MediaItem(s) from dates=[Date(year=2021, month=1, day=18)]"
            f" and date_ranges=[DateRange(startDate=Date(year=2021, month=1, day=18), endDate=Date(year=2021, month=1,"
            f" day=19))]" in result.output
        )
    else:
        assert (
            f"Beginning archival of up to {max_media_items} MediaItem(s)"
            in result.output
        )

    get_media_item_archiver_mock.assert_called()
    get_new_media_item_archivals_mock.assert_called()
