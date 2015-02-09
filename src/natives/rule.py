# -*- coding: utf-8 -*-
#
# Rule
#
# The rule table is used to assign permissions to users, in conjunction with
# roles.
#
# Roles
#
# The roles "Root", "Guest", "User", "Locked" and "Administrator" are preinstalled.
# Rules that apply to Root apply, to every visitor to the page (logged in or not).
# Rules that apply to Guest apply to visitors that are not logged in. So only
# Guests should have permission to things like "/signon" and "/register".
# Rules that apply to User, apply to ever logged in client.
# Locked is for Users that have just registered but not activated their account.
#
# So a short recap:
# Grant permissions to anything everyone should be able to use to Root.
# Grant permissions to anything only members should see to User.
# Grant permissions to administrative functionality to Administrators.
#
# You can extend a role in order to create your own groups. A role extending User
# inherits all the permissions User has except where overridden. So it's easy to
# add some functionality that is only visible to say "Premium" members. All you
# have to do is extend User (Premium will now be able to access everything a
# normal User can access) and give only Premium permissions to your new
# functionality.
#
#
# Rules proper
#
# Rules have a route and various permission fields (insert, remove, ...) and are
# linked to a role each.
#
# Permissions are straightforward. If there is a rule for a route and a role
# then an user with this role can (inside this route):
# Not view anything if "view"="None". Example: admin page.
# View resources he created himself if view="Own" but not those other users
# created. Example: personal site.
# View everything if view="All". Example: comment.
#
# Routes are resource locators. On a technical level they are identical to the
# routes you use in your blueprints. When you are adding a blueprint to the
# project you must also define rules for your routes, otherwise the security
# system won't let users pass through.
# There's two caveats: routes are build after special rules and they are
# regular expressions.
#
# There's two kind of routes: folders and actions.
# Think of folders as your plain old file system folders.
# Inside a folder there can be a multitude of objects and users can create,
# view, delete and change objects or search for them.
# To control what users can see use all the permissions.
#
#
# A practical example:
# You have a blog that all users can see but only blogger(s) can write for.
# Then you'd define the following routes:
# user       /blog/    with view=All, search=All, all other=None
# blogger    /blog/    with create=Own, remove=Own, change=Own
#
# Perhaps you'd also want to have an admin able to remove unwanted posts:
# admin      /blog/    with remove=All
#
# Since both admin and blogger extend user they both inherit the permissions
# to view blog entries.
# The trailing slash tells the security system that this is a folder. It will
# then automatically allow the routes /blog, /blog/<someid>, /blog/create
# /blog/<someid>/delete, /blog/<someid>/update, and /blog/find.
# That's of course unless you've set permissions to None.
#
# Since the security system doesn't know what objects you are presenting in the
# blueprint it cannot check whether the requesting client is the owner of this
# object at this point. If you want to use this feature use the (class)method
# Rule.access(route, role, isOwner) in your blueprint's function after you've
# determined whether the user is the object's owner and return forbidden() if
# she is not.
#
# The second kind of routes are actions. Action routes do not end with a slash.
# Watch:
# user    /blog/random    with view=All
# This allows all users to use the /blog/random route, which could display a
# random blog page.
#
# You can also define actions for objects.
# user    /blog/<id>/comment    with view=All
# This allows users to comment on all blog posts.
#
# Since actions are ... uhm, actions, they do not need a create, modify or
# delete permissions. You only need to set the view permissions. Nothings gonna
# happen if you're setting other permissions.
# Also: There's a permission I haven't mentioned yet.
# that is view="Foreign"
# This allows an user to execute an action only on objects other user created
# but not on his own. Like so:
# user    /blog/<id>/rate    with view=Foreign
# You can theoretically also use this on objects but letting users delete
# the stuff others have written but not what they themselves wrote is probably
# not a good idea. Or maybe it is. You know best what you are using this for.
#
# Created by dp on 2015-01-05.
# ================================================================================ #
import re

from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Enum

from natives import Native, relation
from natives.role import Role
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
    search              = Column(Enum(*permissions))
    
    role                = relation(Role, "role_id")
    
    # ---------------------------------------------------------------------------- #
    def __init__(self, role_id = 0, route = None, insert = None, remove = None,
                 change = None, view = None, search = None):
        self.role_id    = role_id
        self.route      = route
        self.insert     = insert
        self.remove     = remove
        self.change     = change
        self.view       = view
        self.search     = search
    
# -------------------------------------------------------------------------------- #
def access(route, role_id, isOwner = False):
    '''
    @returns        -1 if the route is not in the Rules table.
                    0 of the client is not allowed to perform this action.
                    1 if the client is allowed to perform this action.
    @param route:   The address to check. Either request.path or a link on the
                    site.
    @param role_id: The clients current role_id.
    @param isOwner: Whether the client owns the item associated with the requested
                    action.
    '''
    return 1
    # This here is trying to figure out if this is a standard action (create,
    # delete, update) and use the appropriate permission field. If it is
    # not "view" is used.
    actions = {"/create$": lambda item: item.insert,
               "/[^/]+/delete$": lambda item: item.remove,
               "/[^/]+/update$": lambda item: item.change}
    try:
        for key, value in actions.items():
            if re.match("^.+" + key, route):
                item = lookup(re.sub(key, "/", route), role_id)
                if item: return has_permissions(value(item), isOwner)
        item = lookup(route, role_id)
        if item: return has_permissions(item.view, isOwner)
        return 0
    except ValueError:
        Log.warning(__name__, "Invalid route accessed (%s)." % (route))
        return -1

# -------------------------------------------------------------------------------- #
def has_permissions(permissions, isOwner):
    if permissions == "None": return 0
    if isOwner: return (permissions == "Own" or permissions == "All")
    else: return (permissions == "Foreign" or permissions == "All")

# -------------------------------------------------------------------------------- #
def lookup(route, role_id):
    '''
    Tries to look up the entry in the Rules table whose route matches route.
    If no rule is found a ValueError is raised. Otherwise the function finds
    the rule that applies to the given role most directly and returns it.
    If there is a rule for the given role that is returned.
    If not the function tries to find a rule for the parent, grandparent, ...
    If there is not found a matching still the function returns None.
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
