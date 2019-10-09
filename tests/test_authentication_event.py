from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.authentication_event import AuthenticationEvent
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestAuthenticationEvent(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "account": ["get_by_id", "get_authentication_event"],
                "login": ["get_by_id", "get_authentication_event"],
                "user": ["get_by_id", "get_authentication_event"],
            }
            register_uris(requires, m)

            self.account = self.canvas.get_account(1)
            self.user = self.canvas.get_user(1)

            self.authentication_event_account = self.account.get_authentication_event()
            self.authentication_event_user = self.user.get_authentication_event()

    # __str__()
    def test__str__(self, m):
        string = str(self.authentication_event_account)
        self.assertIsInstance(string, str)
