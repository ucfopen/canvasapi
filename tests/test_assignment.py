import unittest
import requests_mock
import settings

from pycanvas import Canvas
from pycanvas.assignment import Assignment
from util import register_uris


class TestAssignment(unittest.TestCase):
    """
    Tests Assignment functionality.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'assignment': ['edit_assignment', 'delete_assignment'],
            'course': ['get_by_id', 'get_assignment_by_id'],
            'user': ['get_by_id']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)

    # edit()
    def test_edit_assignment(self):
        name = 'New Name'
        assignment = self.course.get_assignment(5)
        edited_assignment = assignment.edit(assignment={'name': name})

        assert isinstance(edited_assignment, Assignment)
        assert hasattr(edited_assignment, 'name')
        assert edited_assignment.name == name

    # delete()
    def test_delete_assignments(self):

        assignment = self.course.get_assignment('5')

        deleted_assignment = assignment.delete()

        assert isinstance(deleted_assignment, Assignment)

    # __str__()
    def test__str__(self):
        string = str(self.course.get_assignment('5'))
        assert isinstance(string, str)
