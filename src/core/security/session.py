# -*- coding: utf-8 -*-
#
# Session
#
# A Session stores the remote client's ip, a randomly generated key and the
# sessions user id. acquire() checks the client's ip and cookie to retrieve his
# unique session.
#
# Created by dp on 2015-01-02.
# ================================================================================ #
from flask.globals import session, request, g
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, DateTime, String

from core.shared import log
from core.utility.keyutility import randomkey
from models import Model


# Classes
# -------------------------------------------------------------------------------- #
class Session(Model):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Sessions"
    
    id                  = Column(Integer, primary_key = True)
    createdOn           = Column(DateTime)
    changedOn           = Column(DateTime)
    key                 = Column(String(32), unique = True)
    ip                  = Column(String(32))
    user_id             = Column(Integer, ForeignKey("Users.id"))


# Functions
# -------------------------------------------------------------------------------- #
def acquire_session():
    '''
    Acquires the current session over the remote client's cookie. The acquired
    session always holds the user the client is signed on with or guest if he
    is not signed on.
    
    @returns            The session.
    '''
    result = None
    if "sKey" in session:
        result = Session.unique((Session.key == session["sKey"]) & \
                                (Session.ip == request.remote_addr))
    if not result: result = create_session()
    log.debug("Session acquired (key = %s)." % (result.key))
    session["sKey"] = result.key
    return result

def create_session():
    '''
    @returns            A new guest session.
    '''
    log.debug("Creating new session ...")
    result          = Session()
    result.key      = randomkey(24)
    result.user_id  = 1
    result.ip       = request.remote_addr
    result.create()
    return result

def is_authenticated():
    '''
    @returns            True if this request comes from a logged in user.
    '''
    g.session       = acquire_session()
    return g.session.user_id >= 2
