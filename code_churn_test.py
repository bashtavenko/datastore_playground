''' Test for code chur model.
    python runner.py ~/google-cloud-sdk/
'''
import unittest
from pprint import pprint as pp

from google.appengine.ext import ndb
from google.appengine.ext import testbed

import code_churn_models as models
import code_churn_models_v2 as models_v2
import code_churn_models_v3 as models_v3


class CodeChurnTestCase(unittest.TestCase):
  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    # Clear ndb's in-context cache between tests.
    ndb.get_context().clear_cache()

  def tearDown(self):
    self.testbed.deactivate()

  def testInsertRepo(self):
    models.Repo(id='my_repo').put()

    # Get with query()
    repos = models.Repo.query().fetch()
    self.assertEqual(1, len(repos))
    my_repo = repos[0]
    self.assertEqual('my_repo', my_repo.key.id())

    # Get with get_by_id
    another_my_repo = models.Repo.get_by_id('my_repo')
    self.assertEqual('my_repo', another_my_repo.key.id())

  def testInsertRepoAndCommits(self):
    # Insert repo with a couple of commits
    my_repo = models.Repo(id='my_repo')
    my_repo.put()
    models.Commit(
            sha='7c087b5',
            committer='Washington Irving',
            message='Initial commit',
            parent=my_repo.key
          ).put()
    models.Commit(
            sha='77c087b5',
            committer='Joe Doe',
            message='Added readme',
            parent=my_repo.key
          ).put()

    # Find all commits for this repo
    ancestor_key = ndb.Key('Repo', 'my_repo')
    commits = models.Commit.query(ancestor=ancestor_key).fetch()
    self.assertEqual(2, len(commits))

    # Find commit with a given sha and its parent (repo)
    commits = models.Commit.query().filter(
      models.Commit.sha == '77c087b5').fetch()
    self.assertEqual(1, len(commits))
    self.assertEqual('my_repo', commits[0].key.parent().id())

  def testRidiculousExample(self):
    # Insert commit with a couple of repos
    my_commit = models.Commit(sha='7c087b5')
    my_commit.put()

    models.Repo(id='my_repo', parent=my_commit.key).put()
    models.Repo(id='my_repo_2', parent=my_commit.key).put()
    ancestor_key = models.Commit.query().fetch()[0].key
    repos = models.Repo.query(ancestor=ancestor_key).fetch()
    self.assertEqual(2, len(repos))

  def testInsertRepoAndCommitsV2(self):
    # Insert repo with a couple of commits as StructuredProperty
    my_repo = models_v2.Repo(
        id='my_repo',
        commits=[
          models_v2.Commit(
                  sha='7c087b5',
                  committer='Washington Irving',
                  message='Initial commit',
              ),
          models_v2.Commit(
                  sha='77c087b5',
                  committer='Joe Doe',
                  message='Added readme',
          )])
    my_repo.put()

    # Find all commits for this repo
    repo = models_v2.Repo.get_by_id('my_repo')
    self.assertIsNotNone(repo)
    commits = repo.commits
    self.assertEqual(2, len(commits))

    # Find commit with a given sha for this repo
    commit = next((c for c in commits if c.sha == '77c087b5'), None)
    self.assertIsNotNone(commit)

  def testInsertRepoAndCommitsKeyProperty(self):
    # Insert repo with a couple of commits
    my_repo = models_v3.Repo(id='my_repo')
    my_repo.put()
    models_v3.Commit(
            sha='7c087b5',
            committer='Washington Irving',
            message='Initial commit',
            repo=my_repo.key
          ).put()
    models_v3.Commit(
            sha='77c087b5',
            committer='Joe Doe',
            message='Added readme',
            repo=my_repo.key
          ).put()

    # Find all commits for this repo
    repo_key = ndb.Key('Repo', 'my_repo')
    commits = models_v3.Commit.query(models_v3.Commit.repo == repo_key).fetch()
    self.assertEqual(2, len(commits))
