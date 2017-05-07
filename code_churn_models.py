""" Sample models. """

from google.appengine.ext import ndb

class Repo(ndb.Model):
  # Assume that repo name will be set in key
  pass

class Commit(ndb.Model):
  # Datastore will autogenerate id, although sha could be used
  # as key as well
  sha = ndb.StringProperty()
  committer = ndb.StringProperty()
  message = ndb.StringProperty()

class File(ndb.Model):
  file_name = ndb.StringProperty()
  url = ndb.StringProperty()
