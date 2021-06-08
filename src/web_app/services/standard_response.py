#!/usr/bin/env python3

# lib imports
import json
import uuid
import datetime
from flask import jsonify

# project imports
from src.db_manager.models.user import User
from src.db_manager.models.role import Role
from src.db_manager.models.appointment import Appointment


def default_serializer(obj):
    if isinstance(obj, (User, Role, Appointment)):
        return obj.to_json()
    elif type(obj) is uuid.UUID:
        return str(obj)
    elif type(obj) is datetime.datetime:
        return obj.strftime("%d-%b-%Y %H:%M:%S")

    raise Exception(f"Can not serialize: {str(type(obj))}")


def serializer(data, indent=4):
    return json.dumps(data, default=default_serializer, indent=indent)


class StandardResponse:

    def __init__(self, data, status):
        self.data = data
        self.status = status

    def to_json(self):
        return serializer({"data": self.data}), self.status

