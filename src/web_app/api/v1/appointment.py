#!/usr/bin/env python3

# lib imports
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

# project imports
from src.db_manager.db_driver import DBDriver
from src.web_app.services.standard_response import StandardResponse


appointment_blueprint = Blueprint('appointment_blueprint', __name__)


@appointment_blueprint.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    current_username = get_jwt_identity()
    user = (DBDriver().get_users(username=current_username) or [None])[0]

    if user is None:
        return StandardResponse('this user is not registered', 401).to_json()

    if 'get_appointments' not in user.role.permissions["permissions"]:
        return StandardResponse('this user is not authorized to do this action.', 403).to_json()

    else:
        appointments = DBDriver().get_appointments()
        return StandardResponse(appointments, 200).to_json()


@appointment_blueprint.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    current_username = get_jwt_identity()
    user = (DBDriver().get_users(username=current_username) or [None])[0]

    if user is None:
        return StandardResponse('this user is not registered', 401).to_json()

    if 'create_appointment' not in user.role.permissions["permissions"]:
        return StandardResponse('this user is not authorized to do this action.', 403).to_json()

    else:
        title = request.json.get("title", None)
        description = request.json.get("description", None)
        appointment_datetime = request.json.get("appointment_datetime", None)
        appointment_period = request.json.get("appointment_period", None)
        appointment = DBDriver().create_appointment(title=title, description=description, appointment_datetime=appointment_datetime,
                                                    appointment_period=appointment_period, user_id=user.id)
        return StandardResponse(appointment, 200).to_json()


@appointment_blueprint.route('/appointments/<app_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def edit_appointment(app_id):
    current_username = get_jwt_identity()
    user = (DBDriver().get_users(username=current_username) or [None])[0]

    if user is None:
        return StandardResponse('this user is not registered', 401).to_json()

    if 'edit_appointment' not in user.role.permissions["permissions"]:
        return StandardResponse('this user is not authorized to do this action.', 403).to_json()

    else:
        appointment = (DBDriver().get_appoitments(id=app_id) or [None])[0]
        if appointment is None:
            return StandardResponse('this appointment does not exist.', 401).to_json()
        else:
            title = request.json.get("title", None)
            description = request.json.get("description", None)
            appointment_datetime = request.json.get("appointment_datetime", None)
            appointment_period = request.json.get("appointment_period", None)
            appointment = DBDriver().update_appointment(id=app_id, title=title, description=description,
                                                        appointment_datetime=appointment_datetime,
                                                        appointment_period=appointment_period)
            return StandardResponse(appointment, 200).to_json()


@appointment_blueprint.route('/appointments/<app_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(app_id):
    current_username = get_jwt_identity()
    user = (DBDriver().get_users(username=current_username) or [None])[0]

    if user is None:
        return StandardResponse('this user is not registered', 401).to_json()

    if 'delete_appointment' not in user.role.permissions["permissions"]:
        return StandardResponse('this user is not authorized to do this action.', 403).to_json()

    DBDriver().delete_appointment(id=app_id)
    return StandardResponse("user deleted successfully", 200).to_json()


