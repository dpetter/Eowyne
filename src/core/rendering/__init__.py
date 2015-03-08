# -*- coding: utf-8 -*-
#
# Rendering
#
# Adds helper functions for rendering forms and views.
#
# Created on 2015-02-02.
# ================================================================================ #
from flask.globals import request
from flask.helpers import flash
from flask.templating import render_template
from flask_wtf.form import Form
from jinja2.exceptions import TemplateNotFound
from werkzeug.utils import redirect
from wtforms.fields.simple import SubmitField

from utility.log import Log


# Forms
# -------------------------------------------------------------------------------- #
class DefaultForm(Form):
    confirm = SubmitField("Confirm")
    cancel = SubmitField("Deny")


# -------------------------------------------------------------------------------- #
def render(template, **kwargs):
    '''
    Renders a template. Catches the template not found exception and shows the
    missing template error page if caught.
    '''
    try:
        return render_template(template, **kwargs)
    except TemplateNotFound:
        Log.error(__name__, "Template not found: %s." % (template))
        return render_template("error/template.html", name = template)

# -------------------------------------------------------------------------------- #
def mismatch():
    '''
    Renders "No matching item" page.
    '''
    return render("error/match.html")

# -------------------------------------------------------------------------------- #
def confirmation(headline, text, on_confirm, on_cancel,
                 template = "base/confirm.html", **args):
    '''
    Renders a confirmation form that has a headline, a descriptive text and two
    buttons - confirm and cancel. on_confirm and on_cancel are functions that have
    to perform the desired actions and return a redirect or html.
    '''
    form = DefaultForm()
    if form.cancel.data == True: return on_cancel()
    elif form.validate_on_submit(): return on_confirm()
    return render(template, form = form, action = request.path,
                  headline = headline, text = text, **args)

# -------------------------------------------------------------------------------- #
def editor(form, headline, on_confirm, on_cancel, template = "base/form.html",
           **args):
    '''
    Renders a form. The form can have various elements and two buttons - confirm
    and cancel. on_confirm and on_cancel are functions that have
    to perform the desired actions and return a redirect or html.
    '''
    if form.cancel.data == True: return on_cancel()
    elif form.validate_on_submit(): return on_confirm()
    return render(template, form = form, action = request.path, headline = headline,
                  **args)

# -------------------------------------------------------------------------------- #
def create_form(item, form, headline, message, on_confirm, on_cancel = None,
                template = "base/form.html", **args):
    '''
    Renders a default create form. If the user confirms the item is filled
    with data from the form and saved. Then message is flashed and the user is
    redirected to on_confirm. If the user cancels he is redirected to on_cancel.
    '''
    def o_con():
        form.populate_obj(item)
        item.create()
        flash(message)
        return redirect(on_confirm)
    if on_cancel: o_can = lambda: redirect(on_cancel)
    else: o_can = lambda: redirect(on_confirm)
    return editor(form, headline, o_con, o_can, template, **args)

# -------------------------------------------------------------------------------- #
def delete_form(item, headline, text, message, on_confirm, on_cancel = None,
                template = "base/confirm.html", **args):
    '''
    Renders a default delete form showing a headline and a description.
    If the user confirms the item is deleted, message is flashed and he is
    redirected to on_confirm. If the user cancels he is redirected to on_cancel.
    '''
    def o_con():
        item.delete()
        flash(message)
        return redirect(on_confirm)
    if on_cancel: o_can = lambda: redirect(on_cancel)
    else: o_can = lambda: redirect(on_confirm)
    return confirmation(headline, text, o_con, o_can, template, **args)

# -------------------------------------------------------------------------------- #
def update_form(item, form, headline, message, on_confirm, on_cancel = None,
                template = "base/form.html", **args):
    '''
    Renders a default update form. If the user confirms the item is filled
    with data from the form and saved. Then message is flashed and the user is
    redirected to on_confirm. If the user cancels he is redirected to on_cancel.
    '''
    def o_con():
        form.populate_obj(item)
        item.update()
        flash(message)
        return redirect(on_confirm)
    if on_cancel: o_can = lambda: redirect(on_cancel)
    else: o_can = lambda: redirect(on_confirm)
    return editor(form, headline, o_con, o_can, template, **args)
