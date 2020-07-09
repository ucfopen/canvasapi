import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestCommMessage(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"comm_message": ["comm_messages"]}
            register_uris(requires, m)

            self.comm_message = self.canvas.get_comm_messages(2)[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.comm_message)
        self.assertIsInstance(string, str)
