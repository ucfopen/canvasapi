import unittest
import settings
import requests_mock

from util import register_uris
from pycanvas.assignment import Assignment
from pycanvas.course import Course
from pycanvas.quiz import Quiz
from pycanvas.exceptions import ResourceDoesNotExist
from pycanvas import Canvas

INVALID_ID = 9001


class TestUser(unittest.TestCase):
    """
    Tests core Canvas functionality.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'user': ['get_by_id', 'get_user_assignments']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

    #get_assignments()
    def test_user_assignments(self):
        user = self.canvas.get_user(1)

        assignments = user.get_assignments(1)
        assignment_list = [assignment for assignment in assignments]

        assert isinstance(assignments[0], Assignment)
        assert len(assignment_list) == 2
