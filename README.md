# google-photos-archiver
[![CircleCI](https://circleci.com/gh/scottx611x/google-photos-archiver.svg?style=svg&circle-token=54dbe16b5fd34bb8c3a646a479b75f640e1c18b5)](https://circleci.com/gh/scottx611x/google-photos-archiver/tree/main)
[![codecov](https://codecov.io/gh/scottx611x/google-photos-archiver/branch/main/graph/badge.svg?token=KGmF8LIaY4)](https://codecov.io/gh/scottx611x/google-photos-archiver)

## What
`google-photos-archiver` aims to provide a simple, fast, extensible interface to be able to back up one's Google Photos to a location of their choosing.

I've drawn inspiration from projects such as: https://github.com/mholt/timeliner & https://github.com/gilesknap/gphotos-sync but wanted to cut my teeth in this domain and see what I could come up with myself.

## Why

I wanted a tool (of my own creation) that I could run on my Pi Zero which would provide a copy of mine and my partner's Google Photos libraries.

But in all seriousness, I've mainly just needed a distraction from the vicious cycle of wake, work, Netflix, sleep, and I thought it was high time to do a little side project.

## How

### Pre-reqs

- `docker`

... Or

- `python==3.8`
- [poetry](https://python-poetry.org/docs/#installation) `>=1.0.0`

#### Development Reqs
- [pre-commit](https://pre-commit.com/#install)
  - Run `pre-commit install`

### Getting Started

```
$ poetry install
$ poetry run google-photos-archiver
Usage: google-photos-archiver [OPTIONS] COMMAND [ARGS]...

Options:
  --client-secret-json-path TEXT  `client_secret.json` file acquired from http
                                  s://developers.google.com/photos/library/gui
                                  des/get-started#request-id  [default:
                                  ./client_secret.json; required]

  --refresh-token-path TEXT       [default: ./refresh_token]
  --help                          Show this message and exit.

Commands:
  archive-media-items
```

#### ... with Docker
```
$ docker build . -t google-photos-archiver
$ docker run google-photos-archiver
Usage: google-photos-archiver [OPTIONS] COMMAND [ARGS]...

Options:
  --client-secret-json-path TEXT  `client_secret.json` file acquired from http
                                  s://developers.google.com/photos/library/gui
                                  des/get-started#request-id  [default:
                                  ./client_secret.json; required]

  --refresh-token-path TEXT       [default: ./refresh_token]
  --help                          Show this message and exit.

Commands:
  archive-media-items
```

#### Running tests
```
$ poetry run pytest
```