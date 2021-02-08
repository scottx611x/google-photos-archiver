# google-photos-archiver
[![CircleCI](https://circleci.com/gh/scottx611x/google-photos-archiver.svg?style=svg&circle-token=54dbe16b5fd34bb8c3a646a479b75f640e1c18b5)](https://circleci.com/gh/scottx611x/google-photos-archiver/tree/main)
[![codecov](https://codecov.io/gh/scottx611x/google-photos-archiver/branch/main/graph/badge.svg?token=KGmF8LIaY4)](https://codecov.io/gh/scottx611x/google-photos-archiver)
[![PyPI version](https://badge.fury.io/py/google-photos-archiver.svg)](https://badge.fury.io/py/google-photos-archiver)

* [What?](#what)
* [Why?](#why)
* [How?](#how)
* [Development Pre\-reqs](#development-pre-reqs)
  * [Optional Reqs](#optional-reqs)
* [Getting Started](#getting-started)
  * [Google Oauth Setup](#google-oauth-setup)
  * [First Run](#first-run)
  * [Development Usage](#development-usage)
  * [\.\.\. with Docker](#-with-docker)
  * [General Usage](#general-usage)
  * [Running tests](#running-tests)
* [Examples](#examples)
  * [Specify a different download location](#specify-a-different-download-location)
  * [Download from specific dates (with wildcard support)](#download-from-specific-dates-with-wildcard-support)
  * [\-\-help](#--help)
  * [archive\-media\-items \-\-help](#archive-media-items---help)
  * [Download Path Hierarchy](#download-path-hierarchy)

[comment]: <> (Created with https://github.com/ekalinin/github-markdown-toc.go)
[comment]: <> (brew install github-markdown-toc && cat ./README.md | gh-md-toc)

## What?
`google-photos-archiver` aims to provide a simple, fast, extensible interface to be able to back up one's Google Photos to a location of their choosing.

I've drawn inspiration from projects such as: https://github.com/mholt/timeliner & https://github.com/gilesknap/gphotos-sync but wanted to cut my teeth in this domain and see what I could come up with myself.

## Why?

I wanted a tool (of my own creation) which could easily provide a copy of mine and my partner's Google Photos libraries, and keep said copy up to date over time.

In reality I've mainly just needed a distraction from the vicious cycle of wake, work, Netflix, sleep, and I thought it was high time to do a little side project.

## How?

### Development Pre-reqs

- `docker`

... Or

- `python==3.8`
- [poetry](https://python-poetry.org/docs/#installation) `>=1.0.0`

#### Optional Reqs
- [pre-commit](https://pre-commit.com/#install)
  - Run `pre-commit install`

### Getting Started

#### Google Oauth Setup
These instructions will help you set up Google OAuth2 client credentials so you can start using `google-photos-archiver`

- While logged into your Google account navigate to [Create a New Project](https://console.developers.google.com/projectcreate)
- Create one, and switch to using it with the UI dropdown
- Navigate to `APIs & Services` click on `+ Enable APIs and services`, and enable the `Photos Library API`
- Navigate back to `APIs & Services` and click on `Credentials`
- Click on `+ Create Credentials > OAuth client ID`
- Configure an OAuth consent screen. You can just fill out the required fields and hit Save.
  - Click `Add Or Remove Scopes` and manually add scope: `https://www.googleapis.com/auth/photoslibrary.readonly`
  - Accept remaining defaults, save through and return to `Credentials`
- Click on `+ Create Credentials > OAuth client ID`
- Make a `"Desktop App"`
- Congrats!, you now have a Client ID and Client Secret
- Download the associated `client_secret.json` file and make note of its location as we'll be providing it's path to `google-photos-archiver`

#### First Run
A browser window will be opened during the initial OAuth flow. After successfully authenticating once, a refresh token will be stored for future use (See: `--refresh-token-path`) and will omit the need to reauthenticate.

#### Development Usage
```
$ git clone git@github.com:scottx611x/google-photos-archiver.git
$ poetry install
$ poetry run google-photos-archiver --help
```

#### ... with Docker

> Note that some more Docker volume mounting will be warranted here if you want to specify a different path to download to etc.
> Ref: https://docs.docker.com/storage/volumes

```
$ docker build . -t google-photos-archiver
$ docker run -v $PWD:/app/ google-photos-archiver  --help
```

#### General Usage

```
$ pip install google-photos-archiver
$ google-photos-archiver --help
```

#### Running tests
```
$ poetry run pytest
```

### Examples

#### Specify a different download location
```
$ google-photos-archiver archive-media-items --download-path /Volumes/my-big-hdd/downloaded_media
```

#### Download from specific dates (with wildcard support)
```
$ google-photos-archiver archive-media-items --date-filter 2020/*/*,2021/8/22
$ google-photos-archiver archive-media-items --date-range-filter 2019/8/22-2020/8/22
```

#### Download Albums and their MediaItems only
```
$ google-photos-archiver archive-media-items --albums-only
```

#### Download Path Hierarchy
```
$ tree /<download_path>/downloaded_media/ | head
/<download_path>/downloaded_media/
├── 2021
│ └── 1
│     ├── 1
│     │ └── a.jpg
│     └── 2
│         └── b.mov
├── 2020
│ ├── 1
│ │ └── 2
│ │     └── c.jpg
│ └── 2
│     └── 3
│         └── d.jpg
└── albums
    └── Album A
        └── <symlink /<download_path>/downloaded_media/2021/1/1/a.jpg >
...
```
