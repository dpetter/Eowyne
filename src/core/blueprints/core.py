# -*- coding: utf-8 -*-
#
# Core
#
# Contains views for the core functionality of the project.
# - Preparing the global scope before every request.
# - Administration pages for roles, rules and menus.
# - Static pages.
#
# Created by dp on 2015-02-02.
# ================================================================================ #
import time

from flask.blueprints import Blueprint
from flask.globals import request, g, session
from flask.helpers import flash
from werkzeug import redirect
from wtforms.fields.simple import TextField, PasswordField
from wtforms.validators import Email, DataRequired

from core import shared
from core.models.session import Session
from core.models.user import Client, User
from core.natives.menu import menubar, Menu
from core.natives.role import Role
from core.natives.rule import access, Rule
from core.rendering import DefaultForm, invalid, forbidden, render, editor
from core.shared import mailservice
from utility.generator import randomkey
from utility.localization import localize
from utility.log import Log


blueprint = Blueprint("Core Controller", __name__)


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


# -------------------------------------------------------------------------------- #
@blueprint.before_app_request
def beforerequest():
    Log.debug(__name__, "Incoming request")
    Log.debug(__name__, request.path)
    # The next line is to prevent the acquisition of globals when a static file
    # (style sheet, image, etc.) is requested. Since all files have an extension
    # but urls don't it simply checks whether the path contains a full stop.
    if "." in request.path: return
    heartbeat()
    if request.path.startswith(shared.noscope_url): return
    # Fill the global scope ...
    g.session       = Session.acquire(session)
    g.user          = Client.get(g.session.user_id)
    g.role          = g.user.role
    g.main_menu     = menubar("main", g.role.id)
    g.personal_menu = menubar("personal", g.role.id)
    g.extended_menu = menubar("extended", g.role.id)
    permitted       = access(request.path, g.role.id, True)
    if permitted == -1: return invalid()
    elif permitted == 0: return forbidden()

# -------------------------------------------------------------------------------- #
def heartbeat():
    try:
        now = time.time()
        if now - shared.time_elapsed < shared.heartbeat_time: return
        shared.time_elapsed = now
        Log.information(__name__, "Heartbeat")
        Role.heartbeat()
        Rule.heartbeat()
        Menu.heartbeat()
    except Exception as e:
        Log.error(__name__, "Heartbeat failed:" + str(e))

# -------------------------------------------------------------------------------- #
def is_authenticated():
    '''
    Returns True if this request comes from a logged in user.
    '''
    g.session       = Session.acquire(session)
    g.user          = Client.get(g.session.user_id)
    return g.user >= 3

# Show administration page
# -------------------------------------------------------------------------------- #
@blueprint.route("/administration", methods = ["GET"])
def administration():
    links = menubar("administration", g.role.id)
    return render("core/administration.html", links = links)

# Show static page
# -------------------------------------------------------------------------------- #
@blueprint.route("/", defaults = {"identifier": "index"}, methods = ["GET"])
@blueprint.route("/pages/<identifier>", methods = ["GET"])
def page(identifier):
    return render("pages/%s.html" % (identifier))

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
            flash(localize("core", "client.signin_failure"))
            return redirect(request.path)
        g.session.user_id = user.id
        g.session.update()
        flash(localize("core", "client.signin_success") % (user.name))
        return redirect("/")
    return editor(form, "", confirm, lambda: redirect("/"), "core/signin.html")

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
        # TODO: Encrypt here.
        password = form.password.data
        user = User(Role.get(4), form.email.data, form.name.data, password, key)
        user.create()
        link = "http://localhost:5000/register/" + key
        text = render("mail/register.html", name = user.name, link = link)
        mailservice.send([form.email.data], "Activate your account", text)
        flash(localize("core", "client.register_success"))
        return redirect("/")
    return editor(form, "", confirm, lambda: redirect("/"), "core/register.html")

# Unlock Account
# -------------------------------------------------------------------------------- #
@blueprint.route("/register/<key>", methods = ["GET"])
def register_unlock(key):
    user = User.unique(User.generated == key)
    if not user: flash(localize("core", "client.no_account"))
    user.generated = ""
    user.role = Role.get(3)
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
    return editor(form, "", confirm, lambda: redirect("/"), "core/email.html")

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
        # TODO: Encrypt here.
        user.password = form.password.data
        user.update()
        flash(localize("core", "client.password_success"))
        return redirect("/")
    return editor(form, "", confirm, lambda: redirect("/"), "core/password.html")
