# -*- coding: utf-8 -*-
#
# Application
#
# Serves the application. Automatically registers all blueprints.
#
# Created on 2015-02-07.
# ================================================================================ #
from datetime import datetime

from flask.app import Flask
from flask_bootstrap import Bootstrap
from werkzeug.contrib.fixers import ProxyFix

from app.configuration import Configuration
from core import shared
from core.shared import db, cache, mailservice
from core.utility import localization
from core.utility.introspection import import_blueprints, localize_natives
from natives import Native
from utility.log import Log


# Initialize application
# -------------------------------------------------------------------------------- #
Log.level(Configuration["log_level"])
Log.information(__name__, "Initialising Flask ...")
app = Flask(__name__,
            static_folder = Configuration["static_dir"],
            template_folder = Configuration["template_dir"])
app.debug = True
app.wsgi_app = ProxyFix(app.wsgi_app)
Bootstrap(app)
app.secret_key = Configuration["secret_key"]
localization.text_path = Configuration["text_files"]
shared.noscope_url = Configuration["noscopeurl"]

Log.information(__name__, "Connecting to database ...")
app.config["SQLALCHEMY_DATABASE_URI"] = Configuration["sql_db_uri"]
db.app = app
db.init_app(app)

# TODO: Cache must be more configurable.
Log.information(__name__, "Setting up cache ...")
cache.init_app(app, config={"CACHE_TYPE": Configuration["cache_type"],
                            "CACHE_DIR": Configuration["cache_path"]})

Log.information(__name__, "Setting up mailservice ...")
if "email_host" in Configuration:
    mailservice.init_app(Configuration["email_host"], Configuration["email_host"],
                         Configuration["email_user"], Configuration["email_pass"])

# Register blueprints
# -------------------------------------------------------------------------------- #
Log.information(__name__, "Registering blueprints ...")
modules = import_blueprints("core") + import_blueprints("plugins")
for module in modules:
    if not hasattr(module, "blueprint"): continue
    Log.information(__name__, "Importing %s ..." % (module.__name__))
    app.register_blueprint(module.blueprint)

# Initialize native heart beats
# -------------------------------------------------------------------------------- #
Log.information(__name__, "Making hearts beat ...")
heartbeat_functions = []
natives = localize_natives("core") + localize_natives("plugins")
for native in natives:
    native.load()
    heartbeat_functions.append(native.heartbeat)
shared.beating_hearts = heartbeat_functions
shared.heartbeat_time = 60.0 / Configuration["heartbeats"]
Native.__message__ = Configuration["native_msg"]

# Run application
# -------------------------------------------------------------------------------- #
if (__name__ == "__main__"):
    shared.time_start = datetime.now()
    app.run(host = Configuration["flask_host"], port = Configuration["flask_port"])
