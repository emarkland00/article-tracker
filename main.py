from datetime import datetime
from config import ConfigClass
import sys

def config_init():
    filename = 'config.ini'
    if len(sys.argv) == 2:
        filename = sys.argv[1]

    ConfigClass.init(filename)

def go():
    fetch_reddit_stuff()
    fetch_hacker_news_stuff()

def fetch_reddit_stuff():
    from reddit import RedditClient as r
    print_msg("getting reddit stuff")
    client = r.RedditClient()
    if not client:
        print "Failed to load up reddit client"
        return

    filtered_posts = client.get_liked_posts()
    articles = []

    for post in filtered_posts:
        art = post.as_json()
        articles.append(create_article(art['name'], art['url'], 'reddit', art['article_key'], art['timestamp']))

    save_articles(articles)
    print_msg("finished getting reddit stuff!")

def fetch_hacker_news_stuff():
    from hackernews import HackerNewsClient as hn
    print_msg("getting hacker news stuff")
    client = hn.HackerNewsClient()
    posts = client.fetch_upvoted_posts()
    articles = [
        create_article(a['title'], a['link'], 'hacker news', a['id'], a['timestamp'])
        for a
        in posts
    ]
    articles = filter_by_new_listings(articles)
    save_articles(articles)
    print_msg("finished getting hacker news stuff!")

def filter_by_new_listings(articles):
    source = articles[0].source
    ids = [ a.article_key for a in articles ]
    existing = Article.find_all_by_source_and_ids(source, ids)
    known = [ a.article_key for a in existing ]
    return [ a for a in articles if a.article_key not in known ]

def save_articles(articles):
    if articles:
        Article.bulk_insert(articles)

def create_article(name, url, source, article_key, timestamp):
    return Article(
        name=name,
        url=url,
        source=source,
        article_key=article_key,
        timestamp=timestamp
    )

def print_msg(msg):
    date = datetime.now()
    d = date.strftime('%Y-%m-%d %I:%M:%S %p')
    print(d + ': ' + msg)

if __name__ == '__main__':
    config_init()

    # import other stuff
    from mysql import Article

    go()
