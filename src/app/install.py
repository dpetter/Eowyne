# -*- coding: utf-8 -*-
#
# Installs basic database.
#
# Created on 2015-01-24.
# ================================================================================ #
import getpass
import importlib
import pkgutil

from flask.app import Flask

from app.configuration import Configuration
from core.navigation.menu import Menubar, Menuitem
from core.security.role import Role
from core.security.rule import Rule
from core.security.session import Session
from core.security.user import User
from core.shared import db
from core.utility.keyutility import hash_password


# Core data
# -------------------------------------------------------------------------------- #
roles = [# parent, name, description
Role(None,  "Root",             "Applies to everyone."),
Role(1,     "Guest",            "Applies to clients who aren't logged in."),
Role(1,     "User",             "Applies to all logged in users."),
Role(3,     "Locked",
     "Applies to clients who haven't activated their account yet."),
Role(3,     "Administrator",    "Has the most extensive permissions.")
]

rules = [# role_id, pattern, insert, delete, update, view, search
Rule(1, "/",                "None", "None", "None", "All"),
Rule(1, "/pages/",          "None", "None", "None", "All"),
Rule(2, "/register/",       "None", "None", "None", "All"),
Rule(2, "/reset/",          "None", "None", "None", "All"),
Rule(2, "/signin",          "None", "None", "None", "All"),
Rule(3, "/signout",         "None", "None", "None", "All"),
Rule(5, "/",                "All",  "All",  "All",  "All"),
Rule(5, "/pages/",          "All",  "All",  "All",  "All"),
Rule(5, "/administration",  "All",  "All",  "All",  "All"),
Rule(5, "/roles/",          "All",  "All",  "All",  "All"),
Rule(5, "/rules/",          "All",  "All",  "All",  "All"),
Rule(5, "/menus/",          "All",  "All",  "All",  "All"),
Rule(5, "/routes",          "None", "None", "None", "All"),
Rule(5, "/plugins",         "None", "None", "None", "All"),
Rule(3, "/personal/",       "None", "None", "None", "All")
]

menubars = [# name
Menubar("personal"),
Menubar("administration"),
Menubar("rule"),
Menubar("role"),
Menubar("menu"),
Menubar("main"),
Menubar("extended")
]

menuitems = [# menubar, weight, name, image, flags, address
Menuitem(1, 0,  "My Account",       "user",             0,  "/personal"),
Menuitem(1, 10, "Sign in",          "log-in",           0,  "/signin"),
Menuitem(1, 10, "Sign out",         "log-out",          0,  "/signout"),
Menuitem(1, 1,  "Administration",   "cog",              0,  "/administration"),
Menuitem(2, 0,  "Rules",            "",                 0,  "/rules"),
Menuitem(2, 1,  "Roles",            "",                 0,  "/roles"),
Menuitem(2, 2,  "Menus",            "",                 0,  "/menus"),
Menuitem(2, 3,  "Routes",           "",                 0,  "/routes"),
Menuitem(2, 4,  "Plugins",          "",                 0,  "/plugins"),
Menuitem(3, 0,  "",                 "plus",             0,  "/rules/create"),
Menuitem(3, 1,  "",                 "remove",           0,  "/rules/<id>/delete"),
Menuitem(3, 2,  "",                 "pencil",           0,  "/rules/<id>/update"),
Menuitem(4, 0,  "",                 "plus",             0,  "/roles/create"),
Menuitem(4, 1,  "",                 "remove",           0,  "/roles/<id>/delete"),
Menuitem(4, 2,  "",                 "pencil",           0,  "/roles/<id>/update"),
Menuitem(5, 0,  "",                 "plus",             0,  "/menus/create"),
Menuitem(5, 1,  "",                 "remove",           0,  "/menus/<id>/delete"),
Menuitem(5, 2,  "",                 "pencil",           0,  "/menus/<id>/update"),
Menuitem(6, 0,  "",                 "home",             0,  "/"),
Menuitem(6, 1,  "About us",         "",                 0,  "/pages/about"),
Menuitem(7, 0,  "Contact",          "",                 0,  "/pages/contact"),
Menuitem(7, 1,  "Legal",            "",                 0,  "/pages/legal")
]


# Initialise application
# -------------------------------------------------------------------------------- #
print("Initializing installer ...")
app = Flask(__name__,
            static_folder = Configuration["static_dir"],
            template_folder = Configuration["template_dir"])
app.secret_key = Configuration["secret_key"]
print("Connecting to database ...")
app.config["SQLALCHEMY_DATABASE_URI"] = Configuration["sql_db_uri"]
db.app = app
db.init_app(app)

# Load plugin installers
# -------------------------------------------------------------------------------- #
path = ["./src/plugins"]
prefix = "plugins."
modules = []
for module_loader, name, ispkg in pkgutil.walk_packages(path, prefix):
    if not name.endswith("__install__"): continue
    module = importlib.import_module(name)
    if not hasattr(module, "install"): continue
    modules.append(module)

# Install application
# -------------------------------------------------------------------------------- #
print("Installing core data ...")
db.create_all()
if Role.total() == 0:
    print("Installing roles ...")
    for item in roles: item.create()
if Rule.total() == 0:
    print("Installing rules ...")
    for item in rules: item.create()
if Menubar.total() == 0:
    print("Installing menubars ...")
    for item in menubars: item.create()
if Menuitem.total() == 0:
    print("Installing menuitems ...")
    for item in menuitems: item.create()
if User.total() == 0:
    print("Installing users ...")
    print("- - - - - - - - - - - - - - - - - - -")
    print("Creating anonymous account ...")
    username    = input("Anonymous username: ")
    print("Create admin account ...")
    user = User(2, "", username, "", "")
    user.create()
    print("- - - - - - - - - - - - - - - - - - -")
    print("Creating administrator account ...")
    username    = input("Administrator username: ")
    email       = input("Administrator email:    ")
    password    = getpass.getpass("Administrator password: ")
    user = User(5, email, username, hash_password(password), "")
    user.create()
    print("- - - - - - - - - - - - - - - - - - -")
Session.total()
print("Installing plugin data ...")
for module in modules: module.install()
