This script is used to manage a trail of articles read over time.



# Requirements

Requires a config.ini file. Below are some sections for configuration

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
```

# Usage
```bash
python main.py [<directory/path/to/config.ini>] # leave blank if config.ini is in the same directory as main.py
```
