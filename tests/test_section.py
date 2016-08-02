import unittest
import settings
import requests_mock

from util import register_uris
from pycanvas.enrollment import Enrollment
from pycanvas import Canvas
from pycanvas import Section


class TestSection(unittest.TestCase):
    """
    Tests core Section functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'generic': ['not_found'],
            'section': ['decross_section', 'get_by_id', 'list_enrollments', 'list_enrollments_2']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.section = self.canvas.get_section(1)

    # __str__()
    def test__str__(self):
        string = str(self.section)
        assert isinstance(string, str)

    # list_enrollments()
    def test_get_enrollments(self):
        enrollments = self.section.get_enrollments()
        enrollment_list = [enrollment for enrollment in enrollments]

        assert len(enrollment_list) == 4
        assert isinstance(enrollment_list[0], Enrollment)

    def test_decross_list_section(self):
        section = self.section.test_decross_list_section()

        assert isinstance(section, Section)
