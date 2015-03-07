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
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, DateTime, String

from models import Model


class Session(Model):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Sessions"
    
    id                  = Column(Integer, primary_key = True)
    createdOn           = Column(DateTime)
    changedOn           = Column(DateTime)
    key                 = Column(String(32), unique = True)
    ip                  = Column(String(32))
    user_id             = Column(Integer, ForeignKey("Users.id"))
