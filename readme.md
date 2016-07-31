This script is used to manage a trail of articles read over time.

# Requirements

Requires a `config.ini` file. Below are some sections for configuration:

**MySQL config**
```
[mysql]
host=<host_address>
username=<username>
password=<password>
db_name=<database_name>
```

**Reddit config**
```
[reddit]
BASE_URL = https://oauth.reddit.com
USER_AGENT = <user_agent_name>
USERNAME = <reddit_username>
CLIENT_ID = <reddit_api_client_id>
CLIENT_SECRET = <reddit_api_client_key>
SUB_REDDITS = <sub_reddit1> <sub_reddit2> <sub_reddit3> ...
```

**Hacker News config**
```
[reddit]
BASE_URL = https://news.ycombinator.com
USER_AGENT = <user_agent_name>
USERNAME = <hacker_news_username>
PASSWORD = <hacker_news_password>
```

# Installation
Create your virtual environment. I recommend using [virtualenv](https://virtualenv.pypa.io/en/stable/).

Run `pip install -r requirements.txt`.

You're all set.

# Usage
```bash
python main.py [<directory/path/to/config.ini>] # leave blank if config.ini in current directory
```

## Example use case
<a href='https://www.errolmarkland.com' target='_blank'>My site</a>
