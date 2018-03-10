This script is used to manage a trail of articles read over time.

# Requirements

Requires a `config.ini` file. Here are sections needed for configuration. While
they aren't **required**, having them defined can enable the max effect for
the tracker.

```
[mysql]
HOST=<host_address>
USERNAME=<username>
PASSWORD=<password>
DB_NAME=<database_name>

[reddit]
BASE_URL = https://oauth.reddit.com
USER_AGENT = <user_agent_name>
USERNAME = <reddit_username>
CLIENT_ID = <reddit_api_client_id>
CLIENT_SECRET = <reddit_api_client_key>
SUB_REDDITS = <sub_reddit1> <sub_reddit2> <sub_reddit3> ...

[hacker_news]
BASE_URL = https://news.ycombinator.com
USER_AGENT = <user_agent_name>
USERNAME = <hacker_news_username>
PASSWORD = <hacker_news_password>
```

# Installation
You'll need `python` with `pip` installed.

Create your virtual environment. I recommend using [virtualenv](https://virtualenv.pypa.io/en/stable/).

Run `pip install -r requirements.txt`.

You're all set.

# Usage
```bash
python main.py [<directory/path/to/config.ini>] # leave blank if config.ini in current directory
```

# Installation with Docker
If you're running Docker, then running this script has gotten even easier.

Run `docker pull sol7117/article-tracker` to pull down the docker container. Make sure that your `config.ini` is in the same directory
as where you pulled down the docker container.

Finally, run `docker run --rm sol7117/article-tracker` to run the tracker. 

## Example use case
<a href='https://errolmarkland.com' target='_blank'>My site</a> (No longer primarily used on my site, as of Nov. 2016. <a href='https://getpocket.com' target='_blank'>Pocket</a> does everything I'd like.)
