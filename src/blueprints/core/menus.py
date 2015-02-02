# -*- coding: utf-8 -*-
#
# Menu
#
# Blueprint for menu administration.
#
# Created by dp on 2014-12-25.
# ================================================================================ #
from flask.blueprints import Blueprint
from flask.globals import g
from flask_wtf.form import Form
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import TextField, SubmitField
from wtforms.validators import DataRequired, NumberRange

from blueprints import render, create_form, delete_form, update_form
from natives.menu import menubar, contextmenu, Menu


blueprint = Blueprint("Menu Controller", __name__)


# Forms
# -------------------------------------------------------------------------------- #
class FormMenu(Form):
    address     = TextField("address", validators = [DataRequired()])
    name        = TextField("name")
    menubar     = TextField("menubar", validators = [DataRequired()])
    weight      = IntegerField("weight", validators = [DataRequired()])
    flags       = IntegerField("flags", validators = [NumberRange(0, 10)])
    image       = TextField("image")
    confirm     = SubmitField("Confirm")
    cancel      = SubmitField("Cancel")


# Default route: View a list of all menus
# -------------------------------------------------------------------------------- #
@blueprint.route("/menus", methods = ["GET"])
def entries():
    items = Menu.all()
    actions = menubar("menu", g.role.id)
    for item in items: item.actions = contextmenu("menu", g.role.id)
    return render("core/menu_list.html", items = items, actions = actions)

# Create Menu
# -------------------------------------------------------------------------------- #
@blueprint.route("/menus/create", methods = ["GET", "POST"])
def create():
    item = Menu()
    return create_form(FormMenu(), item, "Created new menu item.", "/menus")

# Delete Menu
# -------------------------------------------------------------------------------- #
@blueprint.route("/menus/<identifier>/delete", methods = ["GET", "POST"])
def delete(identifier):
    item = Menu.get(int(identifier))
    if not item: return "NO SUCH OBJECT"
    headline = "%s löschen?" % (item.address)
    text = "Menü %s wirklich löschen?" % (item.address)
    return delete_form(item, headline, text, "Deleted menu item.", "/menus")

# Edit Menu
# -------------------------------------------------------------------------------- #
@blueprint.route("/menus/<identifier>/update", methods = ["GET", "POST"])
def update(identifier):
    item = Menu.get(int(identifier))
    if not item: return "NO SUCH OBJECT"
    return update_form(FormMenu(obj = item), item, "Updated menu item.", "/menus")
