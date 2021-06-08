#!/usr/bin/env python3

# lib imports
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

# project imports
from src.common.utils.miscs import ROLES
from src.db_manager.db_driver import DBDriver
from src.web_app.services.standard_response import StandardResponse


user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    current_username = get_jwt_identity()
    user = (DBDriver().get_users(username=current_username) or [None])[0]

    if user is None:
        return StandardResponse('this user is not registered', 401).to_json()

    if 'get_users' not in user.role.permissions["permissions"]:
        return StandardResponse('this user is not authorized to do this action.', 403).to_json()

    users = DBDriver().get_users()
    return StandardResponse(users, 200).to_json()


@user_blueprint.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_username = get_jwt_identity()
    user = (DBDriver().get_users(username=current_username) or [None])[0]

    if user is None or not user.is_active:
        return StandardResponse('this user is not registered or not activated.', 401).to_json()

    if user_id != user.id:
        return StandardResponse('this user is not authorized to see this data.', 403).to_json()

    return StandardResponse(user, 200).to_json()


@user_blueprint.route('/users/<user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(user_id):
    current_username = get_jwt_identity()

    user = (DBDriver().get_users(username=current_username) or [None])[0]

    if user is None or not user.is_active:
        return StandardResponse('this user is not registered or not activated.', 401).to_json()

    if 'update_user' not in user.role.permissions["permissions"]:
        return StandardResponse('this user is not authorized to do this action.', 403).to_json()

    else:
        json_data = request.json

        if user.role.name == ROLES.SUPER_USER.value:
            if user_id == user.id:
                DBDriver().update_user(id=user_id, username=json_data["username"], password=json_data["password"],
                                       name=json_data["name"], email=json_data["email"])
            else:
                role_id = DBDriver().get_role(name=json_data["role"]).id
                user = DBDriver().update_user_by_admin(id=user_id, role_id=role_id, is_active=json_data["is_active"])
                return StandardResponse(user, 200).to_json()
        elif user_id == user.id:
            user = DBDriver().update_user(id=user_id, username=json_data["username"], password=json_data["password"],
                                          e=json_data["name"], email=json_data["email"])
            return StandardResponse(user, 200).to_json()
        else:
            return StandardResponse('this user is not authorized to update this data.', 403).to_json()


@user_blueprint.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_username = get_jwt_identity()
    user = (DBDriver().get_users(username=current_username) or [None])[0]

    if user is None:
        return StandardResponse('this user is not registered', 401).to_json()

    if 'delete_user' not in user.role.permissions["permissions"]:
        return StandardResponse('this user is not authorized to do this action.', 403).to_json()

    DBDriver().delete_user(id=user_id)
    return StandardResponse("user deleted successfully", 200).to_json()


