from google.appengine.ext import ndb, blobstore

#::DATA MODELS::
class Members(ndb.Model):
  emailaddress = ndb.StringProperty()
  firstname = ndb.StringProperty()
  lastname = ndb.StringProperty()
  pictureblobstorekey = ndb.StringProperty()
  pictureservingurl = ndb.StringProperty()
  createddate = ndb.DateTimeProperty(auto_now_add=True)

