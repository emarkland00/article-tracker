import requests
from reddit import RedditArticleListing
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
for f in filtered_articles:
    print '{0}: {1}'.format(f.data.subreddit, f.data.title)