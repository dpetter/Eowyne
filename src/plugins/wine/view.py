from flask.blueprints import Blueprint
from flask.globals import g

from core.rendering import render
from plugins.wine.models import *


blueprint = Blueprint("Wein Controller", __name__)

@blueprint.route("/wein/", methods = ["GET"])
@blueprint.route("/wein/tops", methods = ["GET"])
def wein_tops():
    items = Wein.all()
    if not items: return render("plugins/wein/empty.html", actions = actions)
    return render("plugins/wein/list.html", items = items)

@blueprint.route("/wein/flops", methods = ["GET"])
def wein_flops():
    pass

@blueprint.route("/wein/suche/<name>", methods = ["GET"])
def wein_suche(name):
    weine = Wein.query.filter(Wein.name.contains(name)).all()
    if not weine:
        return render("plugins/wein/empty.html")
    liste = ''
    print('hallo')
    for wein in weine:
        print(str(wein))
        liste += str(wein) + '<br/>'
        return liste

@blueprint.route("/wein/<name>", methods = ["GET"])
def wein(name):
    item = Wein.query.filter(Wein.name==name.replace('_', ' ')).first()
    if not item: return render("plugins/wein/empty.html")
    return render("plugins/wein/view.html", item = item)

