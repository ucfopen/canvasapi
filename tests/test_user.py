import unittest
import settings
import requests_mock

from util import register_uris
from pycanvas.user import User
from pycanvas.enrollment import Enrollment
from pycanvas.exceptions import ResourceDoesNotExist
from pycanvas import Canvas


class TestUser(unittest.TestCase):
    """
    Tests core Account functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'user': ['list_enrollments', 'list_enrollments_2'],
            'generic': ['not_found']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

    def test_list_enrollments(self):
        enrollments = self.user.list_enrollments()
        enrollment_list = [enrollment for enrollment in enrollments]

        assert len(enrollment_list) == 4
        assert isinstance(enrollment_list[0], enrollment)
