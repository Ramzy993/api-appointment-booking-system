#! /usr/bin/env python3

# lib imports
import argparse
import pathlib
import logging
import os
import json

from configparser import ConfigParser, ExtendedInterpolation

logger = logging.getLogger('trace.' + __name__)

CONF_FOLDER = pathlib.Path(__file__).parent.absolute()
CONF_FILE_NAME = "abs.conf.ini"


def generate_conf_files(overrides, environment):
    config = ConfigParser(interpolation=ExtendedInterpolation())
    file = os.path.join(CONF_FOLDER, CONF_FILE_NAME)

    try:
        config.read(file)
    except:
        raise Exception(f"Failed to parse the active environment file {file}")

    if 'test' in environment:
        env = 'test'
    else:
        env = 'dev'

    for section in overrides[environment]:

        if not config.has_section(section) and section != 'DEFAULT':
            raise Exception(f"Section '{section}' is not in {CONF_FILE_NAME}.")

        for key in overrides[environment][section]:
            if not config.has_option(section, key):
                raise Exception(f"Key '{key}' is not in '{section}'.")

            if key == 'env':
                config.set('DEFAULT', 'env', env)
            else:
                config.set(section, key, overrides[environment][section][key])

    with open(file, 'w') as fh:
        config.write(fh)
    logger.info(f"Active environment in {file} has been set to {environment}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Environment Config Generator')
    parser.add_argument('-c', '--config', type=str, required=True, help='JSON file with configuration overrides')
    parser.add_argument('-e', '--environment', type=str, required=True, help="Specify the current working environment.")

    args = parser.parse_args()

    logger = logging.getLogger('')
    logger_format = logging.Formatter('%(levelname)s - %(message)s')
    
    logger_handler = logging.StreamHandler()
    logger.setLevel(logging.DEBUG)
    logger_handler.setFormatter(logger_format)
    logger.addHandler(logger_handler)

    if args.config:
        logger.debug(f"Loading configuration overrides from {args.config}")
        try:
            with open(os.path.join(CONF_FOLDER, args.config), 'r') as fh:
                configs_overrides = json.load(fh)
        except:
            logger.critical(f"Failed to load environment configs from {args.config}")
            exit(1)

    environment = ""
    if args.environment:
        logger.debug(f"Loading environment overrides from {args.environment}")

        try:
            if args.environment not in configs_overrides.keys():
                logger.critical(f"environment value must be in {args.config} keys.")
            else:
                environment = args.environment
        except:
            logger.critical(f"Failed to get environment from {args.environment}")
            exit(1)

    try:
        generate_conf_files(configs_overrides, environment)
    except Exception as e:
        logger.critical(e)
        exit(1)
