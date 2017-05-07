from google.appengine.ext import ndb

class File(ndb.Model):
    file_name = ndb.StringProperty()
    url = ndb.StringProperty()

class Commit(ndb.Model):
    sha = ndb.StringProperty()
    committer = ndb.StringProperty()
    message = ndb.StringProperty()

    # We cannot nest Files into Commit the same way because
    # datastore does not support nested repeated properties.
    #files = ndb.StructuredProperty(File, repeated=True)

class Repo(ndb.Model):
    commits = ndb.StructuredProperty(
        Commit, repeated=True)
