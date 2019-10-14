from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.favorite import Favorite
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestFavorite(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "current_user": [
                    "add_favorite_course",
                    "add_favorite_group",
                    "get_by_id",
                ]
            }
            register_uris(requires, m)

            self.user = self.canvas.get_current_user()
            self.favorite_course = self.user.add_favorite_course(1)
            self.favorite_group = self.user.add_favorite_group(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.favorite_course)
        self.assertIsInstance(string, str)

        string = str(self.favorite_group)
        self.assertIsInstance(string, str)

    # remove()
    def test_remove_favorite_course(self, m):
        register_uris({"current_user": ["remove_favorite_course"]}, m)

        evnt = self.favorite_course.remove()
        self.assertIsInstance(evnt, Favorite)
        self.assertEqual(evnt.context_type, "course")
        self.assertEqual(evnt.context_id, 1)

    def test_remove_favorite_group(self, m):
        register_uris({"current_user": ["remove_favorite_group"]}, m)

        evnt = self.favorite_group.remove()
        self.assertIsInstance(evnt, Favorite)
        self.assertEqual(evnt.context_type, "group")
        self.assertEqual(evnt.context_id, 1)
