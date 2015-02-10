# -*- coding: utf-8 -*-
#
# Configuration
#
# All configuration options for interfacing external systems.
#
# Created on 2015-02-05.
# ================================================================================ #


Configuration = {
    "secret_key": "Extra Ordinary Wine",
    "sql_db_uri": "mysql+pymysql://theoden:king@localhost:3306/eowyne",
    "flask_host": "0.0.0.0",
    "flask_port": 5000,
    "cache_type": "filesystem",
    "cache_path": "./cache",
    "email_host": "smtp.web.de",
    "email_port": 587,
    "email_user": "...@web.de",
    "email_pass": "password",
    "text_files": "./static/txt/"
}