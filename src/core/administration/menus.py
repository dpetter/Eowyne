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
from utility.localization import localize


blueprint = Blueprint("Menu Controller", __name__)


# Forms
# -------------------------------------------------------------------------------- #
class FormMenu(DefaultForm):
    menubar_id  = SelectField(localize("core", "menus.field_menubar"),
                              coerce = int)
#    menubar     = TextField(localize("core", "menus.field_menubar"),
#                            validators = [DataRequired()])
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
    navigation = menubar("administration", g.role.id)
    items = Menuitem.all()
    actions = menubar("menu", g.role.id)
    for item in items: item.actions = contextmenu("menu", g.role.id)
    return render("core/administration/menus.html", navigation = navigation,
                  items = items, actions = actions)

# Create Menu
# -------------------------------------------------------------------------------- #
@blueprint.route("/menus/create", methods = ["GET", "POST"])
def create():
    navigation = menubar("administration", g.role.id)
    item = Menuitem()
    form = FormMenu()
    form.menubar_id.choices = [(bar.id, bar.name) for bar in Menubar.all()]
    headline = localize("core", "menus.create_headline")
    message = localize("core", "menus.create_success")
    return create_form(item, form, headline, message, "/menus",
                       template = "core/administration/form.html",
                       navigation = navigation)

# Delete Menu
# -------------------------------------------------------------------------------- #
@blueprint.route("/menus/<identifier>/delete", methods = ["GET", "POST"])
def delete(identifier):
    navigation = menubar("administration", g.role.id)
    item = Menuitem.get(int(identifier))
    if not item: return mismatch()
    headline = localize("core", "menus.delete_headline")
    text = localize("core", "menus.delete_description") % (item.name)
    message = localize("core", "menus.delete_success")
    return delete_form(item, headline, text, message, "/menus",
                       template = "core/administration/confirm.html",
                       navigation = navigation)

# Edit Menu
# -------------------------------------------------------------------------------- #
@blueprint.route("/menus/<identifier>/update", methods = ["GET", "POST"])
def update(identifier):
    navigation = menubar("administration", g.role.id)
    item = Menuitem.get(int(identifier))
    form = FormMenu(obj = item)
    form.menubar_id.choices = [(bar.id, bar.name) for bar in Menubar.all()]
    if not item: return mismatch()
    headline = localize("core", "menus.update_headline")
    message = localize("core", "menus.update_success")
    return update_form(item, form, headline, message, "/menus",
                       template = "core/administration/form.html",
                       navigation = navigation)
