from datetime import datetime
from config import ConfigClass
from mysql import Article, init as mysql_init
import sys
import itertools
from clients.TrackerClient import TrackerClient

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

def print_msg(msg):
    date = datetime.now()
    d = date.strftime('%Y-%m-%d %I:%M:%S %p')
    print(d + ': ' + msg)

if __name__ == '__main__':
    # Load config
    filename = 'config.ini'
    if len(sys.argv) == 2:
        filename = sys.argv[1]

    if not ConfigClass.init(filename):
        print_msg("Unable to find load config file", filename)
        exit()

    # Get clients
    clients = TrackerClient.get_clients(ConfigClass.get_instance())
    if not clients:
        print_msg("Unable to find any configured clients. exiting")

    # Get articles
    for c in clients:
        articles = c.get_articles()
        articles = filter_by_new_listings(articles)
        save_articles(articles)
        print_msg("finished getting {0} stuff!".format(c.TRACKER_NAME))
