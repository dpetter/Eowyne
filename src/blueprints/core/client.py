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
from flask_wtf.form import Form
from werkzeug.utils import redirect
from wtforms.fields.simple import TextField, PasswordField
from wtforms.validators import DataRequired

from app.globals import mailservice
from blueprints import render
from models.session import Session
from models.user import User
from natives.role import Role
from utility.generator import randomkey


blueprint = Blueprint("Client Controller", __name__)


# Forms
# -------------------------------------------------------------------------------- #
class FormSignin(Form):
    email       = TextField("email", validators = [DataRequired()])
    password    = PasswordField("password", validators = [DataRequired()])

class FormRegister(Form):
    name        = TextField("name", validators = [DataRequired()])
    email       = TextField("email", validators = [DataRequired()])
    password    = PasswordField("password", validators = [DataRequired()])

class FormEmail(Form):
    email               = TextField("email", validators = [DataRequired()])

class FormPassword(Form):
    password            = PasswordField("password", validators = [DataRequired()])


# Sign in
# -------------------------------------------------------------------------------- #
@blueprint.route("/signin", methods = ["GET", "POST"])
def signin():
    form = FormSignin()
    if form.validate_on_submit():
        user = User.unique((User.email == form.email.data) &
                           (User.password == form.password.data))
        if user:
            g.session.user_id = user.id
            Session.update(g.session)
            flash("Labels.signinSuccess")
            flash(user.name)
            return redirect("/")
        else:
            flash("Labels.signinError")
    return render("core/signin.html", form = form, action = request.path)

# Sign out
# -------------------------------------------------------------------------------- #
@blueprint.route("/signout", methods = ["GET"])
def signout():
    g.session.user_id = 1
    Session.update(g.session)
    flash("Labels.signoutSuccess")
    return redirect("/")

# Register
# -------------------------------------------------------------------------------- #
@blueprint.route("/register", methods = ["GET", "POST"])
def register():
    form = FormRegister()
    if form.validate_on_submit():
        if User.find(User.email == form.email.data):
            flash("Labels.emailTaken")
        elif User.find(User.name == form.name.data):
            flash("Labels.nameTaken")
        else:
            key = randomkey(24, form.name.data)
            user = User(Role.get(4), form.email.data, form.name.data,
                        form.password.data, key)
            User.create(user)
            link = "http://localhost:5000/register/" + key
            mailservice.send([form.email.data], "TITLE", link)
            flash("Labels.registerSuccess")
            return redirect("/")
    return render("core/register.html", form = form)

# Unlock
# -------------------------------------------------------------------------------- #
@blueprint.route("/register/<key>", methods = ["GET"])
def unlock(key):
    user = User.unique(User.generated == key)
    if not user:
        flash("Labels.noAccount")
    else:
        user.generated = ""
        user.role = Role.get(3)
        User.update(user)
        g.session.user_id = user.id
        Session.update(g.session)
        flash("Labels.unlockSuccess")
    return redirect("/")

# Reset
# -------------------------------------------------------------------------------- #
@blueprint.route("/reset", methods = ["GET", "POST"])
def reset():
    form = FormEmail()
    if form.validate_on_submit():
        user = User.unique(User.email == form.email.data)
        if not user:
            flash("Labels.noAccount")
        else:
            key = randomkey(24, user.name)
            user.generated = key
            User.update(user)
            link = "http://localhost:5000/reset/" + key
            mailservice.send([form.email.data], "RESET PASS", link)
            flash("Labels.resetSuccess")
            return redirect("/")
    return render("core/email.html", form = form)

# Update Password
# -------------------------------------------------------------------------------- #
@blueprint.route("/reset/<key>", methods = ["GET", "POST"])
def updatepassword(key):
    form = FormPassword()
    if form.validate_on_submit():
        user = User.unique(User.generated == key)
        if not user:
            flash("Labels.noAccount")
        else:
            user.generated = ""
            user.password = form.password.data
            User.update(user)
            flash("Labels.resetSuccess")
            return redirect("/")
    return render("core/password.html", form = form, key = key)