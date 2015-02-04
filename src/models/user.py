# -*- coding: utf-8 -*-
#
# User
#
# Users have a (display) name, an email and a password.
# Every user has a role that defines his permissions.
# This module also provides two filter classes. For security reasons "User"
# should never be used outside of administrative pages. For displaying information
# about the creator of a page, comment, etc. use the filter class "Editor".
# The filter class "Client" is part of the global scope and holds all information
# about the user making the request that is currently processed, such as
# his role and his name.
#
# Created by dp on 2015-01-05.
# ================================================================================ #
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.types import Integer, String

from models import Model
from natives.role import Role
from natives import relation


class User(Model):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Users"
    
    id                  = Column(Integer, primary_key = True)
    createdOn           = Column(DateTime)
    changedOn           = Column(DateTime)
    role_id             = Column(Integer, ForeignKey("Roles.id"))
    email               = Column(String(255), unique = True)
    name                = Column(String(255), unique = True)
    password            = Column(String(255))
    generated           = Column(String(32))
    
    role = relation(Role, "role_id")
    
    # ---------------------------------------------------------------------------- #
    def __init__(self, role = None, email = None, name = None, password = None,
                 generated = None):
        self.role           = role
        self.email          = email
        self.name           = name
        self.password       = password
        self.generated      = generated
    
    # ---------------------------------------------------------------------------- #
    def __eq__(self, other):
        if not hasattr(other, "id"): return False
        return self.id == other.id


class Editor(User):
    __mapper_args__     = {"include_properties": ["id", "name"]}


class Client(User):
    __mapper_args__     = {"include_properties": ["id", "name", "role_id"]}