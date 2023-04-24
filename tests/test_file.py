import unittest
from os.path import isfile

import requests_mock

from canvasapi import Canvas
from canvasapi.file import File
from tests import settings
from tests.util import cleanup_file, register_uris


@requests_mock.Mocker()
class TestFile(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {"course": ["get_by_id", "list_course_files", "list_course_files2"]}, m
            )

            self.course = self.canvas.get_course(1)
            self.file = self.course.get_files()[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.file)
        self.assertIsInstance(string, str)

    # delete()
    def test_delete_file(self, m):
        register_uris({"file": ["delete_file"]}, m)

        deleted_file = self.file.delete()

        self.assertIsInstance(deleted_file, File)
        self.assertTrue(hasattr(deleted_file, "display_name"))
        self.assertEqual(deleted_file.display_name, "Bad File.docx")

    # download()
    def test_download_file(self, m):
        register_uris({"file": ["file_download"]}, m)
        try:
            self.file.download("canvasapi_file_download_test.txt")
            self.assertTrue(isfile("canvasapi_file_download_test.txt"))
            with open("canvasapi_file_download_test.txt") as downloaded_file:
                self.assertEqual(downloaded_file.read(), '"file contents are here"')
        finally:
            cleanup_file("canvasapi_file_download_test.txt")

    # contents()
    def test_contents_file(self, m):
        register_uris({"file": ["file_contents"]}, m)
        contents = self.file.get_contents()
        self.assertEqual(contents, '"Hello there"')
        contents_binary = self.file.get_contents(binary=True)
        self.assertEqual(contents_binary, b'"Hello there"')

    # update()
    def test_update_file(self, m):
        register_uris({"file": ["update_file"]}, m)

        updated_file = self.file.update(name="New filename.docx")

        self.assertIsInstance(updated_file, File)
        self.assertTrue(hasattr(updated_file, "display_name"))
        self.assertEqual(updated_file.display_name, "New filename.docx")
