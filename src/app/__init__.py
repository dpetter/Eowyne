# -*- coding: utf-8 -*-
#
# Main Module
#
# ...
#
# Created by dp on 2015-01-24.
# ================================================================================ #
from builtins import __import__
import importlib
import pkgutil

from flask.app import Flask
from flask_bootstrap import Bootstrap
from flask_cache import Cache

from app.configuration import Configuration
from app.globals import cache, db, mailservice
import blueprints
from blueprints.core import BlueprintCore
from utility import localization
from utility.log import Log


if (__name__ == "__main__"):
    # Initialise application
    # ---------------------------------------------------------------------------- #
    Log.level(Log.DEBUG)
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
    Log.information(__name__, "Setting up cache...")
    cache.init_app(app, config={"CACHE_TYPE": Configuration["cache_type"],
                                "CACHE_DIR": Configuration["cache_path"]})
    Log.information(__name__, "Setting up mailservice...")
    mailservice.init_app(Configuration["email_host"], Configuration["email_host"],
                         Configuration["email_user"], Configuration["email_pass"])
    localization.text_path = Configuration["text_files"]
    
    # Register blueprints
    # ---------------------------------------------------------------------------- #
    Log.information(__name__, "Registering blueprints...")
    app.register_blueprint(BlueprintCore)
    package = blueprints
    path = blueprints.__path__
    prefix = blueprints.__name__ + "."
    for module_loader, name, ispkg in pkgutil.walk_packages(path, prefix):
        module = importlib.import_module(name)
        if not hasattr(module, "blueprint"): continue
        Log.information(__name__, "Importing blueprint %s" % (name))
        app.register_blueprint(module.blueprint)
    
    # Run application
    # ---------------------------------------------------------------------------- #
    app.run(host = "0.0.0.0", port = 5000)