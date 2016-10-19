from datetime import datetime
from config import ConfigClass
from mysql import Article, init as mysql_init
import sys
import itertools


def config_init():
    filename = 'config.ini'
    if len(sys.argv) == 2:
        filename = sys.argv[1]

    # if loaded config successfully, then we can load mysql
    import pdb; pdb.set_trace()
    if ConfigClass.init(filename):
        mysql_init()
    else:
        print_msg("MySQL config needed before proceeding")

def go():
    if ConfigClass.has_config('reddit'):
        fetch_reddit_stuff()

    if ConfigClass.has_config('hacker_news'):
        fetch_hacker_news_stuff()

def fetch_reddit_stuff():
    from reddit import RedditClient as r
    print_msg("getting reddit stuff")
    client = r.RedditClient()
    if not client:
        print_msg("Failed to load up reddit client")
        return

    filtered_posts = client.get_liked_posts()
    articles = []

    for post in filtered_posts:
        art = post.as_json()
        articles.append(create_article(art['name'], art['url'], 'reddit', art['article_key'], art['timestamp']))

    articles = filter_by_new_listings(articles)
    save_articles(articles)
    print_msg("finished getting reddit stuff!")

def fetch_hacker_news_stuff():
    from hackernews import HackerNewsClient as hn
    print_msg("getting hacker news stuff")
    client = hn.HackerNewsClient()
    if not client:
        print_msg("Failed to load up hacker news client")
        return

    posts = client.fetch_upvoted_posts()
    articles = [ create_article(p['title'], p['link'], 'hacker news', p['id'], p['timestamp']) for p in posts ]
    articles = filter_by_new_listings(articles)
    save_articles(articles)
    print_msg("finished getting hacker news stuff!")

def filter_by_new_listings(articles):
    """
    Filter articles by those not yet stored in the database
    """
    if not articles:
        return []

    results = articles

    # must sort articles before grouping
    source_key = lambda x: x.source
    arts = sorted(articles, key=source_key)
    for source, group in itertools.groupby(arts, key=source_key):
        # filter by checking if IDs exist for the corresponding source
        ids = [ g.article_key for g in group ]
        existing = Article.find_all_by_source_and_ids(source, ids)
        known = [ a.article_key for a in existing ]
        results = [ r for r in results if r.article_key not in known ]

    return results

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
    go()
