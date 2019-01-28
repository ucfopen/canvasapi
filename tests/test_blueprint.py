import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.blueprint import BlueprintMigration
from canvasapi.blueprint import ChangeRecord
from canvasapi.course import Course
from canvasapi.paginated_list import PaginatedList
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestBlueprint(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                'course': ['get_blueprint', 'get_by_id']
            }
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.blueprint = self.course.get_blueprint(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.blueprint)
        self.assertIsInstance(string, str)

    # get_associated_courses()
    def test_get_associated_courses(self, m):
        register_uris({'blueprint': ['get_associated_courses']}, m)
        associated_courses = self.blueprint.get_associated_courses()
        self.assertEqual(associated_courses[0].id, 1)
        self.assertIsInstance(associated_courses[0], Course)

    # update_associated_courses()
    def test_update_associated_courses(self, m):
        register_uris({'blueprint': ['update_associated_courses']}, m)
        updated_associations = self.blueprint.update_associated_courses()
        self.assertEqual(updated_associations, True)

    # associated_course_migration()
    def test_associated_course_migration(self, m):
        register_uris({'blueprint': ['associated_course_migration']}, m)
        associated_migration = self.blueprint.associated_course_migration()
        self.assertEqual(associated_migration.id, 1)
        self.assertEqual(associated_migration.comment, "test1")

    # change_blueprint_restrictions()
    def test_change_blueprint_restrictions(self, m):
        register_uris({'blueprint': ['change_blueprint_restrictions']}, m)
        blueprint_restriction = self.blueprint.change_blueprint_restrictions("quiz", 1, True)
        self.assertIsInstance(blueprint_restriction, bool)

    # get_unsynced_changes()
    def test_get_unsynced_changes(self, m):
        register_uris({'blueprint': ['get_unsynced_changes']}, m)
        unsynced_changes = self.blueprint.get_unsynced_changes()
        self.assertIsInstance(unsynced_changes, PaginatedList)
        self.assertIsInstance(unsynced_changes[0], ChangeRecord)
        self.assertEqual(unsynced_changes[0].asset_id, 1)
        self.assertEqual(unsynced_changes[0].asset_type, "quiz")
        self.assertEqual(unsynced_changes[0].asset_name, "test quiz")
        self.assertEqual(unsynced_changes[0].change_type, "updated")

    # list_blueprint_migrations()
    def test_list_blueprint_migrations(self, m):
        register_uris({'blueprint': ['list_blueprint_migrations']}, m)
        blueprint_migrations = self.blueprint.list_blueprint_migrations()
        self.assertIsInstance(blueprint_migrations, PaginatedList)
        self.assertIsInstance(blueprint_migrations[0], BlueprintMigration)
        self.assertEqual(blueprint_migrations[0].id, 1)
        self.assertEqual(blueprint_migrations[0].user_id, 1)
        self.assertEqual(blueprint_migrations[0].template_id, 1)

    # show_blueprint_migration()
    def test_show_blueprint_migration(self, m):
        register_uris({'blueprint': ['show_blueprint_migration']}, m)
        blueprint_migration = self.blueprint.show_blueprint_migration(1)
        self.assertIsInstance(blueprint_migration, BlueprintMigration)
        self.assertEqual(blueprint_migration.id, 1)
        self.assertEqual(blueprint_migration.user_id, 1)
        self.assertEqual(blueprint_migration.workflow_state, "completed")
        self.assertEqual(blueprint_migration.template_id, 1)

    def test_get_migration_details(self, m):
        register_uris({'blueprint': ['get_migration_details']}, m)
        migration_details = self.blueprint.get_migration_details()
        self.assertIsInstance(migration_details, PaginatedList)
        self.assertIsInstance(migration_details[0], ChangeRecord)
        self.assertEqual(migration_details[0].asset_id, 1)
        self.assertEqual(migration_details[0].asset_type, "assignment")
        self.assertEqual(migration_details[0].asset_name, "Test Assignment")
        self.assertEqual(migration_details[0].locked, True)
        self.assertEqual(migration_details[1].asset_id, 2)
        self.assertEqual(migration_details[1].asset_type, "quiz")
        self.assertEqual(migration_details[1].asset_name, "Test Quiz")
        self.assertEqual(migration_details[1].locked, False)
