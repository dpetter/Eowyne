# -*- coding: utf-8 -*-
#
# Configuration
#
# All configuration options for interfacing external systems.
#
# Created on 2015-02-05.
# ================================================================================ #
from utility.log import Log


Configuration = {
    # Set this to Log.WARNING (fastest) or Log.INFORMATION in production.
    "log_level": Log.DEBUG,
    
    # Flask settings. Set host = 0.0.0.0 to route into the internet.
    # Put your static files (js, css, etc) into static_dir.
    # Put your templates into template.
    "flask_host": "0.0.0.0",
    "flask_port": 5000,
    "secret_key": "Extra Ordinary Wine",
    "static_dir": "../../static",
    "template_dir": "../../template", # It doesn't sync. D:
    
    # All your ajax calls should be prefixed with this path.
    "noscopeurl": "/api/",
    
    # Where your localisation files are.
    "text_files": "./static/txt/",
    
    # Tested with pymysql and mysql-connector.
    "sql_db_uri": "mysql+pymysql://theoden:king@localhost:3306/eowyne",
    
    # This is required for multithreaded/cluster usage. See doc on that.
    "native_msg": "./message/",
    "heartbeats": 4.0,
    
    # Remove this if you do not want a mail service.
    "email_host": "smtp.....de",
    "email_port": 587,
    "email_user": "...@....de",
    "email_pass": "password",
    
    # Currently only filesystem cache is supported.
    "cache_type": "filesystem",
    "cache_path": "./cache/"
}