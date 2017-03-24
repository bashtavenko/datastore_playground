from google.appengine.ext import ndb

class TestEntityGroupRoot(ndb.Model):
    """Entity group root"""
    pass

class TestModel(ndb.Model):
    """A model class used for testing."""
    number = ndb.IntegerProperty(default=42)
    text = ndb.StringProperty()

class TestEntityGroupRoot(ndb.Model):
    """Entity group root"""
    pass

class Greeting(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_book(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)

class Account(ndb.Model):
    username = ndb.StringProperty()
    userid = ndb.IntegerProperty()
    email = ndb.StringProperty()

class Revision(ndb.Model):
    message_text = ndb.StringProperty()

