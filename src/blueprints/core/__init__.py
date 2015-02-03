# -*- coding: utf-8 -*-
#
# Core
#
# Contains views for the core functionality of the project.
# - Preparing the global scope before every request.
# - Static pages.
# - Client functionality (sign in etc.)
# - Administration pages for roles, rules and menus.
#
# Created by dp on 2015-02-02.
# ================================================================================ #
from flask.blueprints import Blueprint
from flask.globals import request, g, session

from blueprints import render, invalid, forbidden
from models.session import Session
from models.user import Client
from natives.menu import menubar
from natives.rule import access
from utility.log import Log


BlueprintCore = Blueprint("Core Controller", __name__)


# -------------------------------------------------------------------------------- #
@BlueprintCore.before_app_request
def beforerequest():
    Log.debug(__name__, "Incoming request")
    Log.debug(__name__, request.path)
    # The next line is to prevent the acquisition of globals when a static file
    # (style sheet, image, etc.) is requested. Since all files have an extension
    # but urls don't it simply checks whether the path contains a full stop.
    if "." in request.path: return
    # Fill the global scope ...
    g.session       = Session.acquire(session)
    g.user          = Client.get(g.session.user_id)
    g.role          = g.user.role
    g.main_menu     = menubar("main", g.role.id)
    g.personal_menu = menubar("personal", g.role.id)
    g.extended_menu = menubar("extended", g.role.id)
    permitted       = access(request.path, g.role.id, True)
    if permitted == -1: return invalid()
    elif permitted == 0: return forbidden()


# -------------------------------------------------------------------------------- #
@BlueprintCore.route("/administration", methods = ["GET"])
def administration():
    links = menubar("administration", g.role.id)
    return render("core/administration.html", links = links)
