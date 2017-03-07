from mysql import Article

class TrackerClient:
    """
    The base class for an article tracking client
    - json_config: The config needed to allow the client to run
    """

    def __init__(self, json_config):
        self.config = json_config
        self.__configured = False

    def is_configured(self):
        """
        Checks whether if the client is configured to find articles
        """
        return self.__configured

    def create_article(name, url, source, article_key, timestamp):
        """
        A helper method for creating an article
        """
        return Article(
            name=name,
            url=url,
            source=source,
            article_key=article_key,
            timestamp=timestamp
        )

    def get_articles(self):
        """
        Gets a list of article objects
        """
        raise NotImplementedError('Must define method in sub-class.')
