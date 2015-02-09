# -*- coding: utf-8 -*-
#
# Role
#
# See Rule for documentation.
#
# Created by dp on 2015-01-05.
# ================================================================================ #
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from natives import Native, recursion


class Role(Native):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Roles"
    
    id                  = Column(Integer, primary_key = True)
    parent_id           = Column(Integer, ForeignKey("Roles.id"))
    name                = Column(String(255), unique = True)
    description         = Column(String(255))
    
    parent              = recursion("parent_id")
    
    # ---------------------------------------------------------------------------- #
    def __init__(self, parent_id = 0, name = None, description = None):
        self.parent_id      = parent_id
        self.name           = name
        self.description    = description
