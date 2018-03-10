import sys
import os
import argparse
from datetime import datetime
from config import ConfigClass
from mysql import Article
from clients.TrackerClientFactory import TrackerClientFactory

def main():
    #TODO: Add a flag to specify if we want to get flags from environment variables or flag
    args = collect_args()

    # Load config
    if not ConfigClass.init(args.config):
        print_msg("Unable to find load config file '{0}'.".format(args.config))
        exit(-1)

    # Get clients
    clients = TrackerClientFactory.get_clients(ConfigClass.get_instance())
    if not clients:
        print_msg("Unable to find any configured clients. Exiting.")
        exit(-1)

    # Get articles
    for c in clients:
        print_msg("Fetching articles for {0}".format(c.TRACKER_NAME))
        articles = c.get_articles()
        articles = Article.filter_by_new_listings(articles)
        if Article.bulk_insert(articles):
            print_msg("finished getting {0} stuff!".format(c.TRACKER_NAME))
        else:
            print_msg("Found no new articles for {0}".format(c.TRACKER_NAME))

def collect_args():

    parser = argparse.ArgumentParser(description="A tool used for getting your latest articles that you've read these days")

    # config file
    def valid_file(filename):
        if not os.path.exists(filename):
            raise argparse.ArgumentError("Unable to find file {0}".format(filename))
        return filename
    parser.add_argument('--config', help='The path to the configuration file', type=valid_file, default='config.ini')

    args = parser.parse_args()
    if args.help:
        parser.print_help()

    return args


def print_msg(msg):
    # Helper print method that also records timestamp
    date = datetime.now()
    d = date.strftime('%Y-%m-%d %I:%M:%S %p')
    print(d + ': ' + msg)

if __name__ == '__main__':
    main()
