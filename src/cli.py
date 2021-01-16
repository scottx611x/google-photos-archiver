import time
from pathlib import Path

import click

from src.archivers import DiskArchiver
from src.filters import Date, DateFilter
from src.media_item_archiver import MediaItemArchiver, get_new_media_item_archivals
from src.media_item_recorder import MediaItemRecorder
from src.oauth_handler import GoogleOauthHandler
from src.rest_client import GooglePhotosApiRestClient


@click.group()
@click.pass_context
@click.option(
    "--client-secret-json-path",
    type=str,
    required=True,
    default="../client_secret.json",
    help="`client_secret.json` file acquired from "
    "https://developers.google.com/photos/library/guides/get-started#request-id",
)
@click.option(
    "--refresh-token-path",
    type=str,
    required=False,
    default="../refresh_token",
)
def cli(ctx: click.Context, client_secret_json_path: str, refresh_token_path: str):
    ctx.ensure_object(dict)

    if ctx.obj.get("google_photos_api_rest_client") is None:
        ctx.obj["google_photos_api_rest_client"] = GooglePhotosApiRestClient(
            GoogleOauthHandler(Path(client_secret_json_path), Path(refresh_token_path))
        )


@cli.command()
@click.pass_context
@click.option("--download-path", type=str, default="../downloaded_media")
@click.option(
    "--sqlite-db-path",
    type=str,
    default="../media_items.db",
)
@click.option(
    "--max-threadpool-workers",
    type=int,
    default=100,
    help="The maximiumum amount of workers to utilize for the ThreadPoolExecutor",
)
def archive_media_items(
    ctx: click.Context,
    max_threadpool_workers: int,
    download_path: str,
    sqlite_db_path: str,
):
    google_photos_api_rest_client: GooglePhotosApiRestClient = ctx.obj.get(
        "google_photos_api_rest_client"
    )

    start = time.perf_counter()

    completed_media_item_archivals = MediaItemArchiver(
        archiver=DiskArchiver(
            download_path=Path(download_path),
            recorder=MediaItemRecorder(sqlite_db_path=Path(sqlite_db_path)),
        ),
        # media_items=google_photos_api_rest_client.get_media_items_paginated(limit=200),
        media_items=google_photos_api_rest_client.search_media_items_paginated(
            limit=200, filters=[DateFilter(dates=[Date(year=2021, month=2)])]
        ),
        max_threadpool_workers=max_threadpool_workers,
    ).start()

    end = time.perf_counter()

    new_media_item_archivals = get_new_media_item_archivals(
        completed_media_item_archivals
    )

    click.secho(
        f"Archived {new_media_item_archivals} new MediaItem(s) in {end - start:0.4f} seconds",
        fg="green",
    )


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
