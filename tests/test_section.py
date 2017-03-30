import unittest
import settings
import requests_mock

from canvas_api import Canvas
from canvas_api.enrollment import Enrollment
from canvas_api.section import Section
from tests.util import register_uris


@requests_mock.Mocker()
class TestSection(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'section': ['get_by_id']}, m)

            self.section = self.canvas.get_section(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.section)
        self.assertIsInstance(string, str)

    # list_enrollments()
    def test_get_enrollments(self, m):
        register_uris({'section': ['list_enrollments', 'list_enrollments_2']}, m)

        enrollments = self.section.get_enrollments()
        enrollment_list = [enrollment for enrollment in enrollments]

        self.assertEqual(len(enrollment_list), 4)
        self.assertIsInstance(enrollment_list[0], Enrollment)

    def test_cross_list_section(self, m):
        register_uris({'section': ['crosslist_section']}, m)

        section = self.section.cross_list_section(2)

        self.assertIsInstance(section, Section)

    def test_decross_list_section(self, m):
        register_uris({'section': ['decross_section']}, m)

        section = self.section.decross_list_section()

        self.assertIsInstance(section, Section)

    def test_edit(self, m):
        register_uris({'section': ['edit']}, m)

        edit = self.section.edit()

        self.assertIsInstance(edit, Section)

    def test_delete(self, m):
        register_uris({'section': ['delete']}, m)

        deleted_section = self.section.delete()

        self.assertIsInstance(deleted_section, Section)
