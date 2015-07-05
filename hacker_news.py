import requests
from requests.auth import HTTPBasicAuth
from config import ConfigClass
from datetime import datetime, timedelta
from mysql import Article
import os.path
from lxml import html

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
        self.session = requests.Session()
        
    def login(self):
        login_url = '{0}/login?goto=news'.format(self.base_url)
        headers = { 'User-Agent': self.user_agent }
        data = { 'goto': 'news', 'acct': self.username, 'pw': self.password }

        # we may require web driver. I suspect that HN has CSRF tokens in place. That explains why we can't directly login to the account from the login page.
  

        response = self.session.post(login_url,
                            headers=headers,
                            data=data)

        print response
        print response.headers
        print response.text
        
        # check if logged in
        
    def fetch_upvoted_articles(self):
        url = '{0}/saved?id={1}'.format(self.base_url, self.username)
        response = self.session.get(url)
        tree = html.fromstring(response.text)
        tables = tree.xpath("//table")
        for t in tables:
            post = t.xpath("//tr[contains('@class', 'athing')]")
            if len(post) is 0:
                continue


            header = post.xpath("//td[@class='title']/a")
            link = header.attr('href')
            title = header.value
            author = post.xpath("//span").value
    # maybe get reports for the last 30 DAYS?

client = HackerNewsClient()
client.login()
