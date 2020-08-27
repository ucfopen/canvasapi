import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestAuthenticationEvent(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "account": ["get_by_id", "get_authentication_events"],
                "login": ["create_user_login", "get_authentication_events"],
                "user": ["get_by_id", "get_authentication_events"],
            }
            register_uris(requires, m)

            self.account = self.canvas.get_account(1)
            self.login = self.account.create_user_login(
                user={"id": 1}, login={"unique_id": "belieber@example.com"}
            )
            self.user = self.canvas.get_user(1)

            self.authentication_event_account = (
                self.account.get_authentication_events()[0]
            )
            self.authentication_event_login = self.login.get_authentication_events()[0]
            self.authentication_event_user = self.user.get_authentication_events()[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.authentication_event_account)
        self.assertIsInstance(string, str)
