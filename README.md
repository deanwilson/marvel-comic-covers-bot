# Marvel comic covers posting bot
A bot for posting Marvel Comic covers to Twitter

![Marvel Comics Cover Tweet](/marvel-covers-small.png?raw=true "Screenshot a Marvel Comics cover and description")

## Usage instructions

### Credentials

To run this script you will need both a 
[Marvel Developer API Account](https://developer.marvel.com/)
and a
[Twitter Developer Account](https://developer.twitter.com/en).
Once you have these you should securely store the credentials from each
as you will need a `marvel_public_key`, `twitter_app_key`,
`twitter_app_secret`, `twitter_access_token`, and a
`twitter_access_token_secret` for this programme to run. Currently these
are exposed as environment variables and loaded via the `authtokens.py` code.

### Running the code

Before you can run the `get-comic-details.py` script to fetch a comic
and post it to Twitter you need to create the scripts state file, a
small SQLite database, by running `tools/create-database.py`. This
creates a single table that will track the posted comic IDs to avoid
duplication in the twitter feed.

### Author

 * [Dean Wilson](https://www.unixdaemon.net)
