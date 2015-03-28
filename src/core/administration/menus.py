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
from wtforms.fields.core import SelectField, IntegerField
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired, NumberRange

from core.navigation.menu import menubar, Menuitem, contextmenu, Menubar
from core.rendering import DefaultForm, render, create_form, mismatch, delete_form, \
    update_form
from core.utility.localization import localize


blueprint = Blueprint("eowyne-core-menus", __name__)


# Forms.
# -------------------------------------------------------------------------------- #
class FormMenu(DefaultForm):
    menubar_id  = SelectField(localize("core", "menus.field_menubar"),
                              coerce = int)
    address     = TextField(localize("core", "menus.field_address"),
                            validators = [DataRequired()])
    name        = TextField(localize("core", "menus.field_name"))
    weight      = IntegerField(localize("core", "menus.field_weight"),
                               validators = [NumberRange(0, 25)])
    flags       = TextField(localize("core", "menus.field_flags"),
                            validators = [NumberRange(0, 16)])
    image       = TextField(localize("core", "menus.field_image"))

class FormMenubar(DefaultForm):
    name        = TextField(localize("core", "menus.field_menubar"),
                            validators = [DataRequired()])


# Default route: View a list of all menu items.
# -------------------------------------------------------------------------------- #
@blueprint.route("/menuitem/", methods = ["GET"])
def entries():
    navigation = menubar("administration", g.role.id)
    items = Menuitem.all()
    actions = menubar("menuitem", g.role.id)
    for item in items: item.actions = contextmenu("menuitem", g.role.id)
    return render("core/administration/menuitem-list.html", navigation = navigation,
                  items = items, actions = actions)

# Handler: Create menu item.
# -------------------------------------------------------------------------------- #
@blueprint.route("/menuitem/create", methods = ["GET", "POST"])
def create_menuitem():
    item = Menuitem()
    form = FormMenu()
    form.menubar_id.choices = [(bar.id, bar.name) for bar in Menubar.all()]
    headline = localize("core", "menus.create_headline")
    message = localize("core", "menus.create_success")
    return create_form(item, form, headline, message, "/menus")

# Handler: Delete menu item.
# -------------------------------------------------------------------------------- #
@blueprint.route("/menuitem/<identifier>/delete", methods = ["GET", "POST"])
def delete_menuitem(identifier):
    item = Menuitem.get(int(identifier))
    if not item: return mismatch()
    headline = localize("core", "menus.delete_headline")
    text = localize("core", "menus.delete_description") % (item.name)
    message = localize("core", "menus.delete_success")
    return delete_form(item, headline, text, message, "/menus",
                       template = "core/administration/confirm.html")

# Handler: Edit menu item.
# -------------------------------------------------------------------------------- #
@blueprint.route("/menuitem/<identifier>/update", methods = ["GET", "POST"])
def update_menuitem(identifier):
    item = Menuitem.get(int(identifier))
    form = FormMenu(obj = item)
    form.menubar_id.choices = [(bar.id, bar.name) for bar in Menubar.all()]
    if not item: return mismatch()
    headline = localize("core", "menus.update_headline")
    message = localize("core", "menus.update_success")
    return update_form(item, form, headline, message, "/menus")

# Default route: View a list of all menu bars.
# -------------------------------------------------------------------------------- #
@blueprint.route("/menubar/", methods = ["GET"])
def list_menubars():
    navigation = menubar("administration", g.role.id)
    items = Menubar.all()
    actions = menubar("menu", g.role.id)
    for item in items: item.actions = contextmenu("menubar", g.role.id)
    return render("core/administration/menubar-list.html", navigation = navigation,
                  items = items, actions = actions)

# Handler: Create menu bar.
# -------------------------------------------------------------------------------- #
@blueprint.route("/menubar/create", methods = ["GET", "POST"])
def create_menubar():
    item = Menubar()
    form = FormMenubar()
    headline = localize("core", "menubars.create_headline")
    message = localize("core", "menubars.create_success")
    return create_form(item, form, headline, message, "/menus")

# Handler: Delete menu bar.
# -------------------------------------------------------------------------------- #
@blueprint.route("/menubar/<identifier>/delete", methods = ["GET", "POST"])
def delete_menubar(identifier):
    item = Menubar.get(int(identifier))
    if not item: return mismatch()
    headline = localize("core", "menubars.delete_headline")
    text = localize("core", "menubars.delete_description") % (item.name)
    message = localize("core", "menus.delete_success")
    return delete_form(item, headline, text, message, "/menus",
                       template = "core/administration/confirm.html")

# Handler: Edit menu bar.
# -------------------------------------------------------------------------------- #
@blueprint.route("/menubar/<identifier>/update", methods = ["GET", "POST"])
def update_menubar(identifier):
    item = Menubar.get(int(identifier))
    if not item: return mismatch()
    form = FormMenubar(obj = item)
    headline = localize("core", "menubars.update_headline")
    message = localize("core", "menubars.update_success")
    return update_form(item, form, headline, message, "/menus")
