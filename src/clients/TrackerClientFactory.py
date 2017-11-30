from clients.TrackerClient import TrackerClient
from clients.reddit.RedditClient import RedditClient
from clients.hackernews.HackerNewsClient import HackerNewsClient
from config import ConfigClass

class TrackerClientFactory:
    @staticmethod
    def get_clients(config):
        """
        Get a list of all configured tracker clients
        config - The config object containing all possible tracker configurations
        """
        for subclass in TrackerClient.__subclasses__():
            client_config = ConfigClass.get_config(subclass.TRACKER_NAME or '', subclass.KEYS or [])
            if client_config:
                client = subclass(client_config)
                if client.is_configured:
                    yield client
