#!/usr/bin/env python3

# lib imports
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# project imports
from abs.common.log_manager.log_manger import LogManager
from abs.common.config_manager.config_manager import ConfigManager
from abs.common.exception_handler.base_exception import AbsBaseException
from abs.common.utils.singletone import Singleton
from abs.db_manager.abstract_db_driver import base_model, AbstractDBDriver

from abs.db_manager.models.user import User
from abs.db_manager.models.role import Role
from abs.db_manager.models.appointment import Appointment


class DatabaseDriverException(AbsBaseException):
    """
    this class is used to raise exception related to database
    """


@Singleton
class DBDriver(AbstractDBDriver):

    def __init__(self):
        super().__init__()
        self.dialect = ConfigManager().get_str('DATABASE', 'dialect', fallback='sqlite')
        self.database_name = ConfigManager().get_str('DATABASE', 'database_name')
        self.host = ConfigManager().get_str('DATABASE', 'host')
        self.username = ConfigManager().get_str('DATABASE', 'username')
        self.password = ConfigManager().get_str('DATABASE', 'password')

        if self.dialect == 'sqlite':
            if not os.path.isdir('tmp'):
                os.makedirs('tmp')
            self.connection_string = self.dialect + ":///tmp/" + self.database_name + '.db'
        else:
            self.connection_string = self.dialect + "://" + self.username + ":" + self.password + "@" + \
                                     self.host + "/" + self.database_name

        self.engine = create_engine(self.connection_string)

        base_model.metadata.create_all(self.engine)

        self.connection = self.engine.connect()
        LogManager().info("connected to database")

        self.session = sessionmaker(bind=self.engine)()

        # self.__seed_db()

    def __del__(self):
        self.connection.close()
        LogManager().info("disconnected to database")

    def __commit(self, model):
        self.session.add(model)
        self.session.commit()
        return model

    def __dynamic_filter(self, model, args_dict):
        if model is None:
            raise DatabaseDriverException("cannot find model")

        args_dict.pop('self')

        query = self.session.query(model)
        model_attr_dict = vars(model)

        for key, value in args_dict.items():
            if value is not None and key in model_attr_dict:
                attr = getattr(model, key)
                query = query.filter(attr == value)

        return query

    def __dynamic_update(self, model, args_dict):
        if model is None:
            raise DatabaseDriverException("cannot find model")

        args_dict.pop('self')
        args_dict.pop('id', None)

        model_attr_dict = vars(model)

        for key, value in args_dict.items():
            if value is not None and key in model_attr_dict:
                setattr(model, key, value)

        return model
    
    def create_user(self, username, password, name, email, role_id):
        try:
            user = User(username, password, name, email, role_id)
            return self.__dynamic_commit(user)

        except Exception as e:
            self.session.rollback()
            LogManager().error(f"Database Error: {e}")
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def get_users(self, id=None, username=None, name=None, email=None, role_id=None):
        try:
            users = self.__dynamic_filter(User, locals()).all()
            return users

        except Exception as e:
            self.session.rollback()
            LogManager().error(f"Database Error: {e}")
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def update_user(self, id, username=None, password=None, name=None, email=None, email_confirmed=None, is_active=None):
        try:
            user = self.session.query(User).filter_by(id=id).first()
            user = self.__dynamic_update(User, locals())
            self.session.commit()
            return user

        except Exception as e:
            self.session.rollback()
            LogManager().error(f"Database Error: {e}")
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def update_user_role(self, id, role_id):
        try:
            user = self.session.query(User).filter_by(id=id).first()
            user = self.__dynamic_update(user, locals())
            self.session.commit()
            return user

        except Exception as e:
            self.session.rollback()
            LogManager().error(f"Database Error: {e}")
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def delete_user(self, id):
        try:
            self.session.query(User).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            LogManager().error(f"Database Error: {e}")
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def create_role(self, name, permissions, description=None):
        try:
            role = Role( name, permissions, description)
            return self.__dynamic_commit(role)

        except Exception as e:
            self.session.rollback()
            LogManager().error(f"Database Error: {e}")
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def get_role(self, name):
        try:
            role = self.__dynamic_filter(Role, locals()).all()
            return role

        except Exception as e:
            self.session.rollback()
            LogManager().error(f"Database Error: {e}")
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def update_role(self, name, permissions=None, description=None):
        try:
            role = self.session.query(Role).filter_by(name=name).first()
            role = self.__dynamic_update(role, locals())
            self.session.commit()
            return role

        except Exception as e:
            self.session.rollback()
            LogManager().error(f"Database Error: {e}")
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def delete_role(self, name):
        try:
            self.session.query(Role).filter_by(name=name).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            LogManager().error(f"Database Error: {e}")
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def create_appointment(self, title, appointment_datetime, appointment_period, user_id, description=None):
        try:
            appointment = Appointment(title, appointment_datetime, appointment_period, user_id, description)
            return self.__dynamic_commit(appointment)

        except Exception as e:
            self.session.rollback()
            LogManager().error(f"Database Error: {e}")
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def get_appointments(self, title, appointment_datetime, appointment_period, user_id, description=None):
        try:
            appointments = self.__dynamic_filter(Appointment, locals()).all()
            return appointments

        except Exception as e:
            self.session.rollback()
            LogManager().error(f"Database Error: {e}")
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def update_appointment(self, id, title=None, appointment_datetime=None, appointment_period=None, description=None):
        try:
            appointment = self.session.query(Appointment).filter_by(id=id).first()
            appointment = self.__dynamic_update(appointment, locals())
            self.session.commit()
            return appointment

        except Exception as e:
            self.session.rollback()
            LogManager().error(f"Database Error: {e}")
            raise DatabaseDriverException(f"Database ERROR: {e}")

    def delete_appointment(self, id):
        try:
            self.session.query(Appointment).filter_by(id=id).delete()
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            LogManager().error(f"Database Error: {e}")
            raise DatabaseDriverException(f"Database ERROR: {e}")

