from peewee import MySQLDatabase, Model, PrimaryKeyField, CharField, DateTimeField
from config import ConfigClass

__MYSQL_DB__ = None

class MySQLModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = __MYSQL_DB__

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
        if not source and ids:
            return []

        return [ a for a in Article.select().where((Article.article_key << ids) & (Article.source == source)) ]

    @classmethod
    def bulk_insert(cls, articles):
        arts = [ {
            "name": a.name,
            "url": a.url,
            "source": a.source,
            "article_key": a.article_key,
            "timestamp": a.timestamp
        } for a in articles ]
        with __MYSQL_DB__.atomic():
            Article.insert_many(arts)

def init(db_instance):
    # Check if we already have an instance to the database
    if db_instance:
        return db_instance

    # Check that we have the details needed to connect to database
    mysql_config = ConfigClass().get_mysql_config()
    if not mysql_config:
        print "Config file missing section for mysql"
        return None

    db_instance = MySQLDatabase(
        mysql_config['db_name'],
        host=mysql_config['host'],
        user=mysql_config['username'],
        passwd=mysql_config['password'])
    db_instance.connect()

    # Auto generate tables needed for this operation (if they don't exist)
    if not Article.table_exists():
        Article.create_table()

    return db_instance

__MYSQL_DB__ = init(__MYSQL_DB__)
