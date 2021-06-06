#!/usr/bin/env python3

# lib imports
from flask import Flask


# project imports
from abs.common.config_manager.config_manager import ConfigManager
from abs.common.log_manager.log_manger import LogManager


flask_app = Flask(import_name=__name__)


def creat_app():

    with flask_app.app_context():
        flask_app.config['SECRET_KEY'] = ConfigManager().get_str('FLASK_APP', 'app_secret')
        flask_app.config['ENV'] = ConfigManager().get_str('FLASK_APP', 'env')

        LogManager().info("Flask App created.")


def start_app():
    host = ConfigManager().get_str('FLASK_APP', 'host', fallback='localhost')
    port = ConfigManager().get_int('FLASK_APP', 'port', fallback=8008)
    debug = ConfigManager().get_bool('FLASK_APP', 'debug', fallback=False)

    creat_app()

    LogManager().info(f"App is running on host name: {host}, port: {port}, with debug mode: {debug}")
    flask_app.run(host=host, port=port, debug=debug, use_reloader=False)


@flask_app.route('/', methods=['GET'])
def index():
    return {'status': 'SUCCESS'}

