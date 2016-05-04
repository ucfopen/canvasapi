import unittest
import settings
import requests_mock

from util import register_uris
from pycanvas.section import Section
from pycanvas.enrollment import Enrollment
from pycanvas.exceptions import ResourceDoesNotExist
from pycanvas import Canvas


class TestSection(unittest.TestCase):
    """
    Tests core Section functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'generic': ['not_found']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

    #list_enrollments()
    def test_list_enrollments(self):
        enrollments = self.section.list_enrollments()
        enrollment_list = [enrollment for enrollment in enrollments]

        assert len(enrollment_list) == 4
        assert isinstance(enrollment_list[0], enrollment)
