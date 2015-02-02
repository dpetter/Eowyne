# -*- coding: utf-8 -*-
#
# Globals
#
# Objects usable throughout the application.
#
# Created by dp on 2015-02-02.
# ================================================================================ #
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy

from utility.mail import MailService


db                      = SQLAlchemy()
cache                   = Cache()
mailservice             = MailService()