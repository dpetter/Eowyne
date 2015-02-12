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
from core.natives.menu import Menu
from core.natives.role import Role
from core.natives.rule import Rule
from core.shared import db
from plugins.blog.blog import Blog
from plugins.wine.models.gattung import Gattung
from plugins.wine.models.land import Land
from plugins.wine.models.rebsorte import Rebsorte
from plugins.wine.models.region import Region
from plugins.wine.models.wein import Wein
from plugins.wine.models.weingut import Weingut
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
             Rule(3, "/blog/",              "Own",  "Own",  "Own",  "All")
             ]
    for item in items: item.create()

# -------------------------------------------------------------------------------- #
def installMenus():
    if Menu.get(1): return
    Log.information(__name__, "Installing menus...")
    items = [#    address, name, menubar, weight, flags, image
             Menu("/signin",            "Sign in",          "personal",
                  2, 1, ""),
             Menu("/signout",           "Sign out",         "personal",
                  2, 1, ""),
             Menu("/personal",          "My Account",       "personal",
                  0, 1, ""),
             Menu("/pages/about",       "About us",         "main",
                  0, 0, ""),
             Menu("/blog",              "Blog",             "main",
                  1, 0, ""),
             Menu("/administration",    "Administration",   "main",
                  2, 0, ""),
             Menu("/pages/contact",     "Contact",          "extended",
                  0, 0, ""),
             Menu("/pages/legal",       "Legal",            "extended",
                  0, 0, ""),
             Menu("/rules",             "Rules",            "administration",
                  0, 0, ""),
             Menu("/roles",             "Roles",            "administration",
                  0, 0, ""),
             Menu("/menus",             "Menus",            "administration",
                  0, 0, ""),
             Menu("/rules/create",      "Add rule",         "rule",
                  0, 0, "img/administration/create-24.png"),
             Menu("/rules/<id>/delete", "",                 "rule",
                  1, 0, "img/administration/delete-24.png"),
             Menu("/rules/<id>/update", "",                 "rule",
                  2, 0, "img/administration/update-24.png"),
             Menu("/roles/create",      "Add role",         "role",
                  0, 0, "img/administration/create-24.png"),
             Menu("/roles/<id>/delete", "",                 "role",
                  1, 0, "img/administration/delete-24.png"),
             Menu("/roles/<id>/update", "",                 "role",
                  2, 0, "img/administration/update-24.png"),
             Menu("/menus/create",      "Add menu item",    "menu",
                  0, 0, "img/administration/create-24.png"),
             Menu("/menus/<id>/delete", "",                 "menu",
                  1, 0, "img/administration/delete-24.png"),
             Menu("/menus/<id>/update", "",                 "menu",
                  2, 0, "img/administration/update-24.png"),
             Menu("/blog/create",       "Write blog entry", "blog",
                  0, 0, "img/administration/create-24.png"),
             Menu("/blog/<id>/delete",  "",                 "blog",
                  1, 0, "img/administration/delete-24.png"),
             Menu("/blog/<id>/update",  "",                 "blog",
                  2, 0, "img/administration/update-24.png")
             ]
    for item in items: item.create()

# -------------------------------------------------------------------------------- #
def installUsers():
    if User.get(1): return
    Log.information(__name__, "Installing users...")
    items = [#    role, email, name, password, key
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
Bootstrap(app)
app.secret_key = Configuration["secret_key"]

Log.information(__name__, "Connecting to database...")
app.config["SQLALCHEMY_DATABASE_URI"] = Configuration["sql_db_uri"]
db.app = app
db.init_app(app)
createDatabase()
