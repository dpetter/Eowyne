# -*- coding: utf-8 -*-
#
# Localisation
#
# Used to load localised text.
#
# Created on 2015-02-22.
# ================================================================================ #
from configparser import RawConfigParser
from utility.log import Log


# -------------------------------------------------------------------------------- #
def localize(mod, key):
    '''
    @returns            Localisation string.
    @param mod:         Name of the ini file holding the localisation string.
    @param key:         A string of the form "group.name" specifying the group
                        and key to use.
    '''
    global text_path
    try:
        p = RawConfigParser()
        p.read(text_path + mod + ".ini")
        [section, option] = key.split(".", 1)
        return p.get(section, option)
    except Exception as e:
        Log.error(__name__, str(e))
        return "No Localisation Entry"
