import pytest
from click.testing import CliRunner

from google_photos_archiver.album import create_album
from google_photos_archiver.cli import cli


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
        (["--albums-only"], "albums_only"),
    ],
)
def test_archive_media_items(
    mocker, google_photos_api_rest_client, test_album_dict, options, option_name
):
    get_media_item_archiver_mock = mocker.patch(
        "google_photos_archiver.cli.get_media_item_archiver"
    )
    get_new_media_item_archivals_mock = mocker.patch(
        "google_photos_archiver.cli.get_new_media_item_archivals"
    )
    get_albums_mock = mocker.patch.object(
        google_photos_api_rest_client,
        "get_albums_paginated",
        return_value=[create_album(test_album_dict)],
    )

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["archive-media-items", *options],
        obj={"google_photos_api_rest_client": google_photos_api_rest_client},
    )

    assert result.exit_code == 0

    if option_name == "date_filters_set":
        assert (
            "Beginning archival of MediaItems from dates=[Date(year=2021, month=1, day=18)]"
            " and date_ranges=[DateRange(startDate=Date(year=2021, month=1, day=18), endDate=Date(year=2021, month=1,"
            " day=19))]" in result.output
        )
    else:
        assert "Beginning archival of MediaItems" in result.output
        assert "from dates" not in result.output

    get_media_item_archiver_mock.assert_called()
    get_new_media_item_archivals_mock.assert_called()

    if option_name == "albums_only":
        get_albums_mock.assert_called_with()
    else:
        get_albums_mock.assert_not_called()
