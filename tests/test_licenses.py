import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestLicenses(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"user": ["get_by_id", "get_licenses"]}

            register_uris(requires, m)

            self.user = self.canvas.get_user(1)
            self.licenses = list(self.user.get_licenses())

    # __str__()
    def test__str__(self, m):
        string = str(self.licenses[0])
        self.assertIsInstance(string, str)
