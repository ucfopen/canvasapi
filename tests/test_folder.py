import os
import unittest
import uuid

import requests_mock

from canvasapi import Canvas
from canvasapi.file import File
from canvasapi.folder import Folder
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestFolder(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'folder': ['get_by_id']}, m)

            self.folder = self.canvas.get_folder(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.folder)
        self.assertIsInstance(string, str)

    # list_files()
    def test_folder_files(self, m):
        register_uris({'folder': ['list_folder_files', 'list_folder_files2']}, m)

        files = self.folder.list_files()
        file_list = [file for file in files]
        self.assertEqual(len(file_list), 4)
        self.assertIsInstance(file_list[0], File)
