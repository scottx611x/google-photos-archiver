from pathlib import Path

import click

from google_photos_archiver.cli_utils import (
    Timer,
    get_date_objects_from_filters,
    get_media_item_archiver,
    get_media_items,
    validate_dates,
)
from google_photos_archiver.media_item_archiver import (
    MediaItemArchiver,
    get_new_media_item_archivals,
)
from google_photos_archiver.oauth_handler import GoogleOauthHandler
from google_photos_archiver.rest_client import GooglePhotosApiRestClient


@click.group()
@click.pass_context
@click.option(
    "--client-secret-json-path",
    type=str,
    required=True,
    default="./client_secret.json",
    show_default=True,
    help="`client_secret.json` file acquired from "
    "https://developers.google.com/photos/library/guides/get-started#request-id",
)
@click.option(
    "--refresh-token-path",
    type=str,
    required=False,
    default="./refresh_token",
    show_default=True,
)
def cli(ctx: click.Context, client_secret_json_path: str, refresh_token_path: str):
    ctx.ensure_object(dict)

    if ctx.obj.get("google_photos_api_rest_client") is None:
        ctx.obj["google_photos_api_rest_client"] = GooglePhotosApiRestClient(
            GoogleOauthHandler(Path(client_secret_json_path), Path(refresh_token_path))
        )


@cli.command()
@click.pass_context
@click.option(
    "--download-path",
    type=str,
    default="./downloaded_media",
    show_default=True,
    help="Directory that MediaItems will be archived to",
)
@click.option(
    "--sqlite-db-path", type=str, default="./media_items.db", show_default=True
)
@click.option(
    "--max-threadpool-workers",
    type=int,
    default=100,
    help="The maximum amount of workers to utilize for the ThreadPoolExecutor",
    show_default=True,
)
@click.option(
    "--date-filter",
    type=str,
    callback=validate_dates,
    help="Up to 5 comma delimited Dates conforming to the YYYY/MM/DD pattern."
    " Any of YYYY/MM/DD can be wildcarded (*) like so: "
    "*/MM/DD,YYYY/*/DD,YYYY/MM/*",
)
@click.option(
    "--date-range-filter",
    type=str,
    callback=validate_dates,
    help="Up to 5 comma delimited DateRanges conforming"
    " to the YYYY/MM/DD-YYYY/MM/DD (<start_date>-<end_date>) pattern.",
)
@click.option(
    "--albums-only",
    is_flag=True,
    help="Just target MediaItems that are included in your Albums."
    " MediaItems will be downloaded per usual and symlinked to from directories with each Album's name",
)
# pylint: disable=too-many-arguments,too-many-locals
def archive_media_items(
    ctx: click.Context,
    albums_only: bool,
    date_range_filter: str,
    date_filter: str,
    max_threadpool_workers: int,
    download_path: str,
    sqlite_db_path: str,
):
    with Timer() as timer:
        google_photos_api_rest_client: GooglePhotosApiRestClient = ctx.obj.get(
            "google_photos_api_rest_client"
        )

        dates, date_ranges = get_date_objects_from_filters(
            date_filter, date_range_filter
        )

        _start_message_innards = (
            f" from dates={dates} and date_ranges={date_ranges}"
            if dates != [] or date_ranges != []
            else ""
        )
        start_message = f"Beginning archival of MediaItems" f"{_start_message_innards}"
        click.secho(
            start_message,
            fg="green",
        )

        media_item_archiver: MediaItemArchiver = get_media_item_archiver(
            download_path,
            max_threadpool_workers,
            sqlite_db_path,
        )

        completed_media_item_archivals = []

        if albums_only:
            albums = google_photos_api_rest_client.get_albums_paginated()

            for album in albums:
                if album.title is None:
                    album_title = f"Album ID: {album.id}"
                else:
                    album_title = album.title

                album_path = Path(download_path, "albums", album_title)

                media_items = get_media_items(
                    google_photos_api_rest_client, album=album
                )
                completed_media_item_archivals.extend(
                    media_item_archiver.start(media_items, album_path)
                )

        else:
            media_items = get_media_items(
                google_photos_api_rest_client,
                dates,
                date_ranges,
            )
            completed_media_item_archivals = media_item_archiver.start(media_items)

        new_media_item_archivals = get_new_media_item_archivals(
            completed_media_item_archivals
        )

    click.secho(
        f"Archived {new_media_item_archivals} new MediaItem(s) in {timer.time:0.4f} seconds",
        fg="green",
    )


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
