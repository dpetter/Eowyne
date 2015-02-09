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

from core.natives.role import Role
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


# -------------------------------------------------------------------------------- #
def access(route, role_id, elevated = False):
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
    try:
        # This here is trying to figure out if this is a standard action (create,
        # delete, update) and use the appropriate permission field.
        actions = {"/create$": lambda item: item.insert,
                   "/[^/]+/delete$": lambda item: item.remove,
                   "/[^/]+/update$": lambda item: item.change}
        for key, value in actions.items():
            if re.match("^.+" + key, route):
                item = lookup(re.sub(key, "/", route), role_id)
                if item: return __has_permissions__(value(item), elevated)
        # If it is not a standard action use view.
        item = lookup(route, role_id)
        if item: return __has_permissions__(item.view, elevated)
        return 0
    except ValueError:
        Log.warning(__name__, "Invalid route accessed (%s)." % (route))
        return -1

# -------------------------------------------------------------------------------- #
def lookup(route, role_id):
    '''
    @returns            The item in the route table that matches route and applies
                        to the role identified by role_id. If there's no rule for
                        that role None is returned.
                        If there's no matching route a ValueError is raised.
    @param route:       The address to check.
    @param role_id:     The clients current role_id.
    '''
    Log.debug(__name__, route)
    items = Rule.all()
    # Try to match the route directly. This will collect the correct results for
    # all actions that are explicitly defined (f.i. /mailbox/[^/]+/reply) and for
    # the create, delete, update and find actions of an object folder.
    rules = [item for item in items if \
             re.match(re.sub("/$", "/?", item.route) + "$", route)]
    # If there was no rule found assume this is an object view action.
    # Try to remove the object identifier (f.i. /mailbox/mail123 becomes
    # /mailbox/) and to match again.
    if not rules:
        route = re.sub("(?<=.)/[^/]+$", "/", route)
        rules = [item for item in items if re.match(item.route + "$", route)]
    # If there still was no matching rule found raise a ValueError.
    if not rules: raise ValueError()
    role = Role.get(role_id)
    while(role):
        for item in rules:
            if Role.get(item.role_id) == role: return item
        role = Role.get(role.parent_id)
    return None

# -------------------------------------------------------------------------------- #
def __has_permissions__(permissions, elevated):
    '''
    Iternal only.
    '''
    if permissions == "None": return 0
    if elevated: return 1 * (permissions == "Own" or permissions == "All")
    else: return 1 * (permissions == "Foreign" or permissions == "All")
