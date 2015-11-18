import os
import logging
import traceback
import datetime
import cgi
import MySQLdb
import urllib
import time
import pmsconstants

from pmsdatamodel import Members
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb, blobstore
from datetime import date, datetime, timedelta

class MemberInfo:
  def getFromNoSQLExample(self, emailaddress):
    member = None
    member = Members.gql("WHERE emailaddress = :1", emailaddress.lower()).get()
    return member

  def getFromCloudSQLExample(self, memberguid):
    userlist = [];
    try:
      if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
        db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, user='root', db=_DATABASE_NAME, charset='utf8', use_unicode=True)
      else:
        db = MySQLdb.connect(host='localhost', user='root', passwd='password', db=_DATABASE_NAME, charset='utf8', use_unicode=True)
      cursor = db.cursor()
      cursor.execute('SELECT distinct(...), status, createddate FROM circles ' +
                     'WHERE (... = %s and blocked = %s) ', (memberguid, 0, memberguid, 1))
      for row in cursor.fetchall():
        userlist.append(dict([('...',cgi.escape(row[0])),
                              ('status',str(row[1])),
                              ('createddate',datetime.strptime(cgi.escape(str(row[2])),"%Y-%m-%d %H:%M:%S").strftime("%m/%d/%Y"))
                              ]))
      db.close()

    except:
      logging.error(':: ' + 'Uh oh, an error occurred' + ' | <error...> | ' + ' ::')
      logging.error(traceback.format_exc())
    
    return userlist
