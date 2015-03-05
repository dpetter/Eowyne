# -*- coding: utf-8 -*-
#
# Installs blog database.
#
# Created on 2015-03-05.
# ================================================================================ #
from core.navigation.menu import Menubar, Menuitem
from core.security.rule import Rule
from plugins.blog.blog import Blog


# Plugin data
# -------------------------------------------------------------------------------- #
rules = [# role_id, pattern, insert, delete, update, view, search
Rule(3, "/blog/",              "Own",  "Own",  "Own",  "All"),
Rule(3, "/blog/[^/]+/comment", "None", "None", "None", "Foreign")
]

menubars = [# name
Menubar("blog")
]

menuitems = [# menubar, weight, name, image, flags, address
Menuitem(6, 2,  "Blog",             "",                 0,  "/blog"),
Menuitem(8, 0,  "",                 "plus",             0,  "/blog/create"),
Menuitem(8, 1,  "",                 "remove",           0,  "/blog/<id>/delete"),
Menuitem(8, 2,  "",                 "pencil",           0,  "/blog/<id>/update"),
Menuitem(8, 3,  "Leave a comment",  "comment",          0,  "/blog/<id>/comment")
]

# Install
# -------------------------------------------------------------------------------- #
def install():
    print("Installing rules ...")
    for item in rules: item.create()
    print("Installing menubars ...")
    for item in menubars: item.create()
    print("Installing menuitems ...")
    for item in menuitems: item.create()
    Blog.total()

