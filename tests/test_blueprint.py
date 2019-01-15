import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.course import Course
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
        blueprint_restriction = self.blueprint.change_blueprint_restrictions()
        self.assertTrue(blueprint_restriction)
