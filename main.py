import requests
from config import ConfigClass
from datetime import datetime
from reddit import RedditArticleListing
from mysql import Article    

def get_liked_articles(config):    
    url = '{1}/user/{0}/liked/.json'.format(config.username, config.base_url) 
    headers = { 'User-Agent': config.user_agent }
    req = requests.get(url, headers=headers)
    json = req.json();
    return RedditArticleListing(json['data']) 

settings = ConfigClass().get_reddit_config()         
liked_articles = get_liked_articles(settings)
filtered_articles = liked_articles.filter_by_subreddit(u'technology', u'AskReddit')

if Article.table_exists() is False:
    Article.create_table()
        
for art in Article.select():
    print art.article_id, art.name, art.url, art.timestamp
    
for f in filtered_articles:
    Article.create(name=f.data.title, url=f.data.url, source='reddit', timestamp=datetime.now())
    
print "done!"