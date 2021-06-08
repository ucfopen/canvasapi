import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestExternalFeed(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"course": ["get_by_id", "list_external_feeds"]}, m)

            self.course = self.canvas.get_course(1)
            self.external_feed = self.course.get_external_feeds()[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.external_feed)
        self.assertIsInstance(string, str)
