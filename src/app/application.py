# -*- coding: utf-8 -*-
#
# Application
#
# Serves the application. Automatically registers all blueprints.
#
# Created on 2015-02-07.
# ================================================================================ #
import importlib
import inspect
import pkgutil
import sys

from flask.app import Flask
from flask_bootstrap import Bootstrap
from werkzeug.contrib.fixers import ProxyFix

from app.configuration import Configuration
from core import shared
from core.shared import db, cache, mailservice
from core.utility import localization
from natives import Native
from utility.log import Log


# Initialize application
# -------------------------------------------------------------------------------- #
Log.level(Configuration["log_level"])
Log.information(__name__, "Initialising Flask...")
app = Flask(__name__,
            static_folder = Configuration["static_dir"],
            template_folder = Configuration["template_dir"])
app.debug = True
app.wsgi_app = ProxyFix(app.wsgi_app)
Bootstrap(app)
app.secret_key = Configuration["secret_key"]
localization.text_path = Configuration["text_files"]
shared.noscope_url = Configuration["noscopeurl"]

Log.information(__name__, "Connecting to database...")
app.config["SQLALCHEMY_DATABASE_URI"] = Configuration["sql_db_uri"]
db.app = app
db.init_app(app)

# TODO: Cache must be more configurable.
Log.information(__name__, "Setting up cache...")
cache.init_app(app, config={"CACHE_TYPE": Configuration["cache_type"],
                            "CACHE_DIR": Configuration["cache_path"]})

Log.information(__name__, "Setting up mailservice...")
if "email_host" in Configuration:
    mailservice.init_app(Configuration["email_host"], Configuration["email_host"],
                         Configuration["email_user"], Configuration["email_pass"])

# Register blueprints
# -------------------------------------------------------------------------------- #
Log.information(__name__, "Registering core blueprints...")
core_blueprints = ["core", "security.login", "administration.roles",
                   "administration.rules", "administration.menus"]
#path = ["./src/core/blueprints"]
#prefix = "core.blueprints."
#for module_loader, name, ispkg in pkgutil.walk_packages(path, prefix):
for item in core_blueprints:
    name = "core." + item
    module = importlib.import_module(name)
    if not hasattr(module, "blueprint"): continue
    Log.information(__name__, "Importing %s" % (name))
    app.register_blueprint(module.blueprint)

Log.information(__name__, "Registering plugin blueprints...")
path = ["./src/plugins"]
prefix = "plugins."
for module_loader, name, ispkg in pkgutil.walk_packages(path, prefix):
    module = importlib.import_module(name)
    if not hasattr(module, "blueprint"): continue
    Log.information(__name__, "Importing %s" % (name))
    app.register_blueprint(module.blueprint)

# Initialize native heart beats
# -------------------------------------------------------------------------------- #
Log.information(__name__, "Making hearts beat...")
heartbeat_functions = []
p = lambda x, y: inspect.isclass(y) and y.__module__ == x and issubclass(y, Native)
[path, prefix] = [["./src/core"], "core."]
for module_loader, name, ispkg in pkgutil.walk_packages(path, prefix):
    items = inspect.getmembers(sys.modules[name], lambda y: p(name, y))
    for item in items:
        item[1].load()
        heartbeat_functions.append(item[1].heartbeat)
[path, prefix] = [["./src/plugins"], "plugins."]
for module_loader, name, ispkg in pkgutil.walk_packages(path, prefix):
    items = inspect.getmembers(sys.modules[name], lambda y: p(name, y))
    for item in items:
        item[1].load()
        heartbeat_functions.append(item[1].heartbeat)
shared.beating_hearts = heartbeat_functions
shared.heartbeat_time = 60.0 / Configuration["heartbeats"]
Native.__message__ = Configuration["native_msg"]

# Run application
# -------------------------------------------------------------------------------- #
if (__name__ == "__main__"):
    app.run(host = Configuration["flask_host"], port = Configuration["flask_port"])
