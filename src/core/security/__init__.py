from flask.globals import g

from core.security.rule import can_access
from core.security.user import Client

from .session import acquire_session, is_authenticated


# Functions
# -------------------------------------------------------------------------------- #
def is_authorized(route, owner = None):
    g.session       = acquire_session()
    g.user          = Client.get(g.session.user_id)
    return can_access(route, g.user.role_id, owner)
