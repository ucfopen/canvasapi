from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.file import File
from canvasapi.folder import Folder
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestFolder(unittest.TestCase):

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

    # delete()
    def test_delete_file(self, m):
        register_uris({'folder': ['delete_folder']}, m)

        deleted_folder = self.folder.delete()

        self.assertIsInstance(deleted_folder, Folder)
        self.assertTrue(hasattr(deleted_folder, 'name'))
        self.assertEqual(deleted_folder.full_name, "course_files/Folder 1")

    # list_folders()
    def test_list_folders(self, m):
        register_uris({'folder': ['list_folders']}, m)

        folders = self.folder.list_folders()
        folder_list = [folder for folder in folders]
        self.assertEqual(len(folder_list), 2)
        self.assertIsInstance(folder_list[0], Folder)

    # create_folder()
    def test_create_folder(self, m):
        register_uris({'folder': ['create_folder']}, m)

        name_str = "Test String"
        response = self.folder.create_folder(name=name_str)
        self.assertIsInstance(response, Folder)

    # update()
    def test_update(self, m):
        register_uris({'folder': ['update']}, m)

        new_name = 'New Name'
        response = self.folder.update(name=new_name)
        self.assertIsInstance(response, Folder)
        self.assertEqual(self.folder.name, new_name)
