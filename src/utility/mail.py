# -*- coding: utf-8 -*-
#
# Mail
#
# Access to mail server.
#
# Created by dp on 2015-02-02.
# ================================================================================ #
import smtplib

from utility.log import Log


class MailService():
    # ---------------------------------------------------------------------------- #
    def __init__(self, host = None, port = None, username = None, password = None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        if username: self.tls = True
        else: self.tls = False
    
    # ---------------------------------------------------------------------------- #
    def init_app(self, host, port, username = None, password = None):
        self.host = host
        self.port = port
        if username:
            self.username = username
            self.password = password
            self.tls = True
        else: self.tls = False
    
    # ---------------------------------------------------------------------------- #
    def send(self, recipients, subject, message):
        '''
        Sends an html email with the given message and subject to a list of
        recipients.
        '''
        sender = self.username
        header = "From: <%s>\n" % (sender)
        header += "To: <%s>\n" % (", ".join(x for x in recipients))
        header += "MIME-Version: 1.0\nContent-type: text/html\n"
        header += "Subject: %s\n\n" % (subject)
        try:
            smtp = smtplib.SMTP(self.host, self.port)
            if self.tls:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.sendmail(sender, recipients, header + message)
            return True
        except Exception as e:
            Log.error(self.__class__, "Could not send mail." + str(e))
            return False