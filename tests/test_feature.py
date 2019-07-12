from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestFeature(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"course": ["get_by_id", "get_features"]}
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.feature = self.course.get_features()[0]

    def test__str__(self, m):
        string = str(self.feature)
        self.assertIsInstance(string, str)
