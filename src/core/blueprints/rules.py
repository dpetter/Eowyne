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
from wtforms.fields.core import SelectField
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired

from core.natives.menu import menubar, contextmenu
from core.natives.role import Role
from core.natives.rule import Rule
from core.rendering import DefaultForm, render, create_form, mismatch, delete_form, \
    update_form
from utility.localization import localize


blueprint = Blueprint("Rule Controller", __name__)


# Forms
# -------------------------------------------------------------------------------- #
class FormRule(DefaultForm):
    route       = TextField(localize("core", "rules.field_route"),
                            validators = [DataRequired()])
    role_id     = SelectField(localize("core", "rules.field_role"),
                              coerce = int)
    insert      = SelectField(localize("core", "rules.field_insert"),
                              choices = [(item, item) for item in Rule.permissions])
    remove      = SelectField(localize("core", "rules.field_remove"),
                              choices = [(item, item) for item in Rule.permissions])
    change      = SelectField(localize("core", "rules.field_change"),
                              choices = [(item, item) for item in Rule.permissions])
    view        = SelectField(localize("core", "rules.field_view"),
                              choices = [(item, item) for item in Rule.permissions])


# Default route: View a list of all rules
# -------------------------------------------------------------------------------- #
@blueprint.route("/rules", methods = ["GET"])
def entries():
    items = Rule.all()
    actions = menubar("rule", g.role.id)
    for item in items: item.actions = contextmenu("rule", g.role.id)
    return render("core/administration/rules.html", items = items, actions = actions)

# Create Rule
# -------------------------------------------------------------------------------- #
@blueprint.route("/rules/create", methods = ["GET", "POST"])
def create():
    item = Rule()
    form = FormRule()
    form.role_id.choices = [(role.id, role.name) for role in Role.all()]
    headline = localize("core", "rules.create_headline")
    message = localize("core", "rules.create_success")
    return create_form(item, form, headline, message, "/rules")

# Delete Rule
# -------------------------------------------------------------------------------- #
@blueprint.route("/rules/<identifier>/delete", methods = ["GET", "POST"])
def delete(identifier):
    item = Rule.get(int(identifier))
    if not item: return mismatch()
    headline = localize("core", "rules.delete_headline")
    text = localize("core", "rules.delete_description") % (item.route)
    message = localize("core", "rules.delete_success")
    return delete_form(item, headline, text, message, "/rules")

# Edit Rule
# -------------------------------------------------------------------------------- #
@blueprint.route("/rules/<identifier>/update", methods = ["GET", "POST"])
def update(identifier):
    item = Rule.get(int(identifier))
    if not item: return mismatch()
    form = FormRule(obj = item)
    form.role_id.choices = [(role.id, role.name) for role in Role.all()]
    headline = localize("core", "rules.update_headline")
    message = localize("core", "rules.update_success")
    return update_form(item, form, headline, message, "/rules")
