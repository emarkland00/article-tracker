from peewee import MySQLDatabase, Model, PrimaryKeyField, CharField, DateTimeField
from config import ConfigClass

__MYSQL_DB__ = MySQLDatabase(None)

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
        import pdb; pdb.set_trace()
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
            Article.insert_many(arts).execute()

# Check that we have the details needed to connect to database
mysql_config = ConfigClass().get_mysql_config()
if not mysql_config:
    print "Config file missing section for mysql"
else:    
    import pdb; pdb.set_trace()
    # initialize database connection
    __MYSQL_DB__.init(
        mysql_config['db_name'],
        host=mysql_config['host'],
        user=mysql_config['username'],
        passwd=mysql_config['password'])

    # Auto generate tables needed for this operation (if they don't exist)
    if not Article.table_exists():
        Article.create_table()

