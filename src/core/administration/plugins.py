# -*- coding: utf-8 -*-
#
# Role
#
# Blueprint for role administration.
#
# Created by dp on 2015-03-08.
# ================================================================================ #
import pkgutil
import re
import sys

from flask.blueprints import Blueprint
from flask.globals import g

from core.navigation.menu import menubar
from core.rendering import render
from core.security.rule import access


blueprint = Blueprint("core-plugin-controller", __name__)


# View a list of all plugins.
# -------------------------------------------------------------------------------- #
@blueprint.route("/plugins", methods = ["GET"])
def plugin_overview():
    navigation = menubar("administration", g.role.id)
    plugins = []
    controllers = {}
    installers = []
    [path, prefix] = [["./src/plugins"], "plugins."]
    for ml, name, ispkg in pkgutil.walk_packages(path, prefix):  # @UnusedVariable
        if name.count(".") == 1: plugins.append(name)
        if name.endswith("__install__"): installers.append(name)
        if name not in sys.modules: continue
        module = sys.modules[name]
        if hasattr(module, "blueprint"): controllers[name] = module.blueprint.name
    blueprints = lambda name: sorted([controllers[key] for key in controllers if \
                               key.startswith(name)])
    has_installer = lambda name: len([installer for installer in installers if \
                                      installer.startswith(name)]) > 0
    result = [(name, has_installer(name), blueprints(name)) for name in plugins]
    return render("core/administration/plugin-list.html", navigation = navigation,
                  items = result)

# View a list of all routes.
# -------------------------------------------------------------------------------- #
@blueprint.route("/routes", methods = ["GET"])
def route_overview():
    navigation = menubar("administration", g.role.id)
    rules = sys.modules["__main__"].app.url_map.iter_rules()
    controller = lambda endpoint: endpoint[0 : endpoint.find(".")]
    data = [(controller(str(rule.endpoint)), str(rule.rule)) for rule in rules]
    data.append((blueprint.name, "/plugins"))
    data.append((blueprint.name, "/routes"))
    endpoints = sorted(set(endpoint for endpoint, _ in data))
    def is_ruled(route):
        try: return access(re.sub("<[^<>]+>", "1", route), g.role.id) or True
        except Exception: return False
    routes = lambda endpoint: [(route, is_ruled(route)) for name, route in \
                               data if name == endpoint]
    combine = lambda endpoint: (endpoint, sorted(routes(endpoint)))
    result = [combine(endpoint) for endpoint in endpoints]
    return render("core/administration/route-list.html", navigation = navigation,
                  items = result)
