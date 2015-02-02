# -*- coding: utf-8 -*-
#
# Rule
#
# Blueprint for rule administration.
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
from natives.rule import Rule


blueprint = Blueprint("Rule Controller", __name__)


# Forms
# -------------------------------------------------------------------------------- #
class FormRule(Form):
    route       = TextField("route", validators = [DataRequired()])
    role_id     = SelectField("role_id", coerce = int)
    insert      = SelectField("insert",
                              choices = [(item, item) for item in Rule.permissions])
    remove      = SelectField("remove",
                              choices = [(item, item) for item in Rule.permissions])
    change      = SelectField("change",
                              choices = [(item, item) for item in Rule.permissions])
    view        = SelectField("view",
                              choices = [(item, item) for item in Rule.permissions])
    search      = SelectField("search",
                              choices = [(item, item) for item in Rule.permissions])
    confirm     = SubmitField("Confirm")
    cancel      = SubmitField("Cancel")


# Default route: View a list of all rules
# -------------------------------------------------------------------------------- #
@blueprint.route("/rules", methods = ["GET"])
def entries():
    items = Rule.all()
    actions = menubar("rule", g.role.id)
    for item in items: item.actions = contextmenu("rule", g.role.id)
    return render("core/rule_list.html", items = items, actions = actions)

# Create Rule
# -------------------------------------------------------------------------------- #
@blueprint.route("/rules/create", methods = ["GET", "POST"])
def create():
    item = Rule(None, None, None, None, None, None, None)
    form = FormRule()
    form.role_id.choices = [(role.id, role.name) for role in Role.all()]
    return create_form(form, item, "Created new rule.", "/rules")

# Delete Rule
# -------------------------------------------------------------------------------- #
@blueprint.route("/rules/<identifier>/delete", methods = ["GET", "POST"])
def delete(identifier):
    item = Rule.get(int(identifier))
    if not item: return "NO SUCH OBJECT"
    headline = "%s löschen?" % (item.route)
    text = "Regel %s wirklich löschen?" % (item.route)
    return delete_form(item, headline, text, "Deleted rule.", "/rules")

# Edit Rule
# -------------------------------------------------------------------------------- #
@blueprint.route("/rules/<identifier>/update", methods = ["GET", "POST"])
def update(identifier):
    item = Rule.get(int(identifier))
    if not item: return "NO SUCH OBJECT"
    form = FormRule(obj = item)
    form.role_id.choices = [(role.id, role.name) for role in Role.all()]
    return update_form(form, item, "Updated rule.", "/rules")
