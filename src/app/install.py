# -*- coding: utf-8 -*-
#
# Installs basic database.
#
# Created on 2015-01-24.
# ================================================================================ #
from flask.app import Flask
from flask_bootstrap import Bootstrap

from app.configuration import Configuration
from core.models.session import Session
from core.models.user import User
from core.natives.menu import Menubar, Menuitem
from core.natives.role import Role
from core.natives.rule import Rule
from core.shared import db
from plugins.blog.blog import Blog
from plugins.wine.models import *
from utility import keyutility
from utility.log import Log


# -------------------------------------------------------------------------------- #
def installRoles():
    if Role.get(1): return
    Log.information(__name__, "Installing roles...")
    items = [#    parent, name, description
             Role(None, "Root", "Applies to everyone."),
             Role(1, "Guest", "Applies to clients who aren't logged in."),
             Role(1, "User", "Applies to all logged in users."),
             Role(3, "Locked",
                  "Applies to clients who haven't activated their account yet."),
             Role(3, "Administrator", "Has the most extensive permissions.")
             ]
    for item in items: item.create()

# -------------------------------------------------------------------------------- #
def installRules():
    if Rule.get(1): return
    Log.information(__name__, "Installing rules...")
    items = [#    role_id, pattern, insert, delete, update, view, search
             Rule(1, "/",                   "None", "None", "None", "All"),
             Rule(1, "/pages/",             "None", "None", "None", "All"),
             Rule(2, "/register/",          "None", "None", "None", "All"),
             Rule(2, "/reset/",             "None", "None", "None", "All"),
             Rule(2, "/signin",             "None", "None", "None", "All"),
             Rule(3, "/signout",            "None", "None", "None", "All"),
             Rule(5, "/",                   "All",  "All",  "All",  "All"),
             Rule(5, "/pages/",             "All",  "All",  "All",  "All"),
             Rule(5, "/administration",     "All",  "All",  "All",  "All"),
             Rule(5, "/roles/",             "All",  "All",  "All",  "All"),
             Rule(5, "/rules/",             "All",  "All",  "All",  "All"),
             Rule(5, "/menus/",             "All",  "All",  "All",  "All"),
             Rule(3, "/personal/",          "None", "None", "None", "All"),
             Rule(3, "/blog/",              "Own",  "Own",  "Own",  "All"),
             Rule(3, "/blog/[^/]+/comment", "None", "None", "None", "Foreign"),
             Rule(1, "/wein/",              "None", "None", "None", "All"),
             Rule(1, "/wein/suche/[^/]+",   "None", "None", "None", "All")
             ]
    for item in items: item.create()

# -------------------------------------------------------------------------------- #
def installMenus():
    if Menubar.get(1): return
    Log.information(__name__, "Installing menus...")
    items = [# name
             Menubar("personal"),
             Menubar("administration"),
             Menubar("rule"),
             Menubar("role"),
             Menubar("menu"),
             Menubar("main"),
             Menubar("extended"),
             Menubar("blog")
             ]
    for item in items: item.create()
    items = [# menubar, weight, name, image, flags, address 
             Menuitem(1,    0,  "My Account",       "user",             0,
                      "/personal"),
             Menuitem(1,    10, "Sign in",          "log-in",           0,
                      "/signin"),
             Menuitem(1,    10, "Sign out",         "log-out",          0,
                      "/signout"),
             Menuitem(2,    0,  "Rules",            "lock",             0,
                      "/rules"),
             Menuitem(2,    1,  "Roles",            "bishop",           0,
                      "/roles"),
             Menuitem(2,    2,  "Menus",            "menu-hamburger",   0,
                      "/menus"),
             Menuitem(3,    0,  "",                 "plus",             0,
                      "/rules/create"),
             Menuitem(3,    1,  "",                 "remove",           0,
                      "/rules/<id>/delete"),
             Menuitem(3,    2,  "",                 "pencil",           0,
                      "/rules/<id>/update"),
             Menuitem(4,    0,  "",                 "plus",             0,
                      "/roles/create"),
             Menuitem(4,    1,  "",                 "remove",           0,
                      "/roles/<id>/delete"),
             Menuitem(4,    2,  "",                 "pencil",           0,
                      "/roles/<id>/update"),
             Menuitem(5,    0,  "",                 "plus",             0,
                      "/menus/create"),
             Menuitem(5,    1,  "",                 "remove",           0,
                      "/menus/<id>/delete"),
             Menuitem(5,    2,  "",                 "pencil",           0,
                      "/menus/<id>/update"),
             Menuitem(6,    0,  "About us",         "",                 0,
                      "/pages/about"),
             Menuitem(6,    1,  "Blog",             "",                 0,
                      "/blog"),
             Menuitem(6,    2,  "Top Wines",        "",                 0,
                      "/wein/tops"),
             Menuitem(7,    0,  "Contact",          "",                 0,
                      "/pages/contact"),
             Menuitem(7,    1,  "Legal",            "",                 0,
                      "/pages/legal"),
             Menuitem(8,    0,  "",                 "plus",             0,
                      "/blog/create"),
             Menuitem(8,    1,  "",                 "remove",           0,
                      "/blog/<id>/delete"),
             Menuitem(8,    2,  "",                 "pencil",           0,
                      "/blog/<id>/update"),
             Menuitem(8,    2,  "Leave a comment",  "comment",          0,
                      "/blog/<id>/comment")
             ]
    for item in items: item.create()

