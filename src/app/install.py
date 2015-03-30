# -*- coding: utf-8 -*-
#
# Installs basic database.
#
# Created on 2015-01-24.
# ================================================================================ #
import getpass
import importlib
import os
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


# Core data.
# -------------------------------------------------------------------------------- #
roles = [# parent, name, description
Role(None,  "Root",             "Applies to everyone."),
Role(1,     "Guest",            "Applies to clients who aren't logged in."),
Role(1,     "User",             "Applies to all logged in users."),
Role(3,     "Locked",           "Applies to clients who haven't been activated."),
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
Rule(5, "/role/",           "All",  "All",  "All",  "All"),
Rule(5, "/rule/",           "All",  "All",  "All",  "All"),
Rule(5, "/menubar/",        "All",  "All",  "All",  "All"),
Rule(5, "/menuitem/",       "All",  "All",  "All",  "All"),
Rule(5, "/plugins",         "None", "None", "None", "All"),
Rule(5, "/routes",          "None", "None", "None", "All"),
Rule(3, "/personal/",       "None", "None", "None", "All")
]

menubars = [# name
Menubar("personal"),
Menubar("administration"),
Menubar("rule"),
Menubar("role"),
Menubar("menubar"),
Menubar("menuitem"),
Menubar("main"),
Menubar("extended")
]

menuitems = [# menubar, weight, name, image, flags, address
Menuitem(1, 10, "Sign in",          "log-in",           "eo-ap","/signin"),
Menuitem(1, 10, "Sign out",         "log-out",          "", "/signout"),
Menuitem(1, 1,  "Administration",   "cog",              "", "/administration"),
Menuitem(2, 0,  "Rules",            "ok-circle",        "", "/rule/"),
Menuitem(2, 1,  "Roles",            "briefcase",        "", "/role/"),
Menuitem(2, 2,  "Menus",            "menu-hamburger",   "", "/menubar/"),
Menuitem(2, 3,  "Links",            "play-circle",      "", "/menuitem/"),
Menuitem(2, 4,  "Routes",           "random",           "", "/routes"),
Menuitem(2, 5,  "Plugins",          "cog",              "", "/plugins"),
Menuitem(3, 0,  "",                 "plus",             "", "/rule/create"),
Menuitem(3, 1,  "",                 "remove",           "", "/rule/<id>/delete"),
Menuitem(3, 2,  "",                 "pencil",           "", "/rule/<id>/update"),
Menuitem(4, 0,  "",                 "plus",             "", "/role/create"),
Menuitem(4, 1,  "",                 "remove",           "", "/role/<id>/delete"),
Menuitem(4, 2,  "",                 "pencil",           "", "/role/<id>/update"),
Menuitem(5, 0,  "",                 "plus",             "", "/menubar/create"),
Menuitem(5, 1,  "",                 "remove",           "", "/menubar/<id>/delete"),
Menuitem(5, 2,  "",                 "pencil",           "", "/menubar/<id>/update"),
Menuitem(6, 0,  "",                 "plus",             "", "/menuitem/create"),
Menuitem(6, 1,  "",                 "remove",           "", "/menuitem/<id>/delete"),
Menuitem(6, 2,  "",                 "pencil",           "", "/menuitem/<id>/update"),
]


# Initialize application
# -------------------------------------------------------------------------------- #
print("Initializing installer ...")
if not os.path.exists(Configuration["native_msg"]):
    os.makedirs(Configuration["native_msg"])
if not os.path.exists(Configuration["cache_path"]):
    os.makedirs(Configuration["cache_path"])
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
[path, prefix] = [["./src/plugins"], "plugins."]
modules = []
for module_loader, name, ispkg in pkgutil.walk_packages(path, prefix):
    if ispkg: continue
    if not name.endswith("__install__"): continue
    module = importlib.import_module(name)
    if not hasattr(module, "install"): continue
    modules.append(module)

# Install application
# -------------------------------------------------------------------------------- #
print("Installing core data ...")
print("----------------------------------------------------------------")
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
    print("Creating first users ...")
    anonymous   = input("Anonymous account username:\n>>> ")
    username    = input("Administrator account username:\n>>> ")
    email       = input("Administrator account email:\n>>> ")
    password    = getpass.getpass("Administrator account password:\n>>> ")
    print("Installing users ...")
    user = User(2, "", anonymous, "", "")
    user.create()
    user = User(5, email, username, hash_password(password), "")
    user.create()
Session.total()
print("\n\nInstalling plugin data ...")
print("----------------------------------------------------------------")
for module in modules: module.install()
