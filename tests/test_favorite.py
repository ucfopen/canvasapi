from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestFavorite(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                'current_user': ['add_favorite_course', 'add_favorite_group', 'get_by_id'],
                'course': ['get_by_id'], 'user': ['get_by_id']
            }
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.user = self.canvas.get_current_user()
            self.favorite = self.user.add_favorite_course(self.course)

    # __str__()
    def test__str__(self, m):
        string = str(self.favorite)
        self.assertIsInstance(string, str)
