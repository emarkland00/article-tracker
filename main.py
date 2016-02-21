from reddit import RedditClient
from mysql import Article    
from hacker_news import HackerNewsClient

def go():
    #fetch_reddit_stuff()
    fetch_hacker_news_stuff()

def fetch_reddit_stuff():
    print("getting reddit stuff")
    client = RedditClient()
    filtered_posts = client.get_liked_posts().filter_by_new_listings().filter_by_subreddit(u'technology',u'BlackPeopleTwitter').posts()
        
    for post in filtered_posts:
        art = post.to_article()
        Article.create(name=art['name'], url=art['url'], source=art['source'], article_key=art['article_key'], timestamp=art['timestamp'])
        
    print("finished getting reddit stuff!")

def fetch_hacker_news_stuff():
    client = HackerNewsClient()
    client.login()
    
    """
    HACKER NEWS
    
    https://news.ycombinator.com/saved?id=sol7117
    
    requires user session cookie...
    """

go()
