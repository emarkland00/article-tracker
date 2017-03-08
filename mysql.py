from peewee import MySQLDatabase, Model, PrimaryKeyField, CharField, DateTimeField
from config import ConfigClass
import itertools

__MYSQL_DB__ = MySQLDatabase(None)

class MySQLModel(Model):
    __MYSQL_INIT__ = None
    """A base model that will use our MySQL database"""
    class Meta:
        database = __MYSQL_DB__

    @classmethod
    def has_db_configured(cls):
        """
        Checks whether if the db has been configured
        """
        if MySQLModel.__MYSQL_INIT__ is None:
            MySQLModel.__MYSQL_INIT__ = init()

        try:
            return cls._meta.database.get_conn().open;
        except:
            return False

class Article(MySQLModel):
    """A generic container for holding information"""
    article_id = PrimaryKeyField()
    name = CharField()
    url = CharField()
    source = CharField()
    article_key = CharField()
    timestamp = DateTimeField()

    @classmethod
    def find_all_by_source_and_ids(cls, source, ids):
        if not super(Article, cls).has_db_configured():
            return []

        if not source and ids:
            return []

        return [ a for a in Article.select().where((Article.article_key << ids) & (Article.source == source)) ]

    @classmethod
    def bulk_insert(cls, articles):
        if not articles:
            return False

        if not super(Article, cls).has_db_configured():
            return False

        arts = [ {
            "name": a.name,
            "url": a.url,
            "source": a.source,
            "article_key": a.article_key,
            "timestamp": a.timestamp
        } for a in articles ]


        with __MYSQL_DB__.atomic():
            return Article.insert_many(arts).execute()

    @classmethod
    def filter_by_new_listings(cls, articles):
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

def init():
    # Check that we have the details needed to connect to database
    mysql_config = ConfigClass().get_mysql_config()
    if not mysql_config:
        print "Config file missing section for [mysql]"
        return False

    # initialize database connection
    __MYSQL_DB__.init(
        mysql_config['db_name'],
        host=mysql_config['host'],
        user=mysql_config['username'],
        passwd=mysql_config['password'])

    # Auto generate tables needed for this operation (if they don't exist)
    if not Article.table_exists():
        Article.create_table()

    return True
