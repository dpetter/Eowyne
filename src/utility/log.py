# -*- coding: utf-8 -*-
#
# Log
#
# Simple log implementation. TODO: Expand this for true logging.
#
# Created by dp on 2014-12-06.
# ================================================================================ #
class Log():
    DEBUG               = 4
    INFORMATION         = 3
    EXPERIMENTAL        = 2
    WARNING             = 1
    ERROR               = 0
    __level__           = WARNING
    
    
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def level(value):
        Log.__level__ = value
    
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def debug(module, message):
        if Log.__level__ >= Log.DEBUG:
            print("Debug (%s): %s" % (module, message))
    
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def error(module, message):
        print("Error (%s): %s" % (module, message))
    
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def experimental(module, message):
        if Log.__level__ >= Log.EXPERIMENTAL:
            print("Experimental (%s): %s" % (module, message))
    
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def information(module, message):
        if Log.__level__ >= Log.INFORMATION:
            print("Information (%s): %s" % (module, message))
    
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def warning(module, message):
        if Log.__level__ >= Log.WARNING:
            print("Warning (%s): %s" % (module, message))
