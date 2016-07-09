import requests
from requests.auth import HTTPBasicAuth
from config import ConfigClass
from datetime import datetime, timedelta
from mysql import Article
import os.path

class RedditClientError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class RedditClient:
    def __init__(self):
        reddit_config = ConfigClass().get_reddit_config()
        if not reddit_config:
            print "Missing reddit config. Unable to fetch content from reddit."
            return
            
        self.base_url = reddit_config.base_url
        self.user_agent = reddit_config.user_agent
        self.username = reddit_config.username
        self.client_id = reddit_config.client_id
        self.client_secret = reddit_config.client_secret
        self.access_token = self.fetch_access_token()

    def get_liked_posts(self):
        url = '{1}/user/{0}/liked/.json'.format(self.username, self.base_url)
        headers = { 'User-Agent': self.user_agent, 'Authorization': 'bearer ' + self.access_token }
        req = requests.get(url, headers=headers)
        json = req.json();
        return RedditPostListing(json['data'])

    def fetch_access_token(self):
        filename = 'reddit_access_token'
        access_token = self.fetch_access_token_from_file(filename)
        if access_token is not None:
            return access_token

        r = self.fetch_access_token_from_url()
        access_token = r[0]
        exp_time = r[1]

        with open(filename, 'w') as f:
            f.write(access_token + '|' + str(exp_time))

        return access_token

    def fetch_access_token_from_file(self, path):
        if not os.path.isfile(path):
            return None

        with open(path, 'r') as f:
            content = f.read().split('|')
            if len(content) is not 2:
                return None

            access_token = content[0]
            exp_timestamp = datetime.strptime(content[1], '%Y-%m-%d %H:%M:%S.%f')
            if exp_timestamp < datetime.now():
                return None

            return access_token

    def fetch_access_token_from_url(self):
        auth_url = 'https://www.reddit.com/api/v1/access_token'
        req = requests.post(auth_url,
                      auth=HTTPBasicAuth(self.client_id, self.client_secret),
                      headers={'User-Agent': self.user_agent},
                      data={'grant_type':'client_credentials'})

        json = req.json()
        access_token = json["access_token"]
        expires = json["expires_in"]
        exp_time = datetime.now() + timedelta(seconds=expires)
        return (access_token, exp_time)

class RedditPostDetails:
    def __init__(self, json):
        self.id = json['id']
        self.subreddit = json['subreddit']
        self.title = json['title']
        self.domain = json['domain']
        self.author = json['author']
        self.created_utc = json['created_utc']
        self.selftext_html = json['selftext_html']
        self.selftext = json['selftext']
        self.url = json['url']
        self.timestamp = datetime.now()

    def is_self_article(self):
        return self.selftext == None

class RedditPost:
    def __init__(self, json):
        self.raw = json
        self.kind = json['kind']
        self.data = RedditPostDetails(json['data'])

    def to_article(self):
        return { 'article_key': self.data.id, 'name': self.data.title, 'url': self.data.url, 'source': 'reddit', 'timestamp': self.data.timestamp }

class RedditPostListing:
    def __init__(self, json):
        self.raw = json
        self.modhash = json['modhash']
        self.raw_children = [RedditPost(j) for j in json['children']]
        self.children = self.raw_children

    def filter_by_new_listings(self):
        keys = [c.data.id for c in self.children]
        results = Article.select().where(Article.article_key << keys)
        existing_keys = [r.article_key for r in results]
        self.children = [c for c in self.children if c.data.id not in existing_keys]
        return self

    def filter_by_subreddit(self, *subreddits):
        return RedditFilter.by_subreddit(self.children, subreddits)

    def filter_by_author(self, *authors):
        return RedditFilter.by_author(authors)

class RedditFilter:
    @staticmethod
    def by_subreddit(children, *subreddits):
        subs = subreddits[0]
        for c in children:
            if c.data.subreddit in subs:
                yield c

    @staticmethod
    def by_author(children, *authors):
        a = authors[0]
        for c in children:
            if c.data.author in a:
                yield c
