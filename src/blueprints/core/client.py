# -*- coding: utf-8 -*-
#
# Client
#
# Provides client related functionality - signing in, registering, etc.
#
# Created by dp on 2015-02-01.
# ================================================================================ #
from flask.blueprints import Blueprint
from flask.globals import request, g
from flask.helpers import flash
from werkzeug.utils import redirect
from wtforms.fields.simple import TextField, PasswordField
from wtforms.validators import Email, DataRequired

from app.globals import mailservice
from blueprints import editor, DefaultForm
from models.user import User
from natives.role import Role
from utility.generator import randomkey
from utility.localization import localize


blueprint = Blueprint("Client Controller", __name__)


# Forms
# -------------------------------------------------------------------------------- #
class FormSignin(DefaultForm):
    email       = TextField(localize("administration", "client.field_email"),
                            validators = [Email()])
    password    = PasswordField(localize("administration", "client.field_password"),
                                validators = [DataRequired()])

class FormRegister(DefaultForm):
    name        = TextField(localize("administration", "client.field_username"),
                            validators = [DataRequired()])
    email       = TextField(localize("administration", "client.field_email"),
                            validators = [Email()])
    password    = PasswordField(localize("administration", "client.field_password"),
                                validators = [DataRequired()])

class FormEmail(DefaultForm):
    email       = TextField(localize("administration", "client.field_email"),
                            validators = [Email()])

class FormPassword(DefaultForm):
    password    = PasswordField(localize("administration", "client.field_password"),
                                validators = [DataRequired()])


# Sign in
# -------------------------------------------------------------------------------- #
@blueprint.route("/signin", methods = ["GET", "POST"])
def signin():
    form = FormSignin()
    def confirm():
        email = form.email.data
        # TODO: Encrypt here.
        password = form.password.data
        user = User.unique((User.email == email) & (User.password == password))
        if not user:
            flash(localize("administration", "client.signin_failure"))
            return redirect(request.path)
        g.session.user_id = user.id
        g.session.update()
        flash(localize("administration", "client.signin_success") % (user.name))
        return redirect("/")
    return editor(form, "", confirm, lambda: redirect("/"), "core/signin.html")

# Sign out
# -------------------------------------------------------------------------------- #
@blueprint.route("/signout", methods = ["GET"])
def signout():
    g.session.user_id = 1
    g.session.update()
    flash(localize("administration", "client.signout_success"))
    return redirect("/")

# Register
# -------------------------------------------------------------------------------- #
@blueprint.route("/register", methods = ["GET", "POST"])
def register():
    form = FormRegister()
    def confirm():
        if User.find(User.email == form.email.data):
            flash(localize("administration", "client.email_taken"))
            return redirect(request.path)
        if User.find(User.name == form.name.data):
            flash(localize("administration", "client.name_taken"))
            return redirect(request.path)
        key = randomkey(24, form.name.data)
        # TODO: Encrypt here.
        password = form.password.data
        user = User(Role.get(4), form.email.data, form.name.data, password, key)
        user.create()
        # TODO: Write beautiful mail.
        link = "http://localhost:5000/register/" + key
        mailservice.send([form.email.data], "TITLE", link)
        flash(localize("administration", "client.register_success"))
        return redirect("/")
    return editor(form, "", confirm, lambda: redirect("/"), "core/register.html")

# Unlock
# -------------------------------------------------------------------------------- #
@blueprint.route("/register/<key>", methods = ["GET"])
def register_unlock(key):
    user = User.unique(User.generated == key)
    if not user: flash(localize("administration", "client.no_account"))
    user.generated = ""
    user.role = Role.get(3)
    user.update()
    g.session.user_id = user.id
    g.session.update()
    flash(localize("administration", "client.unlock_success") % (user.name))
    return redirect("/")

# Reset
# -------------------------------------------------------------------------------- #
@blueprint.route("/reset", methods = ["GET", "POST"])
def reset():
    form = FormEmail()
    def confirm():
        user = User.unique(User.email == form.email.data)
        if not user:
            flash(localize("administration", "client.no_account"))
            return redirect(request.path)
        key = randomkey(24, user.name)
        user.generated = key
        user.update()
        # TODO: Write beautiful mail.
        link = "http://localhost:5000/reset/" + key
        mailservice.send([form.email.data], "TITLE", link)
        flash(localize("administration", "client.reset_success"))
        return redirect("/")
    return editor(form, "", confirm, lambda: redirect("/"), "core/email.html")

# Update Password
# -------------------------------------------------------------------------------- #
@blueprint.route("/reset/<key>", methods = ["GET", "POST"])
def reset_update(key):
    form = FormPassword()
    def confirm():
        user = User.unique(User.generated == key)
        if not user:
            flash(localize("administration", "client.no_account"))
            return redirect(request.path)
        user.generated = ""
        # TODO: Encrypt here.
        user.password = form.password.data
        user.update()
        flash(localize("administration", "client.password_success"))
        return redirect("/")
    return editor(form, "", confirm, lambda: redirect("/"), "core/password.html")
