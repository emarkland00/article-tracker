from ConfigParser import ConfigParser
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
        return ConfigClass.__INST__.instance is not None

    @staticmethod
    def get_instance():
        return ConfigClass.__INST__

    def __init__(self):
        if ConfigClass.__INST__ is None:
            raise ValueError('Need to instantiate config.ini via ConfigClass.init()')

        self.instance = ConfigClass.__INST__.instance

    @staticmethod
    def get_config(section_name, section_keys):
        instance = ConfigClass.get_instance()
        if not instance:
            return None

        inst = instance.instance
        if not inst.has_section(section_name):
            return None

        fn = lambda x: inst.get(section_name, x)
        return { k.lower():fn(k) for k in section_keys }

    
    def get_mysql_config(self):
        keys = [ 'HOST', 'USERNAME', 'PASSWORD', 'DB_NAME' ]
        return self.get_config('mysql', keys)

    def get_hacker_news_config(self):
        keys = [ 'BASE_URL', 'USERNAME', 'PASSWORD', 'USER_AGENT' ]
        return self.get_config('hacker_news', keys)

    def get_reddit_config(self):
        keys = [ 'BASE_URL', 'USERNAME', 'USER_AGENT', 'CLIENT_ID', 'CLIENT_SECRET', 'SUB_REDDITS' ]
        return self.get_config('reddit', keys)

    @staticmethod
    def has_config(config_name):
        if not ConfigClass.__INST__:
            return False

        cfg = ConfigClass.__INST__.instance
        return cfg and cfg.has_section(config_name)
