# -*- coding: utf-8 -*-
#
# Models
#
# Extend this class for a database mapped model. You must add the line
# __mapper_args__     = {"concrete": True}
# directly under your class definition.
#
# A model must have the following fields:
#    id           = Column(Integer, primary_key = True)
# It can have the fields
#    createdOn    = Column(DateTime)
#    changedOn    = Column(DateTime)
# which are automatically updated when using create() or update().
#
# You can define any number of additional fields and methods.
#
# Created by dp on 2014-12-18.
# ================================================================================ #
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer

from core.shared import db, log


class Model(db.Model):
    __tablename__       = "Model"
    __batch__           = False     # Do not touch this
    
    id                  = Column(Integer, primary_key = True)
    
    # ---------------------------------------------------------------------------- #
    def create(self):
        '''
        Adds this item to the database.
        '''
        self.createdOn = datetime.now()
        self.changedOn = datetime.now()
        try:
            db.session.add(self)  # @UndefinedVariable
            if not self.__batch__: db.session.commit()  # @UndefinedVariable
            return True
        except IntegrityError as ex:
            log.error(str(ex))
            db.session.rollback()  # @UndefinedVariable
            return False
    
    # ---------------------------------------------------------------------------- #
    def delete(self):
        '''
        Deletes this item from the database.
        '''
        try:
            db.session.delete(self)  # @UndefinedVariable
            if not self.__batch__: db.session.commit()  # @UndefinedVariable
            return True
        except IntegrityError as ex:
            log.error(self.__class__.__name__, str(ex))
            db.session.rollback()  # @UndefinedVariable
            return False
    
    # ---------------------------------------------------------------------------- #
    def update(self):
        '''
        Saves all changes to this item to the database.
        '''
        try:
            self.changedOn = datetime.now()
            if not self.__batch__: db.session.commit()  # @UndefinedVariable
            return True
        except IntegrityError as ex:
            log.error(str(ex))
            db.session.rollback()  # @UndefinedVariable
            return False
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def total(cls):
        '''
        Returns the number of columns in the table.
        '''
        return db.session.query(func.count(cls.id)).scalar()  # @UndefinedVariable
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def get(cls, identifier):
        '''
        Fetches the item with the given id from the database and returns it.
        Returns None if no such item exists.
        '''
        if not identifier: return None
        try:
            return cls.query.get(identifier)
        except IntegrityError as ex:
            log.error(str(ex))
            return None
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def all(cls):
        '''
        Returns a list of all items in this table.
        '''
        try:
            return cls.query.all()
        except IntegrityError as ex:
            log.error(str(ex))
            return []
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def find(cls, *criteria):
        '''
        Returns a list of all items that match the given criteria.
        '''
        try:
            return cls.query.filter(*criteria).all()
        except IntegrityError as ex:
            log.error(str(ex))
            return []
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def unique(cls, *criteria):
        '''
        If there's exactly one item matching the given criteria it is returned.
        Otherwise None is returned.
        '''
        try:
            items = cls.query.filter(*criteria).all()
            if (not items) or (len(items) != 1): return None
            return items[0]
        except IntegrityError as ex:
            log.error(str(ex))
            return None
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def batch(cls, function):
        '''
        Pass a function performing database updates. Transaction is only submitted
        after all updates have been performed. This is faster than performing them
        one after another.
        '''
        cls.__batch__ = True
        function()
        cls.__batch__ = False
        try:
            db.session.commit()  # @UndefinedVariable
        except IntegrityError as ex:
            log.error(str(ex))