from datetime import datetime
from config import ConfigClass
from mysql import Article, init as mysql_init
import sys
import itertools
from clients.TrackerClientFactory import TrackerClientFactory

if __name__ == '__main__':
    def print_msg(msg):
        # Helper print method that also records timestamp
        date = datetime.now()
        d = date.strftime('%Y-%m-%d %I:%M:%S %p')
        print(d + ': ' + msg)
        
    # Load config
    filename = 'config.ini'
    if len(sys.argv) == 2:
        filename = sys.argv[1]

    if not ConfigClass.init(filename):
        print_msg("Unable to find load config file", filename)
        exit()

    # Get clients
    clients = TrackerClientFactory.get_clients(ConfigClass.get_instance())
    if not clients:
        print_msg("Unable to find any configured clients. exiting")

    # Get articles
    for c in clients:
        articles = c.get_articles()
        articles = Article.filter_by_new_listings(articles)
        Article.save_articles(articles)
        print_msg("finished getting {0} stuff!".format(c.TRACKER_NAME))
