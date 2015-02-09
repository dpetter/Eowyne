# -*- coding: utf-8 -*-
#
# Models
#
# Every module in blueprints that implements ...
# blueprint = Blueprint("<pick a name>", __name__)
# ... is automatically imported and designated routes are assigned.
# For every route defined in the blueprint a rule must be created in the /rules
# administration so that users are allowed to visit that route.
#
# Every Blueprint can access the global scope (flask.globals.g) containing:
# - g.user -> the requesting client
# - g.role -> his (security) role
# - g.main_menu, g.personal_menu, g.extended_menu -> three navigation menus
#
# Created on 2015-02-09.
# ================================================================================ #
