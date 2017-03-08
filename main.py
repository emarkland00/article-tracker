import sys
from datetime import datetime
from config import ConfigClass
from mysql import Article
from clients.TrackerClientFactory import TrackerClientFactory

if __name__ == '__main__':
    def print_msg(msg):
        # Helper print method that also records timestamp
        date = datetime.now()
        d = date.strftime('%Y-%m-%d %I:%M:%S %p')
        print(d + ': ' + msg)

    # Load config
    filename = sys.argv[1] if len(sys.argv) == 2 else "config.ini"
    if not ConfigClass.init(filename):
        print_msg("Unable to find load config file {0}".format(filename))
        exit()

    # Get clients
    clients = TrackerClientFactory.get_clients(ConfigClass.get_instance())
    if not clients:
        print_msg("Unable to find any configured clients. exiting")
        exit()

    # Get articles
    for c in clients:
        print_msg("Fetching articles for {0}".format(c.TRACKER_NAME))
        articles = c.get_articles()
        articles = Article.filter_by_new_listings(articles)
        if Article.bulk_insert(articles):
            print_msg("finished getting {0} stuff!".format(c.TRACKER_NAME))
        else:
            print_msg("Found no new articles for {0}".format(c.TRACKER_NAME))
