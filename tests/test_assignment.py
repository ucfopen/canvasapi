import unittest
from datetime import datetime

import requests_mock

from pycanvas import Canvas
from pycanvas.assignment import Assignment
from pycanvas.course import Course
from pycanvas.exceptions import ResourceDoesNotExist
from pycanvas.user import User
import settings
from util import register_uris

INVALID_ID = 9001


class TestCanvas(unittest.TestCase):
    """
    Tests core Canvas functionality.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'assignment': ['create', 'get_by_id', 'get_all_assignments',
                           'get_user_assignments', 'delete_assignment', 'edit_assignment'],
            'course': ['get_by_id'],
            'user': ['get_by_id']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

    def test_create_assignment(self):
        course = self.canvas.get_course(1)

        name = 'Newly Created Assignment'

        assignment_dict = {
            'name': name
        }

        assignment = course.create_assignment(assignment=assignment_dict)

        assert isinstance(assignment, Assignment)
        assert hasattr(assignment, 'name')
        assert assignment.name == name
        assert assignment.id == 5

    def test_get_assignment(self):
        course = self.canvas.get_course(1)

        assignment = course.get_assignment('5')

        assert isinstance(assignment, Assignment)
        assert hasattr(assignment, 'name')

    def test_get_assignments(self):
        course = self.canvas.get_course(1)

        assignments = course.get_assignments()
        assignment_list = [assignment for assignment in assignments]

        assert isinstance(assignments[0], Assignment)
        assert len(assignment_list) == 2

    def test_user_assignments(self):
        user = self.canvas.get_user(1)

        assignments = user.get_assignments(1)
        assignment_list = [assignment for assignment in assignments]

        assert isinstance(assignments[0], Assignment)
        assert len(assignment_list) == 2

    def test_edit_assignment(self):
        course = self.canvas.get_course(1)

        name = 'New Name'
        assignment = course.get_assignment(5)
        edited_assignment = assignment.edit(assignment={'name': name})

        assert isinstance(edited_assignment, Assignment)
        assert hasattr(edited_assignment, 'name')
        assert edited_assignment.name == name

    def test_delete_assignments(self):
        course = self.canvas.get_course(1)

        assignment = course.get_assignment('5')

        deleted_assignment = assignment.delete()

        assert isinstance(deleted_assignment, Assignment)
