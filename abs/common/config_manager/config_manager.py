#! /usr/bin/env python3

# lib imports
import os
from configparser import ConfigParser, ExtendedInterpolation

# project imports
from abs.common.utils.singletone import Singleton
from abs.common import COMMON_FOLDER


CONF_FILE_NAME = "abs.conf.ini"


@Singleton
class ConfigManager:
    def __init__(self):
        conf_file_path = os.path.join(COMMON_FOLDER, 'conf', CONF_FILE_NAME)
        self.__app_config = ConfigParser(interpolation=ExtendedInterpolation())
        self.__app_config.read(conf_file_path)

    def get_str(self, section, key, fallback=None):
        if fallback is None:
            return self.__app_config.get(section, key)
        else:
            return self.__app_config.get(section, key, fallback=fallback)

    def get_int(self, section, key, fallback=None):
        if fallback is None:
            return self.__app_config.getint(section, key)
        else:
            return self.__app_config.getint(section, key, fallback=fallback)

    def get_bool(self, section, key, fallback=None):
        if fallback is None:
            return self.__app_config.getboolean(section, key)
        else:
            return self.__app_config.getboolean(section, key, fallback=fallback)


