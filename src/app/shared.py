# -*- coding: utf-8 -*-
#
# Shared
#
# Objects usable throughout the application.
#
# Created on 2015-02-02.
# ================================================================================ #
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy

from utility.mail import MailService


db                      = SQLAlchemy()
cache                   = Cache()
mailservice             = MailService()
timer                   = 0.0