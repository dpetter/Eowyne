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


# Initialise application
# -------------------------------------------------------------------------------- #
Log.level(Log.DEBUG)
Log.information(__name__, "Initialising Flask...")
app = Flask(__name__,
            static_folder = "../../static",
            template_folder = "../../template")
app.wsgi_app = ProxyFix(app.wsgi_app)
Bootstrap(app)
app.secret_key = Configuration["secret_key"]

Log.information(__name__, "Connecting to database...")
app.config["SQLALCHEMY_DATABASE_URI"] = Configuration["sql_db_uri"]
db.app = app
db.init_app(app)

Log.information(__name__, "Setting up cache...")
cache.init_app(app, config={"CACHE_TYPE": Configuration["cache_type"],
                            "CACHE_DIR": Configuration["cache_path"]})
Log.information(__name__, "Setting up mailservice...")
mailservice.init_app(Configuration["email_host"], Configuration["email_host"],
                     Configuration["email_user"], Configuration["email_pass"])
localization.text_path = Configuration["text_files"]
    
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
path = ["./src/plugins/blueprints"]
prefix = "plugins.blueprints."
for module_loader, name, ispkg in pkgutil.walk_packages(path, prefix):
    module = importlib.import_module(name)
    if not hasattr(module, "blueprint"): continue
    Log.information(__name__, "Importing %s" % (name))
    app.register_blueprint(module.blueprint)

# Run application
# -------------------------------------------------------------------------------- #
if (__name__ == "__main__"):
    app.run(host = Configuration["flask_host"], port = Configuration["flask_port"])
