import unittest
import settings
import requests_mock

from util import register_uris
from pycanvas.enrollment import Enrollment
from pycanvas import Canvas


class TestSection(unittest.TestCase):
    """
    Tests core Section functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'generic': ['not_found'],
            'section': ['get_by_id', 'list_enrollments', 'list_enrollments_2']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.section = self.canvas.get_section(1)

    #list_enrollments()
    def test_list_enrollments(self):
        enrollments = self.section.list_enrollments()
        enrollment_list = [enrollment for enrollment in enrollments]

        assert len(enrollment_list) == 4
        assert isinstance(enrollment_list[0], Enrollment)
