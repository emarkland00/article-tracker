import ConfigParser

class ConfigClass():
    parser = None
    
    def __init__(self):
        ConfigClass.init()
        
    @staticmethod
    def init():
        if ConfigClass.parser is None:
            ConfigClass.parser = ConfigParser.ConfigParser()
            ConfigClass.parser.read('config.ini')
            
    @staticmethod
    def fetchParam(section, key):
        return ConfigClass.parser.get(section, key)
            
    def get_reddit_config(self):
        section = 'config'
        c = ConfigClass()
        c.base_url = ConfigClass.fetchParam(section, 'BASE_URL')
        c.username = ConfigClass.fetchParam(section, 'USERNAME')
        c.user_agent = ConfigClass.fetchParam(section, 'USER_AGENT')
        return c
    
    def get_mysql_config(self):
        section = 'database'
        c = ConfigClass()
        c.host = ConfigClass.fetchParam(section, 'host')
        c.username = ConfigClass.fetchParam(section, 'username')
        c.password = ConfigClass.fetchParam(section, 'password')
        c.db_name = ConfigClass.fetchParam(section, 'db_name')
        return c
        
    
