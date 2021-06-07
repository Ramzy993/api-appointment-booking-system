#!/usr/bin/env python3

# lib imports
import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

# project imports
from abs.db_manager.abstract_db_driver import base_model
from abs.db_manager.guid import GUID


class User(base_model):
    __tablename__ = 'users'

    id = Column(GUID(), default=uuid.uuid4, primary_key=True)
    username = Column(String(128), unique=True, nullable=False, primary_key=True)
    password = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    email_confirmed = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=False)

    role_id = Column(GUID, ForeignKey('roles.id'), nullable=False)

    role = relationship("Role", backref="users", uselist=False)
    appointments = relationship("Appointment", backref="user")

    def __init__(self, name, username, password, email, role_id):
        self.name = name
        self.username = username
        self.password = generate_password_hash(password=password)
        self.email = email
        self.role_id = role_id

    def __repr__(self):
        return f"User id: {self.id}. Name: {self.name}. and UserName: {self.username}."

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            "email_confirmed": self.email_confirmed,
            "is_active": self.is_active,
            "appointments": self.appointments
        }
