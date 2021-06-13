#!/usr/bin/env python3

# lib imports
from abc import ABCMeta, abstractmethod
from sqlalchemy.ext.declarative import declarative_base


base_model = declarative_base()


class AbstractDBDriver(metaclass=ABCMeta):
    def __init__(self):
        pass

    def __del__(self):
        pass

    @abstractmethod
    def create_user(self, username, password, name, email, role_id):
        pass

    @abstractmethod
    def get_users(self, id=None, username=None, name=None, email=None, role_id=None):
        pass

    @abstractmethod
    def update_user(self, id, username=None, password=None, name=None, email=None):
        pass

    @abstractmethod
    def update_user_role(self, id, role_id=None):
        pass

    @abstractmethod
    def update_user_activation(self, id, is_active=None):
        pass

    @abstractmethod
    def update_user_confirmed_email(self, id, email_confirmed=None):
        pass

    @abstractmethod
    def delete_user(self, id):
        pass

    @abstractmethod
    def create_role(self, name, permissions, description=None):
        pass

    @abstractmethod
    def get_role(self, name):
        pass

    @abstractmethod
    def update_role(self, name, permissions=None, description=None):
        pass

    @abstractmethod
    def create_appointment(self, title, appointment_start_datetime, appointment_end_datetime, user_id, description=None):
        pass

    @abstractmethod
    def get_appointments(self, id=None, title=None, appointment_start_datetime=None, appointment_end_datetime=None, user_id=None):
        pass

    @abstractmethod
    def update_appointment(self, id, title=None, appointment_start_datetime=None, appointment_end_datetime=None, description=None):
        pass

    @abstractmethod
    def delete_appointment(self, id):
        pass
