import requests
import ConfigParser
from datetime import datetime
from reddit import RedditArticleListing
from mysql import Article    

class ConfigClass():
    pass

def init():
    parser = ConfigParser.ConfigParser()
    parser.read('config')
    config = ConfigClass()
    config.base_url = parser.get('config', 'BASE_URL')
    config.username = parser.get('config', 'USERNAME')
    config.user_agent = parser.get('config', 'USER_AGENT')
    return config

def get_liked_articles(config):    
    url = '{1}/user/{0}/liked/.json'.format(config.username, config.base_url) 
    headers = { 'User-Agent': config.user_agent }
    req = requests.get(url, headers=headers)
    json = req.json();
    return RedditArticleListing(json['data']) 

settings = init()         
liked_articles = get_liked_articles(settings)
filtered_articles = liked_articles.filter_by_subreddit(u'technology', u'AskReddit')

if Article.table_exists() is False:
    Article.create_table()
        
for art in Article.select():
    print art.article_id, art.name, art.url, art.timestamp
    
for f in filtered_articles:
    Article.create(name=f.data.title, url=f.data.url, source='reddit', timestamp=datetime.now())
    
print "done!"