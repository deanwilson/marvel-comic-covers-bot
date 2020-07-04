# Marvel comic covers posting bot
A bot for posting Marvel Comic covers to Twitter

![Marvel Comics Cover Tweet](/marvel-covers-small.png?raw=true "Screenshot a Marvel Comics cover and description")

## Usage instructions

Running this programme requires two main steps:

  * Creating developer accounts and retrieving the credentials

  * Installing and running the code.

The first of these can take much longer and require more patience, phone
verification, and email confirmations than you'd expect.

### Credentials

To run this script you will need both a 
[Marvel Developer API Account](https://developer.marvel.com/)
and a
[Twitter Developer Account](https://developer.twitter.com/en).
Once you have these you should securely store the credentials. To run the script

you will need a `marvel_public_key`, `twitter_app_key`,
`twitter_app_secret`, `twitter_access_token`, and a
`twitter_access_token_secret`. Currently these are exposed as
environment variables and loaded via the `authtokens.py` code.

### Installing dependencies and running the script

This repository uses `Pipenv` to manage the virtual environments and
dependency tracking and installation. All commands should be run from
inside a virtual environment to ensure this program stays isolated.

Once you've installed `Pipenv` you should create the virtual
environment, activate it and install dependencies.

First we get the code:

  * `git clone https://github.com/deanwilson/marvel-comic-covers-bot.git`
  * `cd marvel-comic-covers-bot`

Then we set up the environment:

  * `pipenv shell`   # shell prompt should show the venv
  * `pipenv install` # install the dependencies listed in `Pipfile`

Now we create the SQLite state database. By prefixing the command with
`pipenv run` we ensure the script is run with the dependencies available.

  * `pipenv run python3 tools/create-database.py`
  * `ls -ahl comic_covers.db` # Confirm it exists

Now add the credentials to your running environment. You created these
in the *Credentials* step above.

    export TWITTER_APP_KEY="REPLACE_ME_WITH_YOUR_SECRET_KEY"
    export TWITTER_APP_SECRET="REPLACE_ME_WITH_YOUR_SECRET_KEY"

    export TWITTER_ACCESS_TOKEN="REPLACE_ME_WITH_YOUR_SECRET_KEY"
    export TWITTER_ACCESS_TOKEN_SECRET="REPLACE_ME_WITH_YOUR_SECRET_KEY"

    export MARVEL_PUBLIC_KEY="REPLACE_ME_WITH_YOUR_SECRET_KEY"

You can now run the actual worker script to fetch an unseen comic cover
from the Marvel API and post it on twitter.

    pipenv run python3 get-comic-details.py

If everything is working you will see some run time information as the
script attempts to locate a new comic cover and then post it to twitter.

### Author

 * [Dean Wilson](https://www.unixdaemon.net)
