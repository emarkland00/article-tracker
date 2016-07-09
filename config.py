from configparser import ConfigParser
import os

__CONFIG_INSTANCE__ = None

class ConfigClass:
    FILENAME = 'config.ini'
    def __init__(self):
        global __CONFIG_INSTANCE__
        self.__parser = self.__get_instance()

    def has_config(self):
        return __CONFIG_INSTANCE__ is not None

    def __get_instance(self):
        global __CONFIG_INSTANCE__
        # Manage a global instance of the parser
        if not __CONFIG_INSTANCE__:
            # Check that the config file exists before creating instance
            if os.path.isfile(ConfigClass.FILENAME):
                __CONFIG_INSTANCE__ = ConfigParser()
                __CONFIG_INSTANCE__.read(ConfigClass.FILENAME)

        return __CONFIG_INSTANCE__

    def __get_section(self, name):
        if not __CONFIG_INSTANCE__:
            return None

        import pdb; pdb.set_trace()
        # find out command to check if section exists in config file

    def __fetch_param(section, key):
        return __CONFIG_INSTANCE__.get(section, key)

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
