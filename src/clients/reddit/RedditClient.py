import os.path
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from clients.TrackerClient import TrackerClient
from RedditClientError import RedditClientError
from RedditPostListing import RedditPostListing

class RedditClient(TrackerClient):
    __AUTH_URL__ = 'https://www.reddit.com/api/v1/access_token'
    __FILE_NAME__ = 'reddit_access_token'
    TRACKER_NAME = 'reddit'
    KEYS = [ 'BASE_URL', 'USERNAME', 'USER_AGENT', 'CLIENT_ID', 'CLIENT_SECRET', 'SUB_REDDITS' ]

    def __init__(self, json_config):
        super(RedditClient, self).__init__(json_config)
        if not json_config:
            return

        self.base_url = json_config['base_url']
        self.user_agent = json_config['user_agent']
        self.username = json_config['username']
        self.client_id = json_config['client_id']
        self.client_secret = json_config['client_secret']
        self.sub_reddits = None
        if 'sub_reddits' in json_config:
            self.sub_reddits = [ s.decode('utf-8') for s in json_config["sub_reddits"].split(',') ]
        self.access_token = self.__fetch_access_token()
        self.__configured = True

    def _get_articles(self):
        filtered_posts = self.__get_liked_posts()
        articles = []
        for post in filtered_posts:
            art = post.as_json()
            articles.append(self.create_article(art['name'], art['url'], 'reddit', art['article_key'], art['timestamp']))

        return articles

    def __get_liked_posts(self):
        url = '{1}/user/{0}/liked/.json'.format(self.username, self.base_url)
        headers = {
            'User-Agent': self.user_agent,
            'Authorization': 'bearer ' + self.access_token
        }
        req = requests.get(url, headers=headers)
        json = req.json()
        posts = RedditPostListing(json['data']).children
        if self.sub_reddits:
            posts = [ l for l in posts if l.data.subreddit in self.sub_reddits ]

        return posts

    def __fetch_access_token(self):
        # get cached token
        access_token = self.__fetch_access_token_from_file(RedditClient.__FILE_NAME__)
        if access_token is not None:
            return access_token

        # get fresh token
        access_token, exp_time = self.__fetch_access_token_from_url()
        with open(RedditClient.__FILE_NAME__, 'w') as f:
            f.write(access_token + '|' + str(exp_time))

        return access_token

    def __fetch_access_token_from_file(self, path):
        if not os.path.isfile(path):
            return None

        with open(path, 'r') as f:
            content = f.read().split('|')
            if len(content) != 2:
                return None

            access_token = content[0]
            exp_timestamp = datetime.strptime(content[1], '%Y-%m-%d %H:%M:%S.%f')
            if exp_timestamp < datetime.now():
                return None

            return access_token

    def __fetch_access_token_from_url(self):
        req = requests.post(RedditClient.__AUTH_URL__,
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={ 'User-Agent': self.user_agent },
            data={ 'grant_type':'client_credentials' })

        json = req.json()
        access_token = json["access_token"]
        expires = json["expires_in"]
        exp_time = datetime.now() + timedelta(seconds=expires)
        return (access_token, exp_time)
