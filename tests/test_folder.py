from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import uuid

import requests_mock
import warnings

from canvasapi import Canvas
from canvasapi.file import File
from canvasapi.folder import Folder
from tests import settings
from tests.util import register_uris, cleanup_file


@requests_mock.Mocker()
class TestFolder(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"folder": ["get_by_id"]}, m)

            self.folder = self.canvas.get_folder(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.folder)
        self.assertIsInstance(string, str)

    # list_files()
    def test_list_files(self, m):
        register_uris({"folder": ["list_folder_files", "list_folder_files2"]}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            files = self.folder.list_files()
            file_list = [file for file in files]
            self.assertEqual(len(file_list), 4)
            self.assertIsInstance(file_list[0], File)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_files()
    def test_get_files(self, m):
        register_uris({"folder": ["list_folder_files", "list_folder_files2"]}, m)

        files = self.folder.get_files()
        file_list = [file for file in files]
        self.assertEqual(len(file_list), 4)
        self.assertIsInstance(file_list[0], File)

    # delete()
    def test_delete_file(self, m):
        register_uris({"folder": ["delete_folder"]}, m)

        deleted_folder = self.folder.delete()

        self.assertIsInstance(deleted_folder, Folder)
        self.assertTrue(hasattr(deleted_folder, "name"))
        self.assertEqual(deleted_folder.full_name, "course_files/Folder 1")

    # list_folders()
    def test_list_folders(self, m):
        register_uris({"folder": ["list_folders"]}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            folders = self.folder.list_folders()
            folder_list = [folder for folder in folders]
            self.assertEqual(len(folder_list), 2)
            self.assertIsInstance(folder_list[0], Folder)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_folders()
    def test_get_folders(self, m):
        register_uris({"folder": ["list_folders"]}, m)

        folders = self.folder.get_folders()
        folder_list = [folder for folder in folders]
        self.assertEqual(len(folder_list), 2)
        self.assertIsInstance(folder_list[0], Folder)

    # create_folder()
    def test_create_folder(self, m):
        register_uris({"folder": ["create_folder"]}, m)

        name_str = "Test String"
        response = self.folder.create_folder(name=name_str)
        self.assertIsInstance(response, Folder)

    # upload()
    def test_upload(self, m):
        register_uris({"folder": ["upload", "upload_final"]}, m)

        filename = "testfile_course_{}".format(uuid.uuid4().hex)

        try:
            with open(filename, "w+") as file:
                response = self.folder.upload(file)
            self.assertTrue(response[0])
            self.assertIsInstance(response[1], dict)
            self.assertIn("url", response[1])
        finally:
            cleanup_file(filename)

    # update()
    def test_update(self, m):
        register_uris({"folder": ["update"]}, m)

        new_name = "New Name"
        response = self.folder.update(name=new_name)
        self.assertIsInstance(response, Folder)
        self.assertEqual(self.folder.name, new_name)

    # copy_file()
    def test_copy_file(self, m):
        register_uris({"folder": ["copy_file"]}, m)

        new_file = self.folder.copy_file(1)
        self.assertIsInstance(new_file, File)
        self.assertEqual(new_file.display_name, "Dummy File-1")
        self.assertEqual(new_file.id, 1)
