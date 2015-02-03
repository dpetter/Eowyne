from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from natives import Native
from natives.rule import access


# -------------------------------------------------------------------------------- #
class Menu(Native):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Menus"
    
    id                  = Column(Integer, primary_key = True)
    address             = Column(String(255))
    name                = Column(String(255))
    menubar             = Column(String(255))
    weight              = Column(Integer)
    flags               = Column(Integer)
    image               = Column(String(255))
    
    # ---------------------------------------------------------------------------- #
    def __init__(self, address = None, name = None, menubar = None, weight = None,
                 flags = None, image = None):
        self.address        = address
        self.name           = name
        self.menubar        = menubar
        self.weight         = weight
        self.flags          = flags
        self.image          = image


# -------------------------------------------------------------------------------- #
def menubar(name, role_id):
    '''
    Returns the menu bar with the given name. Only items the role with the given id
    can access are returned.
    '''
    items = Menu.find(Menu.menubar == name)
    result = [item for item in items if not "<id>" in item.address and \
              access(item.address, role_id, True) == 1]
    return sorted(result, key = lambda item: item.weight)

# -------------------------------------------------------------------------------- #
def contextmenu(name, role_id, owned = False):
    '''
    Returns the context menu for the given item.
    '''
    items = Menu.find(Menu.menubar == name)
    result = [item for item in items if "<id>" in item.address and \
              access(item.address, role_id, owned) == 1]
    return sorted(result, key = lambda item: item.weight)