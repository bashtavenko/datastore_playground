""" Sample models based on KeyProperties.
    High write throughput but only eventual consistency

    Entities don't form entity groups;
    Commit(sha='7c087b5', repo=my_repo_key)
"""

from google.appengine.ext import ndb

class Repo(ndb.Model):
  # Assume that repo name will be set in key
  pass

class Commit(ndb.Model):
  # Datastore will autogenerate id, although sha could be used
  # as key as well
  repo = ndb.KeyProperty(kind=Repo)
  sha = ndb.StringProperty()
  committer = ndb.StringProperty()
  message = ndb.StringProperty()

class File(ndb.Model):
  commit = ndb.KeyProperty(kind=Commit)
  file_name = ndb.StringProperty()
  url = ndb.StringProperty()
