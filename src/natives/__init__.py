from _functools import reduce
from datetime import datetime
import os

from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.annotation import AnnotatedColumn  # @UnresolvedImport
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList, Grouping
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer

from core.shared import db
from utility.log import Log


class Native(db.Model):
    __tablename__       = "Native"
    __batch__           = False     # Do not touch this
    __list__            = []        # Do not touch this
    __fields__          = None      # Do not touch this
    __store__           = None      # Do not touch this
    __timestamp__       = None      # Do not touch this
    __message__         = None
    
    id                  = Column(Integer, primary_key = True)
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def heartbeat(cls):
        if not cls.__message__: return
        filename = cls.__message__ + cls.__name__
        if os.path.exists(filename):
            timestamp = os.path.getmtime(filename)
            if timestamp == cls.__timestamp__: return
            cls.__timestamp__ = timestamp
            cls.__list__ = []
        else:
            f = open(filename, mode='w')
            f.close()
            timestamp = os.path.getatime(filename)
            cls.__timestamp__ = timestamp
    
    # ---------------------------------------------------------------------------- #
    @classmethod
    def stamp(cls):
        if not cls.__message__: return
        filename = cls.__message__ + cls.__name__
        f = open(filename, mode='w')
        f.close()
        timestamp = os.path.getmtime(filename)
        cls.__timestamp__ = timestamp
    
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
        items = cls.query.order_by(cls.id).all()
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
            cls.stamp()
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
            cls.stamp()
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
            cls.stamp()
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


# -------------------------------------------------------------------------------- #
class Storage(object):
    # ---------------------------------------------------------------------------- #
    def __init__(self, model, item):
        self.data = tuple([getattr(item, field) for field in model.__fields__])
        for i, field in enumerate(model.__fields__):
            setattr(self, field, self.data[i])
    
    # ---------------------------------------------------------------------------- #
    def delete(self):
        self.__class__.__model__.delete(self)
    
    # ---------------------------------------------------------------------------- #
    def update(self):
        self.__class__.__model__.update(self)

# -------------------------------------------------------------------------------- #
def fields(cls):
    fields = (key for key, value in vars(cls).items() if \
              key != "id" and value.__class__ == InstrumentedAttribute)
    return ("id",) + tuple(fields)

# -------------------------------------------------------------------------------- #
def storage(cls):
    container = type(cls.__name__ + "_storage", (Storage, ), {"__model__": cls})
    for key, value in vars(cls).items():
        if (value.__class__ == property): setattr(container, key, value)
    return container

# -------------------------------------------------------------------------------- #
def store(model, items):
    return [model.__store__(model, item) for item in items]

# -------------------------------------------------------------------------------- #
def parseExpression(expression):
    '''
    Internal only. Use match(item, *criteria) instead.
    '''
    # Returns a function f(item).
    # f(item) = True exactly if the statement applies to item.
    ec = expression.__class__
    if ec == BinaryExpression:
        return compare(expression.left, expression.operator, expression.right)
    elif ec == BooleanClauseList:
        left = parseExpression(expression.clauses[0])
        right = parseExpression(expression.clauses[1])
        return lambda item: expression.operator(left(item), right(item))
    elif ec == Grouping:
        return parseExpression(expression.element)
    else:
        raise ValueError("This is not a valid search term.")

# -------------------------------------------------------------------------------- #
def compare(left, operator, right):
    '''
    Internal only. Use match(item, *criteria) instead.
    '''
    # Returns a function f(item).
    # f(item) = True exactly if the statement <left> <operator> <right> applies to
    # item.
    # <left>, <right> = either an attribute of item or a constant value.
    # <operator> = one of ==, !=, <, >, <=, >= (or more? i don't know)
    #
    # Written this way since it scales better than
    # return lambda x: operator(getValue(left), getValue(right)).
    try:
        lc = left.__class__
        rc = right.__class__
        if lc == AnnotatedColumn and rc == AnnotatedColumn:
            li = get_index(left)
            ri = get_index(right)
            return lambda item: operator(item.data[li], item.data[ri])
        elif lc == AnnotatedColumn:
            li = get_index(left)
            return lambda item: operator(item.data[li], right.value)
        elif rc == AnnotatedColumn:
            ri = get_index(right)
            return lambda item: operator(left.value, item.data[ri])
        else:
            return lambda x: operator(left.value, right.value)
    except:
        raise ValueError("This is not a valid search term.")

# -------------------------------------------------------------------------------- #
def get_index(entity):
    '''
    Internal only. Use match(item, *criteria) instead.
    '''
    fields = entity._annotations["parententity"].class_.__fields__
    return fields.index(entity.key, )
