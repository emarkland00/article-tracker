from datetime import datetime
from mysql import Article
from config import ConfigClass

def go():
    if not ConfigClass().has_config():
        print "Missing config.ini."
        return

    fetch_reddit_stuff()
    fetch_hacker_news_stuff()

def fetch_reddit_stuff():
    from reddit import RedditClient
    print_msg("getting reddit stuff")
    client = RedditClient()
    filtered_posts = client.get_liked_posts().filter_by_new_listings().filter_by_subreddit(u'technology')

    for post in filtered_posts:
        art = post.to_article()
        Article.create(name=art['name'], url=art['url'], source=art['source'], article_key=art['article_key'], timestamp=art['timestamp'])

    print_msg("finished getting reddit stuff!")

def fetch_hacker_news_stuff():
    """
    HACKER NEWS

    https://news.ycombinator.com/saved?id=sol7117

    requires user session cookie...
    """
    pass
    

def print_msg(msg):
    date = datetime.now()
    d = date.strftime('%Y-%m-%d %-I:%M:%S %p')
    print(d + ': ' + msg)

if __name__ == '__main__':
    go()
