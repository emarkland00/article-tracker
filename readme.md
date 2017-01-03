This script is used to manage a trail of articles read over time.

# Requirements

Requires a `config.ini` file. Below are some sections for configuration:

**MySQL config**
```
[mysql]
HOST=<host_address>
USERNAME=<username>
PASSWORD=<password>
DB_NAME=<database_name>
```

**Reddit config (optional)**
```
[reddit]
BASE_URL = https://oauth.reddit.com
USER_AGENT = <user_agent_name>
USERNAME = <reddit_username>
CLIENT_ID = <reddit_api_client_id>
CLIENT_SECRET = <reddit_api_client_key>
SUB_REDDITS = <sub_reddit1> <sub_reddit2> <sub_reddit3> ...
```

**Hacker News config (optional)**
```
[hacker_news]
BASE_URL = https://news.ycombinator.com
USER_AGENT = <user_agent_name>
USERNAME = <hacker_news_username>
PASSWORD = <hacker_news_password>
```

# Installation
Create your virtual environment. I recommend using [virtualenv](https://virtualenv.pypa.io/en/stable/).

Run `pip install -r requirements.txt`.

You're all set.

Note: If `lxml` is already installed outside of your virtual environment, then you may get an error message. That is
expected behavior since `pip` doesn't check for packages installed outside the virtual environment.
See [this Stack Overflow answer](https://stackoverflow.com/a/13020013) for more details. A (less than ideal) workaround
would be to [create a symlink from the system's `lxml` to the virtual environment](http://stackoverflow.com/a/21355752)

# Usage
```bash
python main.py [<directory/path/to/config.ini>] # leave blank if config.ini in current directory
```

## Example use case
<a href='https://www.errolmarkland.com' target='_blank'>My site</a> (No longer primarily used on my site, as of Nov. 2016. <a href='https://getpocket.com' target='_blank'>Pocket</a> does everything I'd like. However, I will still keep this going.)
