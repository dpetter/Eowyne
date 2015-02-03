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

from blueprints import render, create_form, delete_form, update_form, mismatch
from natives.menu import menubar, contextmenu
from natives.role import Role
from natives.rule import Rule
from utility.localization import localize


blueprint = Blueprint("Rule Controller", __name__)


# Forms
# -------------------------------------------------------------------------------- #
class FormRule(Form):
    route       = TextField(localize("administration", "rules.field_route"),
                            validators = [DataRequired()])
    role_id     = SelectField(localize("administration", "rules.field_role"),
                              coerce = int)
    insert      = SelectField(localize("administration", "rules.field_insert"),
                              choices = [(item, item) for item in Rule.permissions])
    remove      = SelectField(localize("administration", "rules.field_remove"),
                              choices = [(item, item) for item in Rule.permissions])
    change      = SelectField(localize("administration", "rules.field_change"),
                              choices = [(item, item) for item in Rule.permissions])
    view        = SelectField(localize("administration", "rules.field_view"),
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
    headline = localize("administration", "rules.create_headline")
    message = localize("administration", "rules.create_success")
    return create_form(item, form, headline, message, "/rules")

# Delete Rule
# -------------------------------------------------------------------------------- #
@blueprint.route("/rules/<identifier>/delete", methods = ["GET", "POST"])
def delete(identifier):
    item = Rule.get(int(identifier))
    if not item: return mismatch()
    headline = localize("administration", "rules.delete_headline")
    text = localize("administration", "rules.delete_description") % (item.route)
    message = localize("administration", "rules.delete_success")
    return delete_form(item, headline, text, message, "/rules")

# Edit Rule
# -------------------------------------------------------------------------------- #
@blueprint.route("/rules/<identifier>/update", methods = ["GET", "POST"])
def update(identifier):
    item = Rule.get(int(identifier))
    if not item: return mismatch()
    form = FormRule(obj = item)
    form.role_id.choices = [(role.id, role.name) for role in Role.all()]
    headline = localize("administration", "rules.update_headline")
    message = localize("administration", "rules.update_success")
    return update_form(item, form, headline, message, "/rules")
