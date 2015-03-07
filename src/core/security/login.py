# -*- coding: utf-8 -*-
#
# Clients
#
# Contains views for authenticating a client.
#
# Created by dp on 2015-02-02.
# ================================================================================ #
from flask.blueprints import Blueprint
from flask.globals import request, g, session
from flask.helpers import flash
from werkzeug import redirect
from wtforms.fields.simple import TextField, PasswordField
from wtforms.validators import Email, DataRequired

from core.rendering import DefaultForm, editor, render
from core.security.session import Session
from core.security.user import User
from core.shared import mailservice
from core.utility.keyutility import randomkey, match_password, hash_password
from core.utility.localization import localize
from utility.log import Log


blueprint = Blueprint("client-controller", __name__)


def acquire_session():
    '''
    Acquires the current session over the remote client's cookie. The acquired
    session always holds the user the client is signed on with or guest if he
    is not signed on.
    '''
    result = None
    if "sKey" in session:
        result = Session.unique((Session.key == session["sKey"]) & \
                                (Session.ip == request.remote_addr))
    if not result: result = create_session()
    Log.debug(__name__, "Session acquired (%s) ..." % (result.key))
    session["sKey"] = result.key
    return result

def create_session():
    '''
    '''
    Log.debug(__name__, "Creating new session ...")
    result = Session()
    result.key     = randomkey(24)
    result.user_id = 1
    result.ip      = request.remote_addr
    result.create()
    return result

# Forms
# -------------------------------------------------------------------------------- #
class FormSignin(DefaultForm):
    email       = TextField(localize("core", "client.field_email"),
                            validators = [Email()])
    password    = PasswordField(localize("core", "client.field_password"),
                                validators = [DataRequired()])

class FormRegister(DefaultForm):
    name        = TextField(localize("core", "client.field_username"),
                            validators = [DataRequired()])
    email       = TextField(localize("core", "client.field_email"),
                            validators = [Email()])
    password    = PasswordField(localize("core", "client.field_password"),
                                validators = [DataRequired()])

class FormEmail(DefaultForm):
    email       = TextField(localize("core", "client.field_email"),
                            validators = [Email()])

class FormPassword(DefaultForm):
    password    = PasswordField(localize("core", "client.field_password"),
                                validators = [DataRequired()])


# Sign in
# -------------------------------------------------------------------------------- #
@blueprint.route("/signin", methods = ["GET", "POST"])
def signin():
    form = FormSignin()
    def confirm():
        email = form.email.data
        user = User.unique(User.email == email)
        if not user or not match_password(form.password.data, user.password):
            flash(localize("core", "client.signin_failure"))
            return redirect(request.path)
        g.session.user_id = user.id
        g.session.update()
        flash(localize("core", "client.signin_success") % (user.name))
        return redirect("/")
    return editor(form, "", confirm, lambda: redirect("/"), "core/security/signin_form.html")

# Sign out
# -------------------------------------------------------------------------------- #
@blueprint.route("/signout", methods = ["GET"])
def signout():
    g.session.user_id = 1
    g.session.update()
    flash(localize("core", "client.signout_success"))
    return redirect("/")

# Register
# -------------------------------------------------------------------------------- #
@blueprint.route("/register", methods = ["GET", "POST"])
def register():
    form = FormRegister()
    def confirm():
        if User.find(User.email == form.email.data):
            flash(localize("core", "client.email_taken"))
            return redirect(request.path)
        if User.find(User.name == form.name.data):
            flash(localize("core", "client.name_taken"))
            return redirect(request.path)
        key = randomkey(24, form.name.data)
        user = User(4, form.email.data, form.name.data,
                    hash_password(form.password.data), key)
        user.create()
        link = "http://localhost:5000/register/" + key
        text = render("mail/register.html", name = user.name, link = link)
        mailservice.send([form.email.data], "Activate your account", text)
        flash(localize("core", "client.register_success"))
        return redirect("/")
    return editor(form, "", confirm, lambda: redirect("/"), "core/security/register_form.html")

# Unlock Account
# -------------------------------------------------------------------------------- #
@blueprint.route("/register/<key>", methods = ["GET"])
def register_unlock(key):
    user = User.unique(User.generated == key)
    if not user: flash(localize("core", "client.no_account"))
    user.generated = ""
    user.role_id = 3
    user.update()
    g.session.user_id = user.id
    g.session.update()
    flash(localize("core", "client.unlock_success") % (user.name))
    return redirect("/")

# Reset Password
# -------------------------------------------------------------------------------- #
@blueprint.route("/reset", methods = ["GET", "POST"])
def reset():
    form = FormEmail()
    def confirm():
        user = User.unique(User.email == form.email.data)
        if not user:
            flash(localize("core", "client.no_account"))
            return redirect(request.path)
        key = randomkey(24, user.name)
        user.generated = key
        user.update()
        link = "http://localhost:5000/reset/" + key
        text = render("mail/reset.html", name = user.name, link = link)
        mailservice.send([form.email.data], "Reset your password", text)
        flash(localize("core", "client.reset_success"))
        return redirect("/")
    return editor(form, "", confirm, lambda: redirect("/"), "core/security/email_form.html")

# Update Password
# -------------------------------------------------------------------------------- #
@blueprint.route("/reset/<key>", methods = ["GET", "POST"])
def reset_update(key):
    form = FormPassword()
    def confirm():
        user = User.unique(User.generated == key)
        if not user:
            flash(localize("core", "client.no_account"))
            return redirect(request.path)
        user.generated = ""
        user.password = hash_password(form.password.data)
        user.update()
        flash(localize("core", "client.password_success"))
        return redirect("/")
    return editor(form, "", confirm, lambda: redirect("/"), "core/security/password_form.html")
