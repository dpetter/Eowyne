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
from flask.globals import request
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, DateTime, String

from models import Model
from utility.keyutility import randomkey
from utility.log import Log


class Session(Model):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Sessions"
    
    id                  = Column(Integer, primary_key = True)
    createdOn           = Column(DateTime)
    changedOn           = Column(DateTime)
    key                 = Column(String(32), unique = True)
    ip                  = Column(String(32))
    user_id             = Column(Integer, ForeignKey("Users.id"))
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def acquire(cls, cookie):
        '''
        Acquires the current session over the remote client's cookie. The acquired
        session always holds the user the client is signed on with or guest if he
        is not signed on.
        '''
        session = None
        if "sKey" in cookie:
            session = cls.unique((cls.key == cookie["sKey"]) & \
                                 (cls.ip == request.remote_addr))
        if not session:
            Log.debug(__name__, "Creating new session ...")
            session = cls()
            session.key     = randomkey(24)
            session.user_id = 1
            session.ip      = request.remote_addr
            Session.create(session)
        Log.debug(__name__, "Session acquired (%s) ..." % (session.key))
        cookie["sKey"] = session.key
        return session