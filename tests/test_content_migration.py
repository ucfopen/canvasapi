import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.account import Account
from canvasapi.content_migration import (
    ContentMigration,
    ContentMigrationSelectionNode,
    MigrationIssue,
)
from canvasapi.course import Course
from canvasapi.group import Group
from canvasapi.progress import Progress
from canvasapi.user import User
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestContentMigration(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "course": ["get_by_id", "get_content_migration_single"],
                "group": ["get_by_id", "get_content_migration_single"],
                "account": ["get_by_id", "get_content_migration_single"],
                "user": ["get_by_id", "get_content_migration_single"],
            }
            register_uris(requires, m)

            self.account = self.canvas.get_account(1)
            self.course = self.canvas.get_course(1)
            self.group = self.canvas.get_group(1)
            self.user = self.canvas.get_user(1)

            self.content_migration = self.account.get_content_migration(1)
            self.content_migration_course = self.course.get_content_migration(1)
            self.content_migration_group = self.group.get_content_migration(1)
            self.content_migration_user = self.user.get_content_migration(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.content_migration)
        self.assertIsInstance(string, str)

    # _parent_type
    def test_parent_type_account(self, m):
        self.assertEqual(self.content_migration._parent_type, "account")

    def test_parent_type_course(self, m):
        self.assertEqual(self.content_migration_course._parent_type, "course")

    def test_parent_type_group(self, m):
        self.assertEqual(self.content_migration_group._parent_type, "group")

    def test_parent_type_user(self, m):
        self.assertEqual(self.content_migration_user._parent_type, "user")

    def test_parent_type_no_type(self, m):
        migration = ContentMigration(self.canvas._Canvas__requester, {"id": 1})
        with self.assertRaises(ValueError):
            migration._parent_type

    # _parent_id
    def test_parent_id_account(self, m):
        self.assertEqual(self.content_migration._parent_id, 1)

    def test_parent_id_course(self, m):
        self.assertEqual(self.content_migration_course._parent_id, 1)

    def test_parent_id_group(self, m):
        self.assertEqual(self.content_migration_group._parent_id, 1)

    def test_parent_id_user(self, m):
        self.assertEqual(self.content_migration_user._parent_id, 1)

    def test_parent_id_no_id(self, m):
        migration = ContentMigration(self.canvas._Canvas__requester, {"id": 1})
        with self.assertRaises(ValueError):
            migration._parent_id

    # get_migration_issue()
    def test_get_migration_issue(self, m):
        register_uris({"content_migration": ["get_migration_issue_single"]}, m)

        issue = self.content_migration.get_migration_issue(1)
        self.assertIsInstance(issue, MigrationIssue)
        self.assertTrue(hasattr(issue, "id"))
        self.assertEqual(issue.id, 1)

    # get_migration_issues()
    def test_get_migration_issues(self, m):
        register_uris({"content_migration": ["get_migration_issue_multiple"]}, m)

        issues = self.content_migration.get_migration_issues()

        self.assertEqual(len(list(issues)), 2)

        self.assertIsInstance(issues[0], MigrationIssue)
        self.assertTrue(hasattr(issues[0], "id"))
        self.assertEqual(issues[0].id, 1)
        self.assertIsInstance(issues[1], MigrationIssue)
        self.assertTrue(hasattr(issues[1], "id"))
        self.assertEqual(issues[1].id, 2)

    # get_parent()
    def test_get_parent_account(self, m):
        register_uris({"content_migration": ["get_parent_account"]}, m)

        account = self.content_migration.get_parent()
        self.assertIsInstance(account, Account)
        self.assertTrue(hasattr(account, "id"))
        self.assertEqual(account.id, 1)

    def test_get_parent_course(self, m):
        register_uris({"content_migration": ["get_parent_course"]}, m)

        course = self.content_migration_course.get_parent()
        self.assertIsInstance(course, Course)
        self.assertTrue(hasattr(course, "id"))
        self.assertEqual(course.id, 1)

    def test_get_parent_group(self, m):
        register_uris({"content_migration": ["get_parent_group"]}, m)

        group = self.content_migration_group.get_parent()
        self.assertIsInstance(group, Group)
        self.assertTrue(hasattr(group, "id"))
        self.assertEqual(group.id, 1)

    def test_get_parent_user(self, m):
        register_uris({"content_migration": ["get_parent_user"]}, m)

        user = self.content_migration_user.get_parent()
        self.assertIsInstance(user, User)
        self.assertTrue(hasattr(user, "id"))
        self.assertEqual(user.id, 1)

    # get_progress()
    def test_get_progress(self, m):
        register_uris({"content_migration": ["get_progress"]}, m)

        progress = self.content_migration.get_progress()
        self.assertIsInstance(progress, Progress)
        self.assertTrue(hasattr(progress, "id"))
        self.assertEqual(progress.id, 1)

    # update()
    def test_update(self, m):
        register_uris({"content_migration": ["update"]}, m)

        worked = self.content_migration.update()
        self.assertTrue(worked)
        self.assertTrue(hasattr(self.content_migration, "migration_type"))
        self.assertEqual(self.content_migration.migration_type, "dummy_importer")

    def test_update_fail(self, m):
        register_uris({"content_migration": ["update_fail"]}, m)

        worked = self.content_migration.update()
        self.assertFalse(worked)


