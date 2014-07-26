import requests
from datetime import datetime
from reddit import RedditArticleListing
from mysql import Article

# config
BASE_URL = 'http://www.reddit.com'
USER_AGENT = 'sol7117 article fetcher'
USERNAME = 'sol7117'    

def get_liked_articles():    
    url = BASE_URL + '/user/{0}/liked/.json'.format(USERNAME) 
    headers = { 'User-Agent': USER_AGENT }
    req = requests.get(url, headers=headers)
    json = req.json();
    return RedditArticleListing(json['data']) 
         
liked_articles = get_liked_articles()
filtered_articles = liked_articles.filter_by_subreddit(u'technology', u'AskReddit')

if Article.table_exists() is False:
    Article.create_table()
        
for art in Article.select():
    print art.article_id, art.name, art.url, art.timestamp
    
for f in filtered_articles:
    Article.create(name=f.data.title, url=f.data.url, source='reddit', timestamp=datetime.now())
    
print "done!"