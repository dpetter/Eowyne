# -*- coding: utf-8 -*-
#
# Page
#
# Blueprint for displaying static pages.
#
# Created by dp on 2014-12-25.
# ================================================================================ #
from flask.blueprints import Blueprint

from blueprints import render


blueprint = Blueprint("Page Controller", __name__)


# View
# -------------------------------------------------------------------------------- #
@blueprint.route("/", defaults = {"identifier": "index"}, methods = ["GET"])
@blueprint.route("/pages/<identifier>", methods = ["GET"])
def view(identifier):
    return render("pages/%s.html" % (identifier))
