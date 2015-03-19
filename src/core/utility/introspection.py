# -*- coding: utf-8 -*-
#
# Introspection
#
# Functionality for automatic loading of plug-ins.
#
# Created by dp on 2015-03-19.
# ================================================================================ #
import ast
import importlib
import inspect
import pkgutil
import re
import sys

from natives import Native


def import_blueprints(root):
    '''
    @returns            A list of modules containing the blueprint variable. All
                        the modules are also imported by this function.
    @param root         The root of the package tree to import.
    '''
    result = []
    [path, prefix] = [["./src/" + root], root + "."]
    for ml, name, ispkg in pkgutil.walk_packages(path, prefix):  # @UnusedVariable
        if ispkg: continue
        if not has_blueprint(name): continue
        result.append(importlib.import_module(name))
    return result

def has_blueprint(name):
    '''
    @returns            True if module contains the blueprint variable.
    @param name         Name of module.
    '''
    filename = "./src/" + re.sub("\.", "/", name) + ".py"
    file = open(filename)
    source = file.read()
    file.close()
    tree = ast.parse(source)
    for item in tree.body:
        if not isinstance(item, ast.Assign): continue
        for target in item.targets:
            if target.id == "blueprint": return True
    return False

def localize_natives(root):
    '''
    @returns            A list of all natives in the given package that have been
                        defined in one of the modules imported into the application.
    @param root         The root of the package tree to search in.
    '''
    result = []
    [path, prefix] = [["./src/" + root], root + "."]
    predicate = lambda member: is_native(member) and member.__module__ == name
    for ml, name, ispkg in pkgutil.walk_packages(path, prefix):  # @UnusedVariable
        if ispkg: continue
        if not name in sys.modules: continue
        result += inspect.getmembers(sys.modules[name], predicate)
    return [item[1] for item in result]

def is_native(item):
    '''
    @returns            True if item is a native.
    @param item         Anything, really. Really?
    '''
    return inspect.isclass(item) and issubclass(item, Native)
