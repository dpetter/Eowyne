# -*- coding: utf-8 -*-
#
# Application
#
# Serves the application. Automatically registers all blueprints.
#
# Created on 2015-02-07.
# ================================================================================ #
import importlib
import pkgutil

from flask.app import Flask
from flask_bootstrap import Bootstrap
from werkzeug.contrib.fixers import ProxyFix

from app.configuration import Configuration
from core.shared import db, cache, mailservice
from utility import localization
from utility.log import Log
from core import shared
from natives import Native


# Initialise application
# -------------------------------------------------------------------------------- #
Log.level(Configuration["log_level"])
Log.information(__name__, "Initialising Flask...")
app = Flask(__name__,
            static_folder = Configuration["static_dir"],
            template_folder = Configuration["template_dir"])
app.debug=True
app.wsgi_app = ProxyFix(app.wsgi_app)
Bootstrap(app)
app.secret_key = Configuration["secret_key"]
localization.text_path = Configuration["text_files"]
shared.noscope_url = Configuration["noscopeurl"]

Log.information(__name__, "Connecting to database...")
app.config["SQLALCHEMY_DATABASE_URI"] = Configuration["sql_db_uri"]
db.app = app
db.init_app(app)
shared.heartbeat_time = 60.0 / Configuration["heartbeats"]
Native.__message__ = Configuration["native_msg"]

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
path = ["./src/core/blueprints"]
prefix = "core.blueprints."
for module_loader, name, ispkg in pkgutil.walk_packages(path, prefix):
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

# Run application
# -------------------------------------------------------------------------------- #
if (__name__ == "__main__"):
    app.run(host = Configuration["flask_host"], port = Configuration["flask_port"])
