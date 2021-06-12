#! /usr/bin/env python3

# lib imports
from enum import Enum

# project imports
from src.db_manager.db_driver import DBDriver


class ROLES(Enum):
    SUPER_USER = 'super_user'
    ADMIN = 'admin'
    MEMBER = 'member'


def get_user_permissions(user):
    return user.role.permissions.split(',')
