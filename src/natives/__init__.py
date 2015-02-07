from _functools import reduce
from datetime import datetime

from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer

from app.shared import db
from natives.expressions import parseExpression
from natives.storage import fields, storage, store
from utility.log import Log


class Native(db.Model):
    __tablename__       = "Native"
    __batch__           = False     # Do not touch this
    __list__            = []        # Do not touch this
    __fields__          = None      # Do not touch this
    __store__           = None      # Do not touch this
    
    id                  = Column(Integer, primary_key = True)
    
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
        db.session.commit()  # @UndefinedVariable
        cls.__list__ = []
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def load(cls):
        '''
        Loads the table into memory.
        '''
        if cls.__batch__: return True
        if not cls.__fields__: cls.__fields__ = fields(cls)
        if not cls.__store__: cls.__store__ = storage(cls)
        Log.debug(cls.__name__, "Loading cache...")
        items = cls.query.all()
        cls.__list__ = store(cls, items)
        Log.debug(cls.__name__, "Cache loaded...")
        return True
    
    # ---------------------------------------------------------------------------- #
    def create(self):
        '''
        Adds the item to the database.
        '''
        cls = self.__class__
        if not cls.__list__: cls.load()
        self.createdOn = datetime.now()
        self.changedOn = datetime.now()
        try:
            db.session.add(self)  # @UndefinedVariable
            if cls.__batch__: return
            db.session.flush()  # @UndefinedVariable
            db.session.commit()  # @UndefinedVariable
            cls.__list__.append(cls.__store__(cls, self))
        except Exception as e:
            db.session.rollback()  # @UndefinedVariable
            cls.__list__ = []
            raise(e)
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def delete(cls, item):
        '''
        Deletes the item from the database.
        '''
        if not cls.__list__: cls.load()
        try:
            db.session.delete(cls.query.get(item.id))  # @UndefinedVariable
            if cls.__batch__: return
            db.session.commit()  # @UndefinedVariable
            cls.__list__.remove(item)
        except Exception as e:
            db.session.rollback()  # @UndefinedVariable
            cls.__list__ = []
            raise(e)
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def update(cls, item):
        '''
        Updates the item in the database.
        '''
        if not cls.__list__: cls.load()
        try:
            x = cls.query.get(item.id)
            for field in cls.__fields__: setattr(x, field, getattr(item, field))
            if cls.__batch__: return
            db.session.commit()  # @UndefinedVariable
        except Exception as e:
            db.session.rollback()  # @UndefinedVariable
            cls.__list__ = []
            raise(e)
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def get(cls, identifier):
        '''
        Fetches the item with the given id from the database and returns it.
        Returns None if no such item exists.
        '''
        if not identifier: return None
        if not cls.__list__: cls.load()
        items = cls.__list__
        lowerBound = 0
        upperBound = len(items) - 1
        while lowerBound <= upperBound:
            middle = ((upperBound - lowerBound) // 2) + lowerBound
            if items[middle].data[0] == identifier: return items[middle]
            elif items[middle].data[0] < identifier: lowerBound = middle + 1
            else: upperBound = middle - 1
        return None
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def all(cls):
        '''
        Returns all items in this table.
        '''
        if not cls.__list__: cls.load()
        return cls.__list__
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def find(cls, *criteria):
        '''
        Returns a list of all items that match the given criteria.
        '''
        if not cls.__list__: cls.load()
        functions = [parseExpression(c) for c in criteria]
        f = reduce(lambda x, y: x & y, functions)
        return [item for item in cls.__list__ if f(item)]
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def unique(cls, *criteria):
        '''
        Returns the item matching the given criteria if there is exactly one
        matching item. If none or more than one match None is returned.
        '''
        items = cls.find(*criteria)
        if items == None or len(items) != 1: return None
        return items[0]

# -------------------------------------------------------------------------------- #
def relation(native, foreign_id):
    '''
    Defines a relation between two natives (or a native and a model).
    Usage: foreign = relation(Native_Class, "foreign_id").
    '''
    f_get = lambda self: native.get(getattr(self, foreign_id))
    f_set = lambda self, value: setattr(self, foreign_id, __safegetid__(value))
    return property(f_get, f_set)

# -------------------------------------------------------------------------------- #
def recursion(recurse_id):
    '''
    Defines a recursive relation.
    Usage: parent = recursion("parent_id").
    '''
    f_get = lambda self: self.__class__.__model__.get(getattr(self, recurse_id))
    f_set = lambda self, value: setattr(self, recurse_id, __safegetid__(value))
    return property(f_get, f_set)

# -------------------------------------------------------------------------------- #
def __safegetid__(obj):
    if obj: return getattr(obj, "id")
    else: return 0