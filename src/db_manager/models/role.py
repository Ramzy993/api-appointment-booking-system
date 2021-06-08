#!/usr/bin/env python3

# lib imports
import uuid
from sqlalchemy import Column, String, Text, JSON
from sqlalchemy.orm import relationship

# project imports
from src.db_manager.abstract_db_driver import base_model
from src.db_manager.guid import GUID


class Role(base_model):
    __tablename__ = 'roles'

    id = Column(GUID(), default=uuid.uuid4, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    permissions = Column(Text, nullable=False)

    def __init__(self, name, description, permissions):
        self.name = name
        self.description = description
        self.permissions = permissions

    def __repr__(self):
        return f"Role id: {self.id}. Name: {self.name}. and Description: {self.description}. Permissions: {self.permissions}"

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'permissions': self.permissions
        }
