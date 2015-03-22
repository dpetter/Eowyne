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

from core.security.role import Role, match
from core.shared import log
from natives import Native, relation


# Classes
# -------------------------------------------------------------------------------- #
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
def can_access(route, role_id, owner = None):
    try:
        return access(route, role_id, owner)
    except Exception as e:
        log.warning(str(e))
        return False

def access(route, role_id, owner = None):
    '''
    @returns            True if the given role is allowed to access this route.
                        False if not.
    @raises             ValueError if this route is not defined.
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
    @param role_id:     Identifies the role to perform this check for.
    @param owner:       If None true is returned when permissions are not "None".
                        If true true is returned when permissions are "Own".
                        If false true is returned when permissions are "Foreign".
                        If permissions are "All" true is always returned.
                        In all other cases false is returned.
    '''
    actions = {"/create$": lambda x: x.insert,
               "/[^/]+/delete$": lambda x: x.remove,
               "/[^/]+/update$": lambda x: x.change}
    r = route
    permission = lambda x: x.view
    for key in actions:
        m = re.match("^(.+)" + key, r)
        if m:
            r = m.group(1)
            break
    rules = __lookup__(r)
    if not rules: raise ValueError("No rule define for %s." % (route))
    result = match(rules, role_id)
    if not result: return False
    if owner == True: return permission(result) in ("Own", "All")
    elif owner == False: return permission(result) in ("Foreign", "All")
    else: return permission(result) != "None"

def __lookup__(route):
    '''
    @returns            A list of all rules applying to the given route.
    @param route        Route.
    '''
    items = Rule.all()
    rules = [item for item in items if \
             re.match(re.sub("/$", "/?", item.route) + "$", route)]
    if rules: return rules
    route = re.sub("(?<=.)/[^/]+$", "/", route)
    rules = [item for item in items if re.match(item.route + "$", route)]
    return rules
