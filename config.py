from configparser import ConfigParser
import os

class ConfigClass:
    __CONFIG_INSTANCE__ = None
    FILENAME = 'config.ini'

    def __init__(self):
        self.__instance = None
        if ConfigClass.__CONFIG_INSTANCE__:
            self.__instance = ConfigClass.__CONFIG_INSTANCE__

    def __new__(cls):
        import pdb; pdb.set_trace()
        if not ConfigClass.__CONFIG_INSTANCE__:
            ConfigClass.__CONFIG_INSTANCE__ = __ConfigInstance(ConfigClass.FILENAME)
        return ConfigClass.__CONFIG_INSTANCE__

    def __get_section(self, name):
        if not self.__instance:
            return None


        # find out command to check if section exists in config file

    def __fetch_param(section, key):
        return self.__instance.get(section, key)

    def get_reddit_config(self):
        reddit_config = self.__get_section('reddit')
        if not reddit_config:
            return None

        return {
            'base_url': reddit_config.get('BASE_URL'),
            'username': self.__fetch_param(section, 'USERNAME'),
            'user_agent': self.__fetch_param(section, 'USER_AGENT'),
            'client_id': self.__fetch_param(section, 'CLIENT_ID'),
            'client_secret': self.__fetch_param(section, 'CLIENT_SECRET')
        }

    def get_mysql_config(self):
        section = 'mysql'
        mysql_config = self.__get_section(section)
        if not mysql_config:
            return None

        return {
            "host": self.__fetch_param(section, 'host'),
            "username": self.__fetch_param(section, 'username'),
            "password": self.__fetch_param(section, 'password'),
            "db_name": self.__fetch_param(section, 'db_name')
        }

class __ConfigInstance:
    """
    An internal container used to manage the config instance
    """
    def __init(self, filename):
        self.filename = filename
        self.instance = self.__get_instance()

    def __get_instance(self):
        # Check that the config file exists before creating instance
        if not os.path.isfile(self.filename):
            return None

        p = ConfigParser()
        p.read(self.filename)
        return p
