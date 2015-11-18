import os
import logging
import traceback
import pmsconstants

from pmsdatamodel import Members
from google.appengine.api import mail
from flask import render_template

class EmailerUtility:
  def sendSignUpVerificationEmail(self, member):
    message = mail.EmailMessage()
    message.sender = "PayMySitter <hello@paymysitter.com>"
    message.to = member.emailaddress
    message.bcc = "hello@paymysitter.com"
    message.subject = "Your Pay My Sitter verification email"
    message.html = render_template('email_signupverificationemail.html', member=member, _SERVER_TO_USE=pmsconstants._SERVER_TO_USE)
    message.send()
