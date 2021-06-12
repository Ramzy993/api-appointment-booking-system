#!/usr/bin/env python3

# lib imports
from datetime import timedelta

from flask import Flask
# from flask_jwt_extended import create_access_token
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

# project imports
from src.common.config_manager.config_manager import ConfigManager
from src.common.log_manager.log_manger import LogManager
from src.db_manager.db_driver import DBDriver
from src.web_app.api.v1.auth import auth_blueprint
from src.web_app.api.v1.user import user_blueprint
from src.web_app.api.v1.appointment import appointment_blueprint

flask_app = Flask(import_name=__name__)


def creat_app():

    with flask_app.app_context():
        flask_app.config['SECRET_KEY'] = ConfigManager().get_str('FLASK_APP', 'app_secret')
        flask_app.config['ENV'] = ConfigManager().get_str('FLASK_APP', 'env')

        LogManager().info("Flask App created.")

    DBDriver()
    JWTManager(flask_app)

    # API V1 Registration
    abs_api_v1_base_url = '/api/v1'
    flask_app.register_blueprint(auth_blueprint, url_prefix=abs_api_v1_base_url)
    flask_app.register_blueprint(user_blueprint, url_prefix=abs_api_v1_base_url)
    flask_app.register_blueprint(appointment_blueprint, url_prefix=abs_api_v1_base_url)


def start_app():
    host = ConfigManager().get_str('FLASK_APP', 'host', fallback='localhost')
    port = ConfigManager().get_int('FLASK_APP', 'port', fallback=8008)
    debug = ConfigManager().get_bool('FLASK_APP', 'debug', fallback=False)

    creat_app()

    flask_app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=True)
    LogManager().info(f"App is running on host name: {host}, port: {port}, with debug mode: {debug}")


@flask_app.route('/', methods=['GET'])
def index():
    return {'status': 'SUCCESS'}

