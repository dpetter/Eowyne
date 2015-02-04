# -*- coding: utf-8 -*-
#
# Role
#
# Blueprint for role administration.
#
# Created by dp on 2014-12-25.
# ================================================================================ #
from flask.blueprints import Blueprint
from flask.globals import g
from wtforms.fields.core import SelectField
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired

from blueprints import DefaultForm, render, create_form, mismatch, delete_form, \
    update_form
from natives.menu import menubar, contextmenu
from natives.role import Role
from utility.localization import localize


blueprint = Blueprint("Role Controller", __name__)


# Forms
# -------------------------------------------------------------------------------- #
class FormRole(DefaultForm):
    name        = TextField(localize("administration", "roles.field_name"),
                            validators = [DataRequired()])
    description = TextField(localize("administration", "roles.field_description"),
                            validators = [DataRequired()])
    parent_id   = SelectField(localize("administration", "roles.field_parent_id"),
                              coerce = int)


# Default route: View a list of all roles
# -------------------------------------------------------------------------------- #
@blueprint.route("/roles", methods = ["GET"])
def entries():
    items = Role.all()
    actions = menubar("role", g.role.id)
    for item in items: item.actions = contextmenu("role", g.role.id)
    return render("core/role_list.html", items = items, actions = actions)

# Create Role
# -------------------------------------------------------------------------------- #
@blueprint.route("/roles/create", methods = ["GET", "POST"])
def create():
    item = Role()
    form = FormRole()
    form.parent_id.choices = [(role.id, role.name) for role in Role.all()]
    headline = localize("administration", "roles.create_headline")
    message = localize("administration", "roles.create_success")
    return create_form(item, form, headline, message, "/roles")

# Delete Role
# -------------------------------------------------------------------------------- #
@blueprint.route("/roles/<identifier>/delete", methods = ["GET", "POST"])
def delete(identifier):
    item = Role.get(int(identifier))
    if not item: return mismatch()
    headline = localize("administration", "roles.delete_headline")
    text = localize("administration", "roles.delete_description") % (item.name)
    message = localize("administration", "roles.delete_success")
    return delete_form(item, headline, text, message, "/roles")

# Edit Role
# -------------------------------------------------------------------------------- #
@blueprint.route("/roles/<identifier>/update", methods = ["GET", "POST"])
def update(identifier):
    item = Role.get(int(identifier))
    if not item: return mismatch()
    form = FormRole(obj = item)
    form.parent_id.choices = [(role.id, role.name) for role in Role.all()]
    headline = localize("administration", "roles.update_headline")
    message = localize("administration", "roles.update_success")
    return update_form(item, form, headline, message, "/roles")
