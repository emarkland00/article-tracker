from datetime import datetime
from config import ConfigClass
import sys

def config_init():
    filename = 'config.ini'
    if len(sys.argv) == 2:
        filename = sys.argv[1]

    ConfigClass.init(filename)

def go():
    #fetch_reddit_stuff()
    fetch_hacker_news_stuff()

def fetch_reddit_stuff():
    from reddit import RedditClient as r
    print_msg("getting reddit stuff")
    client = r.RedditClient()
    if not client:
        print "Failed to load up reddit client"
        return

    filtered_posts = client.get_liked_posts().filter_by_new_listings().filter_by_subreddit(u'technology',u'BlackPeopleTwitter').posts()

    for post in filtered_posts:
        art = post.to_article()
        Article.create(
            name=art['name'],
            url=art['url'],
            source=art['source'],
            article_key=art['article_key'],
            timestamp=art['timestamp'])

    print_msg("finished getting reddit stuff!")

def fetch_hacker_news_stuff():
    from hackernews import HackerNewsClient as hn
    client = hn.HackerNewsClient()
    client.login()

    """
    HACKER NEWS

    https://news.ycombinator.com/saved?id=sol7117

    requires user session cookie...
    """


def print_msg(msg):
    date = datetime.now()
    d = date.strftime('%Y-%m-%d %I:%M:%S %p')
    print(d + ': ' + msg)

if __name__ == '__main__':
    config_init()

    # import other stuff
    from mysql import Article

    go()
