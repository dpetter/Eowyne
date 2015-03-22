# -*- coding: utf-8 -*-
#
# Shared
#
# Objects usable throughout the application.
#
# Created on 2015-02-02.
# ================================================================================ #
import logging

from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy

from core.utility.mail import MailService


db                      = SQLAlchemy()
cache                   = Cache()
mailservice             = MailService()
beating_hearts          = []
heartbeat_count         = 0
heartbeat_time          = 0.0
log                     = logging.getLogger("eowyne-logger")
request_count           = 0
time_elapsed            = 0.0
time_start              = 0.0
noscope_url             = "/api/"
