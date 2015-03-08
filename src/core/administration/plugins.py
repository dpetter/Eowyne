import importlib
import inspect
import pkgutil
import sys

from flask.blueprints import Blueprint
from flask.globals import g

from app.application import app
from core.navigation.menu import menubar
from core.rendering import render
from core.security.rule import Rule, access
import re


blueprint = Blueprint("plugin-controller", __name__)


# View a list of all plugins.
# -------------------------------------------------------------------------------- #
@blueprint.route("/plugins", methods = ["GET"])
def plugins():
    navigation = menubar("administration", g.role.id)
    modules = []
    controllers = {}
    p = lambda x, y: type(y) == Blueprint
    [path, prefix] = [["./src/plugins/"], "plugins."]
    for module_loader, name, ispkg in pkgutil.walk_packages(path, prefix):  # @UnusedVariable
        modules.append(name)
        items = inspect.getmembers(sys.modules[name], lambda y: p(name, y))
        if items and items[0][0] == "blueprint":
            module = importlib.import_module(name)
            controllers[name] = module.blueprint.name
    plugin_list = [x for x in modules if x.count(".") == 1]
    installer = lambda name: (name + ".__install__") in modules
    blueprints = lambda name: [controllers[key] for key in controllers if \
                               key.startswith(name)]
    result = [(name, installer(name), blueprints(name)) for name in plugin_list]
#    return str(result)
    return render("core/administration/plugin-list.html", navigation = navigation,
                  items = result)

@blueprint.route("/routes", methods = ["GET"])
def routes():
    navigation = menubar("administration", g.role.id)
    l = lambda x: x[0 : x.find(".")]
    data = [(l(str(x.endpoint)), str(x.rule)) for x in app.url_map.iter_rules()]
    names = set((x[0] for x in data))
#    is_ruled = lambda route: access(re.sub("<[^<>]+>", "1", route), 1, True) != -1
    result = [(name, [x[1] for x in data if x[0] == name], [is_ruled(x[1]) for x in data if x[0] == name]) for name in names]
    return render("core/administration/route-list.html", navigation = navigation,
                  items = result)

def is_ruled(route):
    try: return access(re.sub("<[^<>]+>", "1", route), g.role.id) or True
    except Exception: return False
