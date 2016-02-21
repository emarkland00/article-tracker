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
    def fetch_param(section, key):
        return ConfigClass.parser.get(section, key)
            
    def get_reddit_config(self):
        section = 'config'
        c = ConfigClass()
        c.base_url = ConfigClass.fetch_param(section, 'BASE_URL')
        c.username = ConfigClass.fetch_param(section, 'USERNAME')
        c.user_agent = ConfigClass.fetch_param(section, 'USER_AGENT')
        c.client_id = ConfigClass.fetch_param(section, 'CLIENT_ID')
        c.client_secret = ConfigClass.fetch_param(section, 'CLIENT_SECRET')
        return c
    
    def get_hacker_news_config(self):
        section = 'hacker_news'
        c = ConfigClass()
        c.base_url = ConfigClass.fetch_param(section, 'BASE_URL')
        c.username = ConfigClass.fetch_param(section, 'USERNAME')
        c.password = ConfigClass.fetch_param(section, 'PASSWORD')
        c.user_agent = ConfigClass.fetch_param(section, 'USER_AGENT')
        return c
                                            
    def get_mysql_config(self):
        section = 'database'
        c = ConfigClass()
        c.host = ConfigClass.fetch_param(section, 'host')
        c.username = ConfigClass.fetch_param(section, 'username')
        c.password = ConfigClass.fetch_param(section, 'password')
        c.db_name = ConfigClass.fetch_param(section, 'db_name')
        return c
        
