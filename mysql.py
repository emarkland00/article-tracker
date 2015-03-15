from peewee import MySQLDatabase, Model, PrimaryKeyField, CharField, DateTimeField
from config import ConfigClass

mysql_config = ConfigClass().get_mysql_config()
mysql_db = MySQLDatabase(mysql_config.db_name, host=mysql_config.host, user=mysql_config.username, passwd=mysql_config.password)

class MySQLModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db
        
class Article(MySQLModel):
    """A generic container for holding information"""
    article_id = PrimaryKeyField()
    name = CharField()
    url = CharField()
    source = CharField()
    article_key = CharField()
    timestamp = DateTimeField()
    
def init():
    mysql_db.connect()
    if Article.table_exists() is False:
        Article.create_table()
    
init()