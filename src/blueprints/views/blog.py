from flask.blueprints import Blueprint
from flask.globals import g
from flask_wtf.form import Form
from wtforms.fields.simple import TextField, SubmitField
from wtforms.validators import DataRequired

from blueprints import render, create_form, delete_form, update_form
from models.blog import Blog
from natives.menu import menubar, contextmenu


blueprint = Blueprint("Blog Controller", __name__)


# Forms
# -------------------------------------------------------------------------------- #
class FormBlog(Form):
    title       = TextField("Title", validators = [DataRequired()])
    content     = TextField("Content", validators = [DataRequired()])
    confirm     = SubmitField("Confirm")
    cancel      = SubmitField("Cancel")


# Default route: View the latest blog entry.
# -------------------------------------------------------------------------------- #
@blueprint.route("/blog", defaults = {"identifier": 0}, methods = ["GET"])
@blueprint.route("/blog/<identifier>", methods = ["GET"])
def blog(identifier):
    try:
        actions = menubar("blog", g.role.id)
        i = int(identifier)
        if i == 0:
            item = Blog.query.order_by(Blog.changedOn.desc()).limit(1).all()[0]
        else:
            item = Blog.get(int(i))
        ownership = (item.author_id == g.user.id)
        item.actions = contextmenu("blog", g.role.id, ownership)            
        return render("modules/blog.html", item = item, actions = actions)
    except Exception as e:
        return str(e)

@blueprint.route("/blog/list", methods = ["GET"])
def listentry():
    return "HI"

# Create Blog Entry
# -------------------------------------------------------------------------------- #
@blueprint.route("/blog/create", methods = ["GET", "POST"])
def createentry():
    item = Blog()
    item.author_id = g.user.id
    return create_form(FormBlog(), item, "Created blog entry.", "/blog")

# Delete Blog Entry
# -------------------------------------------------------------------------------- #
@blueprint.route("/blog/<identifier>/delete", methods = ["GET", "POST"])
def delete_entry(identifier):
    item = Blog.get(int(identifier))
    if not item: return "NO SUCH OBJECT"
    headline = "%s löschen?" % (item.title)
    text = "Menü %s wirklich löschen?" % (item.title)
    return delete_form(item, headline, text, "Deleted blog entry.", "/blog",
                       "/blog/%s" % (identifier))

# Edit Blog Entry
# -------------------------------------------------------------------------------- #
@blueprint.route("/blog/<identifier>/update", methods = ["GET", "POST"])
def update_entry(identifier):
    item = Blog.get(int(identifier))
    if not item: return "NO SUCH OBJECT"
    return update_form(FormBlog(obj = item), item, "Updated blog entry.",
                       "/blog/%s" % (identifier))