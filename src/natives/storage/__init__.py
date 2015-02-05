from sqlalchemy.orm.attributes import InstrumentedAttribute


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
