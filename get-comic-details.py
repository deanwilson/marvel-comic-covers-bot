#!/usr/bin/env python3
import json
import os.path
import random
import requests
import sqlite3

from authtokens import AuthTokens
from bs4 import BeautifulSoup
from sys import exit

from twython import Twython

MAX_TWEET_LENGTH = 280
MAX_COMIC_ID = 89479  # newest shown via API console on 3rd July 2020


class ComicsData:
    def __init__(self, database):
        self.database = database

    def _db_connect(self):
        try:
            conn = sqlite3.connect(self.database)
        except Exception as e:
            print("Exception thrown: " + str(e))
            exit(1)

        return conn

    def seen(self, comic_id):
        seen = False

        conn = self._db_connect()
        c = conn.cursor()

        c.execute("SELECT * FROM comics WHERE comic_id = '%d'" % comic_id)

        records = c.fetchall()

        conn.close()

        if records:
            print("Has records")  # DEBUG
            seen = True

        return seen

    def record(self, comic_id):
        print(f"In Record with {comic_id}")
        conn = self._db_connect()
        c = conn.cursor()

        try:
            c.execute("INSERT INTO comics (comic_id) VALUES (%d)" % comic_id)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Failed to write {comic_id} to the database")
            exit(1)


def config():
    # TODO: Make this a data class?

    config = {
        "api_endpoint": "https://gateway.marvel.com:443/v1/public",
        "referer": "unixdaemon.net",  # TODO: You will need to change this.
        # All the access tokens live in a file called `authtokens.py`
        "auth": AuthTokens(),
        "database": "comic_covers.db",
    }

    return config


def get_twitter(config):

    handle = Twython(
        config["auth"].twitter_app_key(),
        config["auth"].twitter_app_secret(),
        config["auth"].twitter_access_token(),
        config["auth"].twitter_access_token_secret(),
    )

    return handle


def get_comic(config, comic_id):
    print(f"Getting {comic_id}")
    payload = {
        "apikey": config["auth"].marvel_public_key(),
    }

    headers = {"referer": config["referer"]}

    url = "/".join([config["api_endpoint"], "comics", str(comic_id)])

    print(f"Fetching {comic_id} at {url}")  # DEBUG

    r = requests.get(url, params=payload, headers=headers)

    print(f"Calling {r.url}")

    comic_json = json.loads(r.text)

    return comic_json


def remove_tags(html):
    return BeautifulSoup(html, "lxml").text


def extract_attribution(comic_json):
    """ Provide attribution to the data used.

  Where possible it returns the current attribution text from
  the Marvel API but we provide a default so one is ALWAYS present.
  """

    default = "Data provided by #Marvel. Copyright 2020 MARVEL"

    attribution = comic_json.get("attributionText", default)

    attribution = attribution.replace("Marvel", "#Marvel")

    return attribution


def extract_tweet(comic_json):

    comic_data = {
        "title": comic_json["title"],
        "description": False,
        "creators": [],
    }

    print(f"In extract tweet with {comic_json.get('description')}")

    if comic_json["description"]:
        comic_data["description"] = remove_tags(comic_json["description"])

    comic_data["release_date"] = comic_json["dates"][0]["date"]  # TODO: wrap this!

    roles = {}
    for creator in comic_json["creators"]["items"]:
        role = creator["role"]

        if role in ["writer", "editor"]:
            continue

        if role not in roles:
            roles[role] = []  # TODO: Default dict?

        roles[role].append(creator["name"])

    for role in roles:
        people = ", ".join(roles[role])
        comic_data["creators"].append(f"{role}: {people}")

    return comic_data


def extract_image_url(comic_json):
    image = comic_json["images"][0]

    url = image["path"] + "." + image["extension"]

    return url


def tweet_media(image_url):
    # TODO: There is a problem passing r.content that reading the file
    #       does not trigger. Possible additional binary conversion needed?
    # response = twitter.upload_media(media=r.content)

    r = requests.get(image_url)

    image_file = "/tmp/cover.jpg"
    with open(image_file, "wb") as f:
        f.write(r.content)

    photo = open(image_file, "rb")

    return photo


def choose_comic(comics, config, max_attempts=5):
    current_id = 0
    attempts = 0

    while attempts <= max_attempts:
        attempts += 1
        current_id = random.randint(1, MAX_COMIC_ID)
        print(f"Looking for {current_id}")

        response = get_comic(config, current_id)

        if response["code"] != 200:
            print(f"{current_id} was unsuccessful: {response['status']}")
            continue

        if not comics.seen(current_id):
            print("IN IF")
            # we have our winner
            comics.record(current_id)
            break
    else:
        print("Failed to find any comics")
        exit(1)

    return current_id


if __name__ == "__main__":

    config = config()

    # if we can't track the covers used exit early
    if not os.path.isfile(config["database"]):
        print(f"A database already exists at {config['database']}")
        exit(1)

    comics = ComicsData(config["database"])

    ## override here to test a specific comic
    comic_id = choose_comic(comics, config)
    # comic_id = 70286

    comic = get_comic(config, comic_id)

    issue_data = comic["data"]["results"][0]
    comic_data = extract_tweet(issue_data)
    cover_url = extract_image_url(issue_data)

    attribution = extract_attribution(comic)

    print(f"Modified {attribution}")
    print(f"Original {comic['attributionText']}")

    twitter = get_twitter(config)

    photo = tweet_media(cover_url)

    response = twitter.upload_media(media=photo)

    creators = ""
    if comic_data["creators"]:
        creators = "Creators: " + "\n".join(comic_data["creators"])

    base_size = len(comic_data["title"]) + len(attribution) + 2
    creator_size = len(creators)

    creators_tweet = False
    if base_size + creator_size > MAX_TWEET_LENGTH:
        print(f"Creators will not fit {base_size + creator_size}")
        creators_tweet = True

    # Build the tweet text
    tweet_text = [
        comic_data["title"],
        "\n",
        attribution,
    ]

    if not creators_tweet:
        tweet_text.insert(2, f"{creators}\n")

    # and convert to a string for posting
    status = "\n".join(tweet_text)

    print(f"Attempting to tweet #{status}")

    result = twitter.update_status(status=status, media_ids=[response["media_id"]])
    prev_status = result["id_str"]

    description = comic_data["description"]

    if description:
        print("Tweeting Description")
        description_summary = (
            (description[:276] + "...") if len(description) > MAX_TWEET_LENGTH else description
        )
        result = twitter.update_status(
            status=description_summary, in_reply_to_status_id=prev_status
        )
        prev_status = result["id_str"]

    if creators_tweet:
        result = twitter.update_status(
            status=creators, in_reply_to_status_id=prev_status
        )
