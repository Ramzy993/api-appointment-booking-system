#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ˅

import os
import logging

from abs.common.utils.singletone import Singleton
from abs.common.config_manager.config_manager import ConfigManager
from abs.common import COMMON_FOLDER


@Singleton
class LogManager:

    log_folder = os.path.join(COMMON_FOLDER, 'log_manager', 'logs')
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file_path = os.path.join(log_folder, ConfigManager().get_str('LOGGER', 'log_file_name'))
    log_level = ConfigManager().get_str('LOGGER', 'log_level', 'DEBUG')
    log_to_console = ConfigManager().get_bool('LOGGER', 'log_to_console', True)
    log_time_format = ConfigManager().get_str('LOGGER', 'log_time_format')
    log_format = '[%(asctime)s] [%(levelname)s] - %(message)s'
    logger_name = ConfigManager().get_str('LOGGER', 'logger_name', 'DEBUG')

    def __init__(self):
        logging.basicConfig(filename=self.log_file_path, filemode='a', datefmt=self.log_time_format, level=self.log_level,
                            format=self.log_format)
        if self.log_to_console:
            logger_handler_stream = logging.StreamHandler()
            logger_handler_stream.setLevel(self.log_level)
            logger_handler_stream.setFormatter(fmt=logging.Formatter(self.log_format))
            logger = logging.getLogger(self.logger_name)
            logger.addHandler(logger_handler_stream)

    def debug(self, msg):
        logging.getLogger(self.logger_name).debug(msg)

    def info(self, msg):
        logging.getLogger(self.logger_name).info(msg)

    def error(self, msg):
        logging.getLogger(self.logger_name).error(msg)

    def critical(self, msg):
        logging.getLogger(self.logger_name).critical(msg)
