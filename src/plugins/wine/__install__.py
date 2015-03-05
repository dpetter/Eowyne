# -*- coding: utf-8 -*-
#
# Installs wine database.
#
# Created on 2015-03-05.
# ================================================================================ #
from core.navigation.menu import Menubar, Menuitem
from core.security.rule import Rule
from plugins.wine.models import *


# Plugin data
# -------------------------------------------------------------------------------- #
rules = [# role_id, pattern, insert, delete, update, view, search
Rule(1, "/wein/",              "None", "None", "None", "All"),
Rule(1, "/wein/suche/[^/]+",   "None", "None", "None", "All")
]

menubars = [# name
Menubar("wein")
]

menuitems = [# menubar, weight, name, image, flags, address
Menuitem(6, 3,  "Top Wines",        "",                 0,  "/wein/tops"),
]

# -------------------------------------------------------------------------------- #
def installGattung():
    if Gattung.get(1): return
    print("Installing Gattungen...")
    items = [
             Gattung("Rotwein"),
             Gattung("Weisswein"),
             Gattung("Roséwein"),
             Gattung("Champagner"),
             Gattung("Sekt"),
            ]
    for item in items: item.create()

# -------------------------------------------------------------------------------- #
def installLand():
    if Land.get(1): return
    print("Installing Laender...")
    item = Land("Frankreich")
    item.create()

# -------------------------------------------------------------------------------- #
def installRebsorte():
    if Rebsorte.get(1): return
    print("Installing Rebsorten...")
    item = Rebsorte("Merlot")
    item.create()

# -------------------------------------------------------------------------------- #
def installRegion():
    if Region.get(1): return
    print("Installing Regionen...")
    item = Region("Languedoc Roussillon")
    item.create()

# -------------------------------------------------------------------------------- #
def installWeingut():
    if Weingut.get(1): return
    print("Installing Weingueter...")
    item = Weingut("Domaine de La Grange")
    item.create()

# -------------------------------------------------------------------------------- #
def installWein():
    if Wein.get(1): return
    print("Installing Wein...")
    item = Wein("La Grange Terroir Merlot Pabrio",
                Gattung.get(1),
                Rebsorte.get(1),
                Land.get(1),
                Region.get(1),
                Weingut.get(1),
                2013)
    item.create()

# -------------------------------------------------------------------------------- #
def install():
    print("Installing rules ...")
    for item in rules: item.create()
    print("Installing menubars ...")
    for item in menubars: item.create()
    print("Installing menuitems ...")
    for item in menuitems: item.create()
    installGattung()
    installLand()
    installRebsorte()
    installRegion()
    installWeingut()
    installWein()