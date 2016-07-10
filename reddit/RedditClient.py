import requests
from requests.auth import HTTPBasicAuth
from config import ConfigClass
from datetime import datetime, timedelta
from mysql import Article
from reddit import *
import os.path
from RedditClientError import RedditClientError

class RedditClient:
    def __init__(self):
        reddit_config = ConfigClass().get_reddit_config()
        if not reddit_config:
            print "Missing reddit config. Unable to fetch content from reddit."
            return

        self.base_url = reddit_config['base_url']
        self.user_agent = reddit_config['user_agent']
        self.username = reddit_config['username']
        self.client_id = reddit_config['client_id']
        self.client_secret = reddit_config['client_secret']
        self.access_token = self.__fetch_access_token()

    def get_liked_posts(self):
        url = '{1}/user/{0}/liked/.json'.format(self.username, self.base_url)
        headers = {
            'User-Agent': self.user_agent,
            'Authorization': 'bearer ' + self.access_token
        }
        req = requests.get(url, headers=headers)
        json = req.json();
        return RedditPostListing(json['data'])

    def __fetch_access_token(self):
        filename = 'reddit_access_token'
        access_token = self.__fetch_access_token_from_file(filename)
        if access_token is not None:
            return access_token

        r = self.__fetch_access_token_from_url()
        access_token = r[0]
        exp_time = r[1]

        with open(filename, 'w') as f:
            f.write(access_token + '|' + str(exp_time))

        return access_token

    def __fetch_access_token_from_file(self, path):
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

    def __fetch_access_token_from_url(self):
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
