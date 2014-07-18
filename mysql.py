from peewee import MySQLDatabase, Model, PrimaryKeyField, CharField, DateTimeField

mysql_db = MySQLDatabase('article-tracker-db', host='127.0.0.1', user='root', passwd='password')

class MySQLModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db
        
class Article(MySQLModel):
    article_id = PrimaryKeyField()
    name = CharField()
    url = CharField()
    source = CharField()
    timestamp = DateTimeField()
    
def init():
    mysql_db.connect()
    if Article.table_exists() is False:
        Article.create_table()
    
init()