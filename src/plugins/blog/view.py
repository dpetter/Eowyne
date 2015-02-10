from flask.blueprints import Blueprint
from flask.globals import g, request
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired

from core.natives.menu import menubar, contextmenu
from core.natives.rule import access
from core.rendering import DefaultForm, render, create_form, mismatch, forbidden, \
    delete_form, update_form
from plugins.blog.blog import Blog


blueprint = Blueprint("Blog Controller", __name__)


# Forms
# -------------------------------------------------------------------------------- #
class FormBlog(DefaultForm):
    title       = TextField("Title", validators = [DataRequired()])
    description = TextField("Content", validators = [DataRequired()])


# Default route: View the latest blog entry.
# -------------------------------------------------------------------------------- #
@blueprint.route("/blog", defaults = {"identifier": 0}, methods = ["GET"])
@blueprint.route("/blog/<identifier>", methods = ["GET"])
def blog(identifier):
    actions = menubar("blog", g.role.id)
    i = int(identifier)
    if i == 0:
        item = Blog.query.order_by(Blog.changedOn.desc()).first()# @UndefinedVariable
    else: item = Blog.get(i)
    if not item: return render("modules/blog-empty.html", actions = actions)
    ownership = (item.author == g.user)
    item.actions = contextmenu("blog", g.role.id, ownership)            
    return render("modules/blog.html", item = item, actions = actions)

# List all blog entries
# -------------------------------------------------------------------------------- #
@blueprint.route("/blog/list", methods = ["GET"])
def listentries():
    actions = menubar("blog", g.role.id)
    items = Blog.query.order_by(Blog.changedOn.desc()).all()  # @UndefinedVariable
    return render("modules/blog-list.html", items = items, actions = actions)

# Create Blog Entry
# -------------------------------------------------------------------------------- #
@blueprint.route("/blog/create", methods = ["GET", "POST"])
def create_entry():
    try:
        item = Blog()
        item.author_id = g.user.id
        return create_form(item, FormBlog(), "", "Created blog entry.", "/blog")
    except Exception as e:
        return(str(e))

# Delete Blog Entry
# -------------------------------------------------------------------------------- #
@blueprint.route("/blog/<identifier>/delete", methods = ["GET", "POST"])
def delete_entry(identifier):
    item = Blog.get(int(identifier))
    if not item: return mismatch()
    ownership = (item.author == g.user)
    if access(request.path, g.role.id, ownership) != 1: return forbidden()
    headline = "%s löschen?" % (item.title)
    text = "Menü %s wirklich löschen?" % (item.title)
    return delete_form(item, headline, text, "Deleted blog entry.", "/blog",
                       "/blog/%s" % (identifier))

# Edit Blog Entry
# -------------------------------------------------------------------------------- #
@blueprint.route("/blog/<identifier>/update", methods = ["GET", "POST"])
def update_entry(identifier):
    item = Blog.get(int(identifier))
    if not item: return mismatch()
    ownership = (item.author == g.user)
    if access(request.path, g.role.id, ownership) != 1: return forbidden()
    return update_form(item, FormBlog(obj = item), "", "Updated blog entry.",
                       "/blog/%s" % (identifier))