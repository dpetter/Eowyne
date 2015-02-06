# -*- coding: utf-8 -*-
#
# Install basic database.
#
# ...
#
# Created by dp on 2014-02-02.
# ================================================================================ #
from flask.app import Flask
from flask_bootstrap import Bootstrap

from app.configuration import Configuration
from app.globals import cache, db
from models.blog import Blog
from models.session import Session
from models.user import User
from models.gattung import Gattung
from models.land import Land
from models.rebsorte import Rebsorte
from models.region import Region
from models.weingut import Weingut
from models.wein import Wein
from natives.menu import Menu
from natives.role import Role
from natives.rule import Rule
from utility.log import Log


class Installer():
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def installRoles():
        if Role.get(1): return
        Log.debug(Installer.__name__, "Installing roles...")
        items = [
                 #    parent name
                 #    description
                 Role(None, "Root",
                      "Applies to everyone."),
                 Role(1, "Guest",
                      "Applies to clients who aren't logged in."),
                 Role(1, "User",
                      "Applies to all logged in users."),
                 Role(3, "Locked",
                      "Applies to clients who haven't activated their account yet."),
                 Role(3, "Administrator",
                      "Has the most extensive permissions."),
                 ]
        for item in items: item.create()
    
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def installRules():
        if Rule.get(1): return
        Log.debug(Installer.__name__, "Installing rules...")
        items = [
                 #    role_id pattern
                 #    insert, delete, update, view, search
                 Rule(1, "/",
                      "None",   "None", "None", "All",  "None"),
                 Rule(1, "/pages/",
                      "None",   "None", "None", "All",  "None"),
                 Rule(2, "/register/",
                      "None",   "None", "None", "All",  "None"),
                 Rule(2, "/reset/",
                      "None",   "None", "None", "All",  "None"),
                 Rule(2, "/signin",
                      "None",   "None", "None", "All",  "None"),
                 Rule(3, "/signout",
                      "None",   "None", "None", "All",  "None"),
                 Rule(5, "/",
                      "All",    "All",  "All",  "All",  "All"),
                 Rule(5, "/pages/",
                      "All",    "All",  "All",  "All",  "All"),
                 Rule(5, "/administration",
                      "All",    "All",  "All",  "All",  "All"),
                 Rule(5, "/roles/",
                      "All",    "All",  "All",  "All",  "All"),
                 Rule(5, "/rules/",
                      "All",    "All",  "All",  "All",  "All"),
                 Rule(5, "/menus/",
                      "All",    "All",  "All",  "All",  "All"),
                 Rule(3, "/personal/",
                      "None",   "None", "None", "All",  "None"),
                 Rule(3, "/blog/",
                      "Own",    "Own",  "Own",  "All",  "None")
                 ]
        for item in items: item.create()
    
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def installMenus():
        if Menu.get(1): return
        Log.debug(Installer.__name__, "Installing menus...")
        items = [
                 # address, name, menubar, weight, flags, image
                 Menu("/signin",            "Sign in",
                      "personal",   2, 1, None),
                 Menu("/signout",           "Sign out",
                      "personal",   2, 1, None),
                 Menu("/personal",          "Mein Account",
                      "personal",   0, 1, None),
                 Menu("/pages/about",       "Über uns",
                      "main",       0, 0, None),
                 Menu("/blog",              "Blog",
                      "main",       1, 0, None),
                 Menu("/administration",    "Administration",
                      "main",       2, 0, None),
                 Menu("/pages/contact",     "Kontakt",
                      "extended",   0, 0, None),
                 Menu("/pages/legal",       "Impressum",
                      "extended",   0, 0, None),
                 Menu("/rules",             "Rules",
                      "administration",0, 0, None),
                 Menu("/roles",             "Roles",
                      "administration",0, 0, None),
                 Menu("/menus",             "Menus",
                      "administration",0, 0, None),
                 Menu("/rules/create",      "Neue Regel",
                      "rule",       0, 0, "img/administration/create-24.png"),
                 Menu("/rules/<id>/delete", "",
                      "rule",       1, 0, "img/administration/delete-24.png"),
                 Menu("/rules/<id>/update", "",
                      "rule",       2, 0, "img/administration/update-24.png"),
                 Menu("/roles/create",      "Neue Rolle",
                      "role",       0, 0, "img/administration/create-24.png"),
                 Menu("/roles/<id>/delete", "",
                      "role",       1, 0, "img/administration/delete-24.png"),
                 Menu("/roles/<id>/update", "",
                      "role",       2, 0, "img/administration/update-24.png"),
                 Menu("/menus/create",      "Neuer Menüeintrag",
                      "menu",       0, 0, "img/administration/create-24.png"),
                 Menu("/menus/<id>/delete", "",
                      "menu",       1, 0, "img/administration/delete-24.png"),
                 Menu("/menus/<id>/update", "",
                      "menu",       2, 0, "img/administration/update-24.png"),
                 Menu("/blog/create",     "Neuer Blogeintrag",
                      "blog",       0, 0, "img/administration/create-24.png"),
                 Menu("/blog/<id>/delete", "",
                      "blog",       1, 0, "img/administration/delete-24.png"),
                 Menu("/blog/<id>/update", "",
                      "blog",       2, 0, "img/administration/update-24.png")
                 ]
        for item in items: item.create()
    
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def installUsers():
        if User.get(1): return
        Log.debug(Installer.__name__, "Installing users...")
        items = [
                 #    role          email                   name
                 #    password      key
                 User(Role.get(2),  None,               "Gast",
                      None,         ""),
                 User(Role.get(5),  "eowyn@eowyne.de",  "Administrator",
                      "pwd",        ""),
                 User(Role.get(3),  "user@eowyne.de",   "Benutzer",
                      "pwd",        ""),
                 User(Role.get(3),  "test@eowyne.de",   "Test Benutzer",
                      "pwd",        ""),
                 ]
        for item in items: item.create()
    
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def installSessions():
        Session.get(1)
    
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def installGattung():
        if Gattung.get(1): return
        Log.debug(Installer.__name__, "Installing Gattungen...")
        items = [
                Gattung("Rotwein"),
                Gattung("Weisswein"),
                Gattung("Roséwein"),
                Gattung("Champagner"),
                Gattung("Sekt"),
                ]
        for item in items: item.create()

    # ---------------------------------------------------------------------------- #
    @staticmethod
    def installLand():
        if Land.get(1): return
        Log.debug(Installer.__name__, "Installing Laender...")
        item = Land("Frankreich")
        item.create()

    # ---------------------------------------------------------------------------- #
    @staticmethod
    def installRebsorte():
        if Rebsorte.get(1): return
        Log.debug(Installer.__name__, "Installing Rebsorten...")
        item = Rebsorte("Merlot")
        item.create()

    # ---------------------------------------------------------------------------- #
    @staticmethod
    def installRegion():
        if Region.get(1): return
        Log.debug(Installer.__name__, "Installing Regionen...")
        item = Region("Languedoc Roussillon")
        item.create()

    # ---------------------------------------------------------------------------- #
    @staticmethod
    def installWeingut():
        if Weingut.get(1): return
        Log.debug(Installer.__name__, "Installing Weingueter...")
        item = Weingut("Domaine de La Grange")
        item.create()

    # ---------------------------------------------------------------------------- #
    @staticmethod
    def installWein():
        if Wein.get(1): return
        Log.debug(Installer.__name__, "Installing Wein...")
        item = Wein("La Grange Terroir Merlot Pabrio",
                    Gattung.get(1),
                    Rebsorte.get(1),
                    Land.get(1),
                    Region.get(1),
                    Weingut.get(1),
                    2013,
        )
        item.create()

# Install
# -------------------------------------------------------------------------------- #
def createDatabase():
    db.create_all()
    createTableData()

def createTableData():
    Installer.installRoles()
    Installer.installRules()
    Installer.installMenus()
    Installer.installUsers()
    Installer.installSessions()
    Installer.installGattung()
    Installer.installLand()
    Installer.installRebsorte()
    Installer.installRegion()
    Installer.installWeingut()
    Installer.installWein()

def recreateDatabase():
    db.drop_all()
    createDatabase()

# Initialise application
# -------------------------------------------------------------------------------- #

Log.level(Log.DEBUG)
Log.information(__name__, "Initialising Flask...")
app = Flask(__name__,
            static_folder = "../../static",
            template_folder = "../../template")
Bootstrap(app)
app.secret_key = Configuration["secret_key"]
cache.init_app(app, config={"CACHE_TYPE": Configuration["cache_type"],
                            "CACHE_DIR": Configuration["cache_path"]})
Log.information(__name__, "Connecting to database...")
app.config["SQLALCHEMY_DATABASE_URI"] = Configuration["sql_db_uri"]
db.app = app
db.init_app(app)

createDatabase()
