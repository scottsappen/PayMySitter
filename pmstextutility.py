import os
import logging
import traceback
import pmsconstants

from google.appengine.api import mail
from flask import render_template


#Mobile provider email SMS gateways
_MOBILE_PROVIDERS_DICT = {'ATT': 'txt.att.net', 'Alltel': 'message.alltel.com', 'Boost Mobile': 'myboostmobile.com', 'Cricket': 'sms.mycricket.com', 'Metro PCS': 'mymetropcs.com', 'Nextel': 'messaging.nextel.com', 'Ptel': 'ptel.com', 'Qwest': 'qwestmp.com', 'Sprint': 'messaging.sprintpcs.com', 'Suncom': 'tms.suncom.com', 'Tracfone': 'mmst5.tracfone.com', 'T-Mobile': 'tmomail.net', 'Verizon': 'vtext.com', 'Virgin Mobile': 'vmobl.com', 'U.S. Cellular': 'email.uscc.net'};


class TextUtility:
  def sendTextMessage(self, mobilenumber, mobileprovider, mobilemessage):
    if mobilenumber and mobileprovider:
      if mobileprovider in _MOBILE_PROVIDERS_DICT:
        message = mail.EmailMessage()
        message.sender = "PayMySitter <hello@paymysitter.com>"
        message.to = str(mobilenumber.replace("-", "") + "@" + _MOBILE_PROVIDERS_DICT.get(mobileprovider))
        message.subject = "PayMySitter! "
        message.html = str(mobilemessage)
        logging.info("TextUtility message.to = " + message.to + " and message.subject = " + message.subject)
        message.send()
