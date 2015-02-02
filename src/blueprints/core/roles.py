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
from flask_wtf.form import Form
from wtforms.fields.core import SelectField
from wtforms.fields.simple import TextField, SubmitField
from wtforms.validators import DataRequired

from blueprints import render, create_form, delete_form, update_form
from natives.menu import menubar, contextmenu
from natives.role import Role


blueprint = Blueprint("Role Controller", __name__)


# Forms
# -------------------------------------------------------------------------------- #
class FormRole(Form):
    name        = TextField("name", validators = [DataRequired()])
    description = TextField("description", validators = [DataRequired()])
    parent_id   = SelectField("parent_id", coerce = int)
    confirm     = SubmitField("Confirm")
    cancel      = SubmitField("Cancel")


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
    return create_form(form, item, "Created new role.", "/roles")

# Delete Role
# -------------------------------------------------------------------------------- #
@blueprint.route("/roles/<identifier>/delete", methods = ["GET", "POST"])
def delete(identifier):
    item = Role.get(int(identifier))
    if not item: return "NO SUCH OBJECT"
    headline = "%s löschen?" % (item.name)
    text = "Rolle %s wirklich löschen?" % (item.name)
    return delete_form(item, headline, text, "Deleted role.", "/roles")

# Edit Role
# -------------------------------------------------------------------------------- #
@blueprint.route("/roles/<identifier>/update", methods = ["GET", "POST"])
def update(identifier):
    item = Role.get(int(identifier))
    if not item: return "NO SUCH OBJECT"
    form = FormRole(obj = item)
    form.parent_id.choices = [(role.id, role.name) for role in Role.all()]
    return update_form(form, item, "Updated role.", "/roles")
