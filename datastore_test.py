# [Local Unit Testing for
# Python](https://cloud.google.com/appengine/docs/standard/python/tools/localunittesting)
#
# [Guestbook](
# https://cloud.google.com/appengine/docs/standard/python/getting-started/creating-guestbook)
#
# [Creating and Using Entity Keys]
# (https://cloud.google.com/appengine/docs/standard/python/ndb/creating-entity-keys)
#
# python runner.py ~/google-cloud-sdk/
import unittest
from pprint import pprint as pp

from google.appengine.ext import ndb
from google.appengine.ext import testbed

import models


class DatastoreTestCase(unittest.TestCase):
  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    # Clear ndb's in-context cache between tests.
    ndb.get_context().clear_cache()

  def tearDown(self):
    self.testbed.deactivate()

  def testInsertEntity(self):
    models.TestModel().put()
    self.assertEqual(1, len(models.TestModel.query().fetch(2)))

  def testFilterByNumber(self):
    root = models.TestEntityGroupRoot(id="root")
    models.TestModel(parent=root.key).put()
    models.TestModel(number=17, parent=root.key).put()
    query = models.TestModel.query(ancestor=root.key).filter(
        models.TestModel.number == 42)
    results = query.fetch(2)
    self.assertEqual(1, len(results))
    self.assertEqual(42, results[0].number)

  def testGuestbook(self):
    models.Greeting(
      content='Hello world',
      parent=ndb.Key('Book', 'brane3')).put()

    models.Greeting(
      content='Flat sheet',
      parent=ndb.Key('Book', 'brane2')).put()

    ancestor_key = ndb.Key('Book', 'brane3')
    greetings = models.Greeting.query_book(ancestor_key).fetch(20)
    self.assertEqual(1, len(greetings))

    #import pdb; pdb.set_trace()
    #pp(greetings)

  def testAccount(self):
    account_key = ndb.Key(models.Account, 'sandy@example.com')

    # Ask Datastore to allocate an ID.
    new_id = ndb.Model.allocate_ids(size=1, parent=account_key)[0]

    #import pdb; pdb.set_trace()

    # Datastore returns us an integer ID that we can use to create the message
    # key
    message_key = ndb.Key('Message', new_id, parent=account_key)

    # Now we can put the message into Datastore
    initial_revision = models.Revision(
       message_text='Hello', id='1', parent=message_key)
    initial_revision.put()


if __name__ == '__main__':
  unittest.main()
