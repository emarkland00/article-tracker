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

def init(db_instance):
    # Check if we already have an instance to the database
    if db_instance:
        return db_instance

    # Check that we have the details needed to connect to database
    mysql_config = ConfigClass().get_mysql_config()
    if not mysql_config:
        print "Config file missing section for mysql"
        return None

    db_instance = MySQLDatabase(mysql_config.db_name, host=mysql_config.host, user=mysql_config.username, passwd=mysql_config.password)
    db_instance.connect()

    # Auto generate tables needed for this operation (if they don't exist)
    if Article.table_exists() is False:
        Article.create_table()

    return db_config

__MYSQL_DB__ = init(__MYSQL_DB__)
