import itertools
from mysql import Article

class TrackerClient(object):
    """
    The base class for an article tracking client
    - json_config: The config needed to allow the client to run
    """

    def __init__(self, json_config):
        self.tracker_name = 'name'
        self.config = json_config
        self.config_keys = []
        self.__configured = False

    def is_configured(self):
        """
        Checks whether if the client is configured to find articles
        """
        return self.__configured

    def create_article(self, name, url, source, article_key, timestamp):
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

    def get_articles(self, new_only=True):
        """
        Gets a list of article objects
        """
        articles = self._get_articles()
        if not new_only:
            return articles
        return self.__filter_by_new_listings(articles)

    def _get_articles(self):
        raise NotImplementedError('Must define method in sub-class.')

    def __filter_by_new_listings(self, articles):
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
