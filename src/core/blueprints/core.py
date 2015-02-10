# -*- coding: utf-8 -*-
#
# Core
#
# Contains views for the core functionality of the project.
# - Preparing the global scope before every request.
# - Administration pages for roles, rules and menus.
# - Static pages.
#
# Created by dp on 2015-02-02.
# ================================================================================ #
import time

from flask.blueprints import Blueprint
from flask.globals import request, g, session

from core import shared
from core.models.session import Session
from core.models.user import Client
from core.natives.menu import menubar, Menu
from core.natives.role import Role
from core.natives.rule import access, Rule
from core.rendering import invalid, forbidden, render
from utility.log import Log


blueprint = Blueprint("Core Controller", __name__)


# -------------------------------------------------------------------------------- #
@blueprint.before_app_request
def beforerequest():
    Log.debug(__name__, "Incoming request")
    Log.debug(__name__, request.path)
    # The next line is to prevent the acquisition of globals when a static file
    # (style sheet, image, etc.) is requested. Since all files have an extension
    # but urls don't it simply checks whether the path contains a full stop.
    if "." in request.path: return
    heartbeat()
    if request.path.startswith(shared.noscope_url): return
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
def heartbeat():
    try:
        now = time.time()
        if now - shared.time_elapsed < shared.heartbeat_time: return
        shared.time_elapsed = now
        Log.information(__name__, "Heartbeat")
        Role.heartbeat()
        Rule.heartbeat()
        Menu.heartbeat()
    except Exception as e:
        Log.error(__name__, "Heartbeat failed:" + str(e))

# -------------------------------------------------------------------------------- #
def is_authenticated():
    '''
    Returns True if this request comes from a logged in user.
    '''
    g.session       = Session.acquire(session)
    g.user          = Client.get(g.session.user_id)
    return g.user >= 3

# -------------------------------------------------------------------------------- #
@blueprint.route("/administration", methods = ["GET"])
def administration():
    links = menubar("administration", g.role.id)
    return render("core/administration.html", links = links)

# -------------------------------------------------------------------------------- #
@blueprint.route("/", defaults = {"identifier": "index"}, methods = ["GET"])
@blueprint.route("/pages/<identifier>", methods = ["GET"])
def page(identifier):
    return render("pages/%s.html" % (identifier))