@requests_mock.Mocker()
class TestMigrationIssue(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "course": ["get_by_id", "get_content_migration_single"],
                "group": ["get_by_id", "get_content_migration_single"],
                "account": ["get_by_id", "get_content_migration_single"],
                "user": ["get_by_id", "get_content_migration_single"],
                "content_migration": [
                    "get_migration_issue_single",
                    "get_migration_issue_single_course",
                    "get_migration_issue_single_group",
                    "get_migration_issue_single_user",
                ],
            }
            register_uris(requires, m)

            self.account = self.canvas.get_account(1)
            self.course = self.canvas.get_course(1)
            self.group = self.canvas.get_group(1)
            self.user = self.canvas.get_user(1)

            self.content_migration = self.account.get_content_migration(1)
            self.content_migration_course = self.course.get_content_migration(1)
            self.content_migration_group = self.group.get_content_migration(1)
            self.content_migration_user = self.user.get_content_migration(1)

            self.migration_issue = self.content_migration.get_migration_issue(1)
            self.migration_issue_course = (
                self.content_migration_course.get_migration_issue(1)
            )
            self.migration_issue_group = (
                self.content_migration_group.get_migration_issue(1)
            )
            self.migration_issue_user = self.content_migration_user.get_migration_issue(
                1
            )

    # __str__()
    def test__str__(self, m):
        string = str(self.migration_issue)
        self.assertIsInstance(string, str)

    # update()
    def test_update(self, m):
        register_uris({"content_migration": ["update_issue"]}, m)

        worked = self.migration_issue.update()
        self.assertTrue(worked)
        self.assertTrue(hasattr(self.migration_issue, "id"))
        self.assertEqual(self.migration_issue.id, 1)

    def test_update_fail(self, m):
        register_uris({"content_migration": ["update_issue_fail"]}, m)

        worked = self.migration_issue.update()
        self.assertFalse(worked)


@requests_mock.Mocker()
class TestMigrator(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "course": ["get_by_id", "get_migration_systems_multiple"],
                "group": ["get_by_id", "get_migration_systems_multiple"],
                "account": ["get_by_id", "get_migration_systems_multiple"],
                "user": ["get_by_id", "get_migration_systems_multiple"],
                "content_migration": [
                    "get_migration_issue_single",
                    "get_migration_issue_single_course",
                    "get_migration_issue_single_group",
                    "get_migration_issue_single_user",
                ],
            }
            register_uris(requires, m)

            self.account = self.canvas.get_account(1)
            self.course = self.canvas.get_course(1)
            self.group = self.canvas.get_group(1)
            self.user = self.canvas.get_user(1)

            self.migrator = self.account.get_migration_systems()[0]
            self.migrator_course = self.course.get_migration_systems()[0]
            self.migrator_group = self.group.get_migration_systems()[0]
            self.migrator_user = self.user.get_migration_systems()[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.migrator)
        self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestSelectiveData(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "course": ["get_by_id"],
                "group": ["get_by_id"],
                "account": ["get_by_id"],
                "user": ["get_by_id"],
            }
            register_uris(requires, m)

            self.account = self.canvas.get_account(1)
            self.course = self.canvas.get_course(1)
            self.group = self.canvas.get_group(1)
            self.user = self.canvas.get_user(1)

    def test_get_selective_data(self, m):
        register_uris(
            {
                "course": ["get_content_migration_single"],
                "group": ["get_content_migration_single"],
                "account": ["get_content_migration_single"],
                "user": ["get_content_migration_single"],
                "content_migration": [
                    "get_selective_data_account",
                    "get_selective_data_course",
                    "get_selective_data_group",
                    "get_selective_data_user",
                ],
            },
            m,
        )
        for context_type in ["account", "course", "group", "user"]:
            context = getattr(self, context_type)
            migration = context.get_content_migration(1)
            for node in migration.get_selective_data():
                self.assertIsInstance(node, ContentMigrationSelectionNode)
                self.assertIsInstance(str(node), str)

            for node in migration.get_selective_data(type="assignments"):
                self.assertIsInstance(node, ContentMigrationSelectionNode)
                self.assertIsInstance(str(node), str)
