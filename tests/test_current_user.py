from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock
import warnings

from canvasapi import Canvas
from canvasapi.bookmark import Bookmark
from canvasapi.group import Group
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestCurrentUser(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)
        with requests_mock.Mocker() as m:
            register_uris({'current_user': ['get_by_id']}, m)
            self.user = self.canvas.get_current_user()

    # __str__()
    def test__str__(self, m):
        string = str(self.user)
        self.assertIsInstance(string, str)

    # list_groups()
    def test_list_groups(self, m):
        register_uris({'current_user': ['list_groups', 'list_groups2']}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            groups = self.user.list_groups()
            group_list = [group for group in groups]

            self.assertEqual(len(group_list), 4)
            self.assertIsInstance(group_list[0], Group)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_groups()
    def test_get_groups(self, m):
        register_uris({'current_user': ['list_groups', 'list_groups2']}, m)

        groups = self.user.get_groups()
        group_list = [group for group in groups]

        self.assertEqual(len(group_list), 4)
        self.assertIsInstance(group_list[0], Group)

    # list_bookmarks()
    def test_list_bookmarks(self, m):
        register_uris({'bookmark': ['list_bookmarks']}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            bookmarks = self.user.list_bookmarks()
            bookmark_list = [bookmark for bookmark in bookmarks]
            self.assertEqual(len(bookmark_list), 2)
            self.assertIsInstance(bookmark_list[0], Bookmark)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_bookmarks()
    def test_get_bookmarks(self, m):
        register_uris({'bookmark': ['list_bookmarks']}, m)

        bookmarks = self.user.get_bookmarks()
        bookmark_list = [bookmark for bookmark in bookmarks]
        self.assertEqual(len(bookmark_list), 2)
        self.assertIsInstance(bookmark_list[0], Bookmark)

    # get_bookmark()
    def test_get_bookmark(self, m):
        register_uris({'bookmark': ['get_bookmark']}, m)

        bookmark_by_id = self.user.get_bookmark(45)
        self.assertIsInstance(bookmark_by_id, Bookmark)
        self.assertEqual(bookmark_by_id.name, "Test Bookmark 3")
        bookmark_by_obj = self.user.get_bookmark(bookmark_by_id)
        self.assertIsInstance(bookmark_by_obj, Bookmark)
        self.assertEqual(bookmark_by_obj.name, "Test Bookmark 3")

    # create_bookmark()
    def test_create_bookmark(self, m):
        register_uris({'bookmark': ['create_bookmark']}, m)
        evnt = self.user.create_bookmark(
            name="Test Bookmark",
            url="https://www.google.com"
        )
        self.assertIsInstance(evnt, Bookmark)
        self.assertEqual(evnt.name, "Test Bookmark")
        self.assertEqual(evnt.url, "https://www.google.com")
