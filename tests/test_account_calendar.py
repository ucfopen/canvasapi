import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestAccountCalendar(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"account": ["get_account_calendar", "get_by_id"]}, m)

            self.account = self.canvas.get_account(1)
            self.account_calendar = self.account.get_account_calendar()

    # __str__()
    def test__str__(self, m):
        string = str(self.account_calendar)
        self.assertIsInstance(string, str)
