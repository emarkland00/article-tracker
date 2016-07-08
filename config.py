from configparser import ConfigParser
import os

__CONFIG_INSTANCE__ = None

class ConfigClass:
    FILENAME = 'config.ini'
    def __init__(self):
        self.parser = self.__get_instance()

    def __get_instance(self):
        if not __CONFIG_INSTANCE__:
            if not self.__has_config_file():
                __CONFIG_INSTANCE__ = ConfigParser()
                __CONFIG_INSTANCE__.read(ConfigClass.FILENAME)

        return __CONFIG_INSTANCE__

    def __has_config_file(self):
        return os.path.isfile(ConfigClass.filename)

    def __has_section(self, name):
        if not __CONFIG_PARSER_FILE__:
            return false

        import pdb; pdb.set_trace()
        # find out command to check if section exists in config file

    @staticmethod
    def fetchParam(section, key):
        return ConfigClass.parser.get(section, key)

    def get_reddit_config(self):
        section = 'reddit'
        if not self.__has_section(section):
            return

        c = ConfigClass()
        c.base_url = ConfigClass.fetchParam(section, 'BASE_URL')
        c.username = ConfigClass.fetchParam(section, 'USERNAME')
        c.user_agent = ConfigClass.fetchParam(section, 'USER_AGENT')
        c.client_id = ConfigClass.fetchParam(section, 'CLIENT_ID')
        c.client_secret = ConfigClass.fetchParam(section, 'CLIENT_SECRET')
        return c

    def get_mysql_config(self):
        section = 'mysql'
        if not self.__has_section(section):
            return

        c = ConfigClass()
        c.host = ConfigClass.fetchParam(section, 'host')
        c.username = ConfigClass.fetchParam(section, 'username')
        c.password = ConfigClass.fetchParam(section, 'password')
        c.db_name = ConfigClass.fetchParam(section, 'db_name')
        return c
