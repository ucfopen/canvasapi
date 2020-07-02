import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.bookmark import Bookmark
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestBookmark(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {"bookmark": ["get_bookmark"], "current_user": ["get_by_id"]}, m
            )

            self.user = self.canvas.get_current_user()
            self.bookmark = self.user.get_bookmark(45)

    # delete()
    def test_delete_bookmark(self, m):
        register_uris({"bookmark": ["delete_bookmark"]}, m)

        deleted_bookmark = self.bookmark.delete()

        self.assertIsInstance(deleted_bookmark, Bookmark)
        self.assertTrue(hasattr(deleted_bookmark, "name"))
        self.assertEqual(deleted_bookmark.name, "Test Bookmark 3")

    # edit()
    def test_edit_bookmark(self, m):
        register_uris({"bookmark": ["edit_bookmark"]}, m)

        name = "New Name"
        url = "http//happy-place.com"
        edited_bookmark = self.bookmark.edit(name=name, url=url)

        self.assertIsInstance(edited_bookmark, Bookmark)
        self.assertTrue(hasattr(edited_bookmark, "name"))
        self.assertEqual(edited_bookmark.name, name)

    # __str__()
    def test__str__(self, m):
        string = str(self.bookmark)
        self.assertIsInstance(string, str)
