# -*- coding: utf-8 -*-
#
# Menu
#
# Used to build all kind of menu bars.
#
# Created by dp on 2015-01-05.
# ================================================================================ #
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from core.natives.rule import access
from natives import Native


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
    @returns            Returns all menu items in the menu bar identified by name.
                        Only links not dependent on an item (that is not
                        contained <id> in their address) are returned. Results are
                        sorted by weight.
    @param name         Identifies the menu bar.
    @param role_id      Identifies the client's role.
    '''
    items = Menu.find(Menu.menubar == name)
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
    items = Menu.find(Menu.menubar == name)
    result = [item for item in items if "<id>" in item.address and \
              access(item.address, role_id, elevated) == 1]
    return sorted(result, key = lambda item: item.weight)
