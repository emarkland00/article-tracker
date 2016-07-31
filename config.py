from configparser import ConfigParser
import os

class ConfigClass:
    class __ConfigInstance:
        """
        An internal container used to manage the config instance
        """
        def __init__(self, filename):
            self.filename = filename
            self.instance = self.__get_instance()

        def __get_instance(self):
            # Check that the config file exists before creating instance
            if not os.path.isfile(self.filename):
                return None

            p = ConfigParser()
            p.read(self.filename)
            return p

    # The singleton used to hold the config instance
    __INST__ = None

    # The name of the config file to search for
    FILENAME = 'config.ini'

    @staticmethod
    def init(filename):
        ConfigClass.__INST__ = ConfigClass.__ConfigInstance(filename)

    def __init__(self):
        if ConfigClass.__INST__ is None:
            raise ValueError('Need to instantiate config.ini via ConfigClass.init()')

        self.instance = ConfigClass.__INST__.instance

    def __get_section_values(self, section_name, section_keys):
        if not self.instance or not self.instance.has_section(section_name):
            return None

        fn = lambda x: self.instance.get(section_name, x)
        return { k.lower():fn(k) for k in section_keys }
        # find out command to check if section exists in config file

    def get_mysql_config(self):
        keys = [ 'host', 'username', 'password', 'db_name' ]
        return self.__get_section_values('mysql', keys)

    def get_hacker_news_config(self):
        keys = [ 'BASE_URL', 'USERNAME', 'PASSWORD', 'USER_AGENT' ]
        return self.__get_section_values('hacker_news', keys)

    def get_reddit_config(self):
        keys = [ 'BASE_URL', 'USERNAME', 'USER_AGENT', 'CLIENT_ID', 'CLIENT_SECRET', 'SUB_REDDITS' ]
        return self.__get_section_values('reddit', keys)
