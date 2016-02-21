import configparser

#import os.path # needed on server side
class ConfigClass():
    parser = None
    
    def __init__(self):
        ConfigClass.init()
        
    @staticmethod
    def init():
        if ConfigClass.parser is None:
            ConfigClass.parser = configparser.ConfigParser()
            #path = os.getcwd() + "/bin/python/article-tracker/config.ini"  #needed_on_server_side  
            ConfigClass.parser.read('config.ini')   #TODO: Fix this on server side
            
    @staticmethod
    def fetchParam(section, key):
        return ConfigClass.parser.get(section, key)
            
    def get_reddit_config(self):
        section = 'config'
        c = ConfigClass()
        c.base_url = ConfigClass.fetchParam(section, 'BASE_URL')
        c.username = ConfigClass.fetchParam(section, 'USERNAME')
        c.user_agent = ConfigClass.fetchParam(section, 'USER_AGENT')
        c.client_id = ConfigClass.fetchParam(section, 'CLIENT_ID')
        c.client_secret = ConfigClass.fetchParam(section, 'CLIENT_SECRET')
        return c
    
    def get_mysql_config(self):
        section = 'database'
        c = ConfigClass()
        c.host = ConfigClass.fetchParam(section, 'host')
        c.username = ConfigClass.fetchParam(section, 'username')
        c.password = ConfigClass.fetchParam(section, 'password')
        c.db_name = ConfigClass.fetchParam(section, 'db_name')
        return c