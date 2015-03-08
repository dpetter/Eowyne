# -*- coding: utf-8 -*-
#
# Rule
#
# The rule table is used to assign permissions to users, in conjunction with
# roles.
#
# Created by dp on 2015-01-05.
# ================================================================================ #
import re

from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Enum

from core.security.role import Role
from natives import Native, relation
from utility.log import Log


class Rule(Native):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Rules"
    
    permissions         = ("None", "Own", "Foreign", "All")
    
    id                  = Column(Integer, primary_key = True)
    role_id             = Column(Integer, ForeignKey("Roles.id"))
    route               = Column(String(255))
    insert              = Column(Enum(*permissions))
    remove              = Column(Enum(*permissions))
    change              = Column(Enum(*permissions))
    view                = Column(Enum(*permissions))
    
    role                = relation(Role, "role_id")
    
    # ---------------------------------------------------------------------------- #
    def __init__(self, role_id = 0, route = "None", insert = "None",
                 remove = "None", change = "None", view = "None"):
        self.role_id    = role_id
        self.route      = route
        self.insert     = insert
        self.remove     = remove
        self.change     = change
        self.view       = view


# Functions
# -------------------------------------------------------------------------------- #
def access(route, role_id, owner = None): #elevated = False):
    '''
    @returns            -1 if the route is not in the Rules table.
                        0 of the client is not allowed to perform this action.
                        1 if the client is allowed to perform this action.
    @param route:       The address to check. Where the routes ...
                        /something/id
                        /something/id/create
                        /something/id/delete
                        /something/id/update
                        ... match the rule(s) definded for "/something/". They use
                        the appropriate view, insert, remove or change field to
                        determine permissions.
                        "/something/" also matches "/something/" and uses view.
                        "/something/id/reply" matches only the explicitly
                        defined rule "/something/[^/]+/reply" and also uses view.
    @param role_id:     Identifies the clients current role. If no rule for that role
                        can be found the function tries to find one for the role's
                        parent, grandparent, etc. If still none is found it is
                        assumed the client has no rights to access the resource.
    @param elevated:    Whether the client is especially privileged on that route.
                        For example if he has written the associated entry.
    '''
    actions = {"/create$": lambda item: item.insert,
               "/[^/]+/delete$": lambda item: item.remove,
               "/[^/]+/update$": lambda item: item.change}
    for key in actions:
        m = re.match("^(.+)" + key, route)
        if not m: continue
        rules = lookup(m.group(1))
        if not rules: return -1
        result = __match__(rules, role_id)
        if not result: return 0
        return __has_permissions__(actions[key](result), owner)
    rules = lookup(route)
    if not rules: return -1
    result = __match__(rules, role_id)
    if not result: return 0
    return __has_permissions__(result.view, owner)

def lookup(route):
    items = Rule.all()
    rules = [item for item in items if \
             re.match(re.sub("/$", "/?", item.route) + "$", route)]
    if rules: return rules
    route = re.sub("(?<=.)/[^/]+$", "/", route)
    rules = [item for item in items if re.match(item.route + "$", route)]
    return rules

def __match__(rules, role_id):
    role = Role.get(role_id)
    while(role):
        for item in rules:
            if Role.get(item.role_id) == role: return item
        role = Role.get(role.parent_id)
    return None

def __has_permissions__(permissions, owner):
    if owner == True: return 1 * (permissions in ("Own", "All"))
    elif owner == False: return 1 * (permissions in ("Foreign", "All"))
    else: return 1 * (permissions != "None")
