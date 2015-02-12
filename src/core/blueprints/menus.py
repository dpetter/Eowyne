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
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired, NumberRange

from core.natives.menu import Menu, menubar, contextmenu
from core.rendering import DefaultForm, render, create_form, mismatch, delete_form, \
    update_form
from utility.localization import localize


blueprint = Blueprint("Menu Controller", __name__)


# Forms
# -------------------------------------------------------------------------------- #
class FormMenu(DefaultForm):
    menubar     = TextField(localize("core", "menus.field_menubar"),
                            validators = [DataRequired()])
    address     = TextField(localize("core", "menus.field_address"),
                            validators = [DataRequired()])
    name        = TextField(localize("core", "menus.field_name"))
    weight      = IntegerField(localize("core", "menus.field_weight"),
                               validators = [NumberRange(0, 25)])
    flags       = IntegerField(localize("core", "menus.field_flags"),
                               validators = [NumberRange(0, 16)])
    image       = TextField(localize("core", "menus.field_image"))


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
    headline = localize("core", "menus.create_headline")
    message = localize("core", "menus.create_success")
    return create_form(item, FormMenu(), headline, message, "/menus")

# Delete Menu
# -------------------------------------------------------------------------------- #
@blueprint.route("/menus/<identifier>/delete", methods = ["GET", "POST"])
def delete(identifier):
    item = Menu.get(int(identifier))
    if not item: return mismatch()
    headline = localize("core", "menus.delete_headline")
    text = localize("core", "menus.delete_description") % (item.name)
    message = localize("core", "menus.delete_success")
    return delete_form(item, headline, text, message, "/menus")

# Edit Menu
# -------------------------------------------------------------------------------- #
@blueprint.route("/menus/<identifier>/update", methods = ["GET", "POST"])
def update(identifier):
    item = Menu.get(int(identifier))
    if not item: return mismatch()
    headline = localize("core", "menus.update_headline")
    message = localize("core", "menus.update_success")
    return update_form(item, FormMenu(obj = item), headline, message, "/menus")