# -------------------------------------------------------------------------------- #
def installUsers():
    if User.get(1): return
    Log.information(__name__, "Installing users...")
    items = [# role, email, name, password, key
             User(Role.get(2),  None,               "Gast",None,         ""),
             User(Role.get(5),  "eowyn@eowyne.de",  "Administrator","pwd",        ""),
             User(Role.get(3),  "user@eowyne.de",   "Benutzer","pwd",        ""),
             User(Role.get(3),  "test@eowyne.de",   "Test Benutzer", "pwd",        "")
             ]
    for item in items: item.create()

# -------------------------------------------------------------------------------- #
def installSessions():
    Session.get(1)

# -------------------------------------------------------------------------------- #
def installGattung():
    if Gattung.get(1): return
    Log.information(__name__, "Installing Gattungen...")
    items = [
             Gattung("Rotwein"),
             Gattung("Weisswein"),
             Gattung("Roséwein"),
             Gattung("Champagner"),
             Gattung("Sekt"),
            ]
    for item in items: item.create()

# -------------------------------------------------------------------------------- #
def installLand():
    if Land.get(1): return
    Log.information(__name__, "Installing Laender...")
    item = Land("Frankreich")
    item.create()

# -------------------------------------------------------------------------------- #
def installRebsorte():
    if Rebsorte.get(1): return
    Log.information(__name__, "Installing Rebsorten...")
    item = Rebsorte("Merlot")
    item.create()

# -------------------------------------------------------------------------------- #
def installRegion():
    if Region.get(1): return
    Log.information(__name__, "Installing Regionen...")
    item = Region("Languedoc Roussillon")
    item.create()

# -------------------------------------------------------------------------------- #
def installWeingut():
    if Weingut.get(1): return
    Log.debug(__name__, "Installing Weingueter...")
    item = Weingut("Domaine de La Grange")
    item.create()

# -------------------------------------------------------------------------------- #
def installWein():
    if Wein.get(1): return
    Log.information(__name__, "Installing Wein...")
    item = Wein("La Grange Terroir Merlot Pabrio",
                Gattung.get(1),
                Rebsorte.get(1),
                Land.get(1),
                Region.get(1),
                Weingut.get(1),
                2013)
    item.create()

# Install
# -------------------------------------------------------------------------------- #
def createDatabase():
    db.create_all()
    createTableData()

# -------------------------------------------------------------------------------- #
def createTableData():
    installRoles()
    installRules()
    installMenus()
    installUsers()
    installSessions()
    installGattung()
    installLand()
    installRebsorte()
    installRegion()
    installWeingut()
    installWein()

# -------------------------------------------------------------------------------- #
def recreateDatabase():
    db.drop_all()
    createDatabase()

# Initialise application
# -------------------------------------------------------------------------------- #
Log.level(Log.INFORMATION)
Log.information(__name__, "Initialising Flask...")
app = Flask(__name__,
            static_folder = "../../static",
            template_folder = "../../template")
app.secret_key = Configuration["secret_key"]
keyutility.salt = Configuration["crypt_salt"]

Log.information(__name__, "Connecting to database...")
app.config["SQLALCHEMY_DATABASE_URI"] = Configuration["sql_db_uri"]
db.app = app
db.init_app(app)
createDatabase()
