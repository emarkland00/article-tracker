import requests
from config import ConfigClass
from datetime import datetime
from mysql import Article
import unicodedata

class RedditClient:
    def __init__(self):
        reddit_config = ConfigClass().get_reddit_config()
        self.base_url = reddit_config.base_url
        self.user_agent = reddit_config.user_agent
        self.username = reddit_config.username
    
    def get_liked_posts(self):    
        url = '{1}/user/{0}/liked/.json'.format(self.username, self.base_url) 
        headers = { 'User-Agent': self.user_agent }
        req = requests.get(url, headers=headers)
        json = req.json();
        return RedditPostListing(json['data'])

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