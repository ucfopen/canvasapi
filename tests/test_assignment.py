import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.assignment import Assignment, AssignmentGroup
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestAssignment(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'course': ['get_by_id', 'get_assignment_by_id']}, m)

            self.course = self.canvas.get_course(1)
            self.assignment = self.course.get_assignment(5)

    # edit()
    def test_edit_assignment(self, m):
        register_uris({'assignment': ['edit_assignment']}, m)

        name = 'New Name'
        edited_assignment = self.assignment.edit(assignment={'name': name})

        self.assertIsInstance(edited_assignment, Assignment)
        self.assertTrue(hasattr(edited_assignment, 'name'))
        self.assertEqual(edited_assignment.name, name)

    # delete()
    def test_delete_assignments(self, m):
        register_uris({'assignment': ['delete_assignment']}, m)

        deleted_assignment = self.assignment.delete()

        self.assertIsInstance(deleted_assignment, Assignment)

    # __str__()
    def test__str__(self, m):
        string = str(self.assignment)
        self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestAssignmentGroup(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({
                'course': ['get_by_id'],
                'assignment': ['get_assignment_group']
            }, m)

            self.course = self.canvas.get_course(1)
            self.assignment_group = self.course.get_assignment_group(5)

    # edit()
    def test_edit_assignment_group(self, m):
        register_uris({'assignment': ['edit_assignment_group']}, m)

        name = 'New Name'
        edited_assignment_group = self.assignment_group.edit(
            assignment_group={'name': name}
        )

        self.assertIsInstance(edited_assignment_group, AssignmentGroup)
        self.assertTrue(hasattr(edited_assignment_group, 'name'))
        self.assertEqual(edited_assignment_group.name, name)

    # delete()
    def test_delete_assignment_group(self, m):
        register_uris({'assignment': ['delete_assignment_group']}, m)

        deleted_assignment_group = self.assignment_group.delete()

        self.assertIsInstance(deleted_assignment_group, AssignmentGroup)
        self.assertTrue(hasattr(deleted_assignment_group, 'name'))
        self.assertEqual(deleted_assignment_group.name, 'Assignment Group 5')

    # __str__()
    def test__str__(self, m):
        string = str(self.assignment_group)
        self.assertIsInstance(string, str)
