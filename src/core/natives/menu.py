# -*- coding: utf-8 -*-
#
# Menu
#
# Used to build all kind of menu bars.
#
# Created by dp on 2015-01-05.
# ================================================================================ #
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from core.natives.rule import access
from natives import Native, relation


# -------------------------------------------------------------------------------- #
class Menubar(Native):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Menubars"
    
    id                  = Column(Integer, primary_key = True)
    name                = Column(String(255), unique = True)
    
    # ---------------------------------------------------------------------------- #
    def __init__(self, name = ""):
        self.name           = name


# -------------------------------------------------------------------------------- #
class Menuitem(Native):
    __mapper_args__     = {"concrete": True}
    __tablename__       = "Menuitems"
    
    id                  = Column(Integer, primary_key = True)
    menubar_id          = Column(Integer, ForeignKey("Menubars.id"))
    weight              = Column(Integer)
    name                = Column(String(255))
    image               = Column(String(255))
    flags               = Column(Integer)
    address             = Column(String(255))
    
    menubar             = relation(Menubar, "menubar_id")
    
    # ---------------------------------------------------------------------------- #
    def __init__(self, menubar_id = 0, weight = 0, name = "", image = "",
                 flags = 0, address = ""):
        self.address    = address
        self.name       = name
        self.menubar_id = menubar_id
        self.weight     = weight
        self.flags      = flags
        self.image      = image


# -------------------------------------------------------------------------------- #
def menubar(name, role_id):
    '''
    @returns            Returns all menu items in the menu bar identified by name.
                        Only links not dependent on an item (that is not
                        contained <id> in their address) are returned. Results are
                        sorted by weight.
    @param name         Identifies the menu bar.
    @param role_id      Identifies the client's role.
    '''
    bar = Menubar.unique(Menubar.name == name)
    if not bar: return None
    items = Menuitem.find(Menuitem.menubar_id == bar.id)
    result = [item for item in items if not "<id>" in item.address and \
              access(item.address, role_id, True) == 1]
    return sorted(result, key = lambda item: item.weight)

# -------------------------------------------------------------------------------- #
def contextmenu(name, role_id, elevated = False):
    '''
    @returns            Returns all menu items in the menu bar identified by name.
                        Only links dependent on an item (that is containing <id>
                        in their address) are returned. Results are sorted by
                        weight.
    @param name         Identifies the menu bar.
    @param role_id      Identifies the client's role.
    @param elevated     Whether the client has extended permissions.
    '''
    bar = Menubar.unique(Menubar.name == name)
    if not bar: return None
    items = Menuitem.find(Menuitem.menubar_id == bar.id)
    result = [item for item in items if "<id>" in item.address and \
              access(item.address, role_id, elevated) == 1]
    return sorted(result, key = lambda item: item.weight)
