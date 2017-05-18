import os
import unittest
import uuid

import requests_mock

from canvasapi import Canvas
from canvasapi.file import File
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestFile(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'course': ['get_by_id', 'list_course_files',
                'list_course_files2']}, m)

            self.course = self.canvas.get_course(1)
            self.file = self.course.list_files()[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.file)
        self.assertIsInstance(string, str)

    # delete()
    def test_delete_file(self, m):
        register_uris({'file': ['delete_file']}, m)

        deleted_file = self.file.delete()

        self.assertIsInstance(deleted_file, File)
        self.assertTrue(hasattr(deleted_file, 'display_name'))
        self.assertEqual(deleted_file.display_name, "Bad File.docx")
