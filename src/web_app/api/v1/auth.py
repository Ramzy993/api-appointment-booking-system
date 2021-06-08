#!/usr/bin/env python3

# lib imports
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from werkzeug.security import check_password_hash

# project imports
from src.common.log_manager.log_manger import LogManager
from src.common.utils.miscs import ROLES
from src.db_manager.db_driver import DBDriver
from src.web_app.services.standard_response import StandardResponse


auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username is None or password is None:
        return StandardResponse('username and password must be in json data', 400).to_json()

    user = (DBDriver().get_users(username=username) or [None])[0]

    if user is None:
        return StandardResponse('this user is not registered', 401).to_json()

    if  not check_password_hash(user.password, password):
        return StandardResponse('wrong password', 401).to_json()

    LogManager().info(f"this user {username} is authenticated.")
    access_token = create_access_token(identity=username)
    return StandardResponse({"access_token": access_token}, 200).to_json()


@auth_blueprint.route('/register', methods=['POST'])
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    name = request.json.get("name", None)
    email = request.json.get("email", None)

    if None in [username, password, name, email]:
        return StandardResponse('username, password, name, email must be in json data', 400).to_json()

    user = (DBDriver().get_users(username=username) or [None])[0]

    if user is not None:
        return StandardResponse('this username is already registered', 401).to_json()

    role_id = DBDriver().get_role(name=ROLES.MEMBER.value).id
    user = DBDriver().create_user(username=username, password=password, name=name, email=email, role_id=role_id)
    LogManager().info(f"user created with username {username}.")
    return StandardResponse(user, 200).to_json()
