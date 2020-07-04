from dataclasses import dataclass
import sys
import os


class AuthTokens:
    """Class for providing service authentication tokens."""

    def __init__(self):
        self.data = {}

        self.data["twitter_app_key"] = self.get_token("TWITTER_APP_KEY")
        self.data["twitter_app_secret"] = self.get_token("TWITTER_APP_SECRET")

        self.data["twitter_access_token"] = self.get_token("TWITTER_ACCESS_TOKEN")
        self.data["twitter_access_token_secret"] = self.get_token(
            "TWITTER_ACCESS_TOKEN_SECRET"
        )

        self.data["marvel_public_key"] = self.get_token("MARVEL_PUBLIC_KEY")

    def twitter_app_key(self):
        return self.data["twitter_app_key"]

    def twitter_app_secret(self):
        return self.data["twitter_app_secret"]

    def twitter_access_token(self):
        return self.data["twitter_access_token"]

    def twitter_access_token_secret(self):
        return self.data["twitter_access_token_secret"]

    def marvel_public_key(self):
        return self.data["marvel_public_key"]

    def get_token(self, name):
        """Load the GitHub token from the environment."""

        if name in os.environ:
            return os.environ[name]
        else:
            print(f"Please set the environment variable {name}")
            sys.exit(1)
