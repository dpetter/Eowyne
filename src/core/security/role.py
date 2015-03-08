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


# Classes
# -------------------------------------------------------------------------------- #
class Role(Native):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Roles"
    
    id                  = Column(Integer, primary_key = True)
    parent_id           = Column(Integer, ForeignKey("Roles.id"))
    name                = Column(String(255), unique = True)
    description         = Column(String(255))
    
    parent              = recursion("parent_id")
    
    # ---------------------------------------------------------------------------- #
    def __init__(self, parent_id = 0, name = "", description = ""):
        self.parent_id      = parent_id
        self.name           = name
        self.description    = description


# Functions
# -------------------------------------------------------------------------------- #
def match(rules, role_id):
    '''
    @returns            The rule that applies to the given role.
    @param rules        A list of rules to check.
    @param role_id      Determines which role to match against. If there's no
                        matching rule found for this role, the function
                        recursively tries to match against its parent,
                        grandparent and so on.
    '''
    role = Role.get(role_id)
    while(role):
        for item in rules:
            if Role.get(item.role_id) == role: return item
        role = Role.get(role.parent_id)
    return None
