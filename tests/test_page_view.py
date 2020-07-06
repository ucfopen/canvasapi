import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestPageView(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"user": ["get_by_id", "page_views", "page_views_p2"]}, m)

            self.user = self.canvas.get_user(1)
            pageviews = self.user.get_page_views()
            self.pageview = pageviews[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.pageview)
        self.assertIsInstance(string, str)
