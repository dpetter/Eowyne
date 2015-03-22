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
from flask.globals import request, g
from werkzeug.wrappers import Response

from core import shared
from core.navigation.menu import menubar
from core.rendering import render
from core.security import acquire_session
from core.security.rule import access
from core.security.user import Client
from core.shared import log


blueprint = Blueprint("core-controller", __name__)


# Functions
# -------------------------------------------------------------------------------- #
def heartbeat():
    try:
        now = time.time()
        if now - shared.time_elapsed < shared.heartbeat_time: return
        shared.time_elapsed = now
        log.info("Heartbeat.")
        shared.heartbeat_count += 1
        for function in shared.beating_hearts: function()
    except Exception as e:
        log.error("Heartbeat failed: " + str(e))


def forbidden():
    '''
    Renders "Forbidden" Page
    '''
    return render("error/permissions.html")

def invalid():
    '''
    Renders "Invalid route" page.
    '''
    return render("error/route.html")


# Runs before every request
# -------------------------------------------------------------------------------- #
@blueprint.before_app_request
def beforerequest():
    log.debug("Incoming request")
    log.debug(request.path)
    # The next line is to prevent the acquisition of globals when a static file
    # (style sheet, image, etc.) is requested. Since all files have an extension
    # but urls don't it simply checks whether the path contains a full stop.
    if "." in request.path: return
    heartbeat()
    shared.request_count += 1
    if request.path.startswith(shared.noscope_url): return
    # Fill the global scope ...
    g.session       = acquire_session()
    if isinstance(g.session, Response): return g.session
    g.user          = Client.get(g.session.user_id)
    g.role          = g.user.role
    g.main_menu     = menubar("main", g.role.id)
    g.personal_menu = menubar("personal", g.role.id)
    g.extended_menu = menubar("extended", g.role.id)
    try:
        if access(request.path, g.role.id, True) == 0: return forbidden()
    except Exception as e:
        log.error(str(e))
        return invalid()

# Show administration page
# -------------------------------------------------------------------------------- #
@blueprint.route("/administration", methods = ["GET"])
def administration():
    links = menubar("administration", g.role.id)
    information = (shared.time_start, shared.heartbeat_count,
                   shared.request_count)
    return render("core/administration/dashboard.html", navigation = links,
                  information = information)

# Show static page
# -------------------------------------------------------------------------------- #
@blueprint.route("/", defaults = {"identifier": "index"}, methods = ["GET"])
@blueprint.route("/pages/<identifier>", methods = ["GET"])
def page(identifier):
    return render("pages/%s.html" % (identifier))
