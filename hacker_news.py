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
        hn_config = ConfigClass.get_hacker_news_config()
        self.username = hn_config.username
        self.password = hn_config.password
        self.base_url = hn_config.base_url
        
    def login(self):
        pass
    
    def fetch_upvoted_articles(self):
        pass
    # maybe get reports for the last 30 DAYS?