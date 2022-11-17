import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestJWT(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"jwt": ["create_jwt"]}, m)

            self.jwt = self.canvas.create_jwt()

    # __str__()
    def test__str__(self, m):
        string = str(self.jwt)
        self.assertIsInstance(string, str)
