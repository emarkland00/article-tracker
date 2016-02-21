import requests
from requests.auth import HTTPBasicAuth
from config import ConfigClass
from datetime import datetime, timedelta
from mysql import Article
import os.path

class HackerNewsClientError(Exception):
    def __init__(self, value):
        self.value = value
         
    def __str__(self):
        return repr(self.value)
    
class HackerNewsClient:
    def __init__(self):
        hn_config = ConfigClass().get_hacker_news_config()
        self.username = hn_config.username
        self.password = hn_config.password
        self.base_url = hn_config.base_url
        self.user_agent = hn_config.user_agent
        
    def login(self):        
        s = requests.session()
        login = s.get(self.base_url, verify=False, headers={'User-Agent': self.user_agent })
        
        res = s.post(self.base_url + '/login', 
                      verify=False,
                      headers={'User-Agent': self.user_agent, 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*', 'Origin': self.base_url},
                      data='goto=news&acct={0}&pw={1}'.format(self.username, self.password))
        t = res.text
    
    def fetch_upvoted_articles(self):
        pass
    # maybe get reports for the last 30 DAYS?