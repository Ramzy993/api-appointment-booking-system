#!/usr/bin/env python3

# lib imports
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# project imports
from src.db_manager.abstract_db_driver import base_model
from src.db_manager.guid import GUID


class Appointment(base_model):
    __tablename__ = 'appointments'

    id = Column(GUID(), default=uuid.uuid4, primary_key=True)
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    appointment_datetime = Column(DateTime, nullable=False)
    appointment_period = Column(String(32), nullable=False)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user_id = Column(GUID, ForeignKey('users.id'), nullable=False)

    def __init__(self, title, description, appointment_datetime, appointment_period, user_id):
        self.title = title
        self.description = description
        self.appointment_datetime = appointment_datetime
        self.appointment_period = appointment_period
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.user_id = user_id

    def __repr__(self):
        return f"Role id: {self.id}. Title: {self.title}. and Description: {self.description}."

    def to_json(self):
        return {
            'id': self.id,
            'description': self.description,
            'appointment_datetime': self.appointment_datetime,
            'appointment_period': self.appointment_period,
            'user_id': self.user_id
        }
