from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.login import Login
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestLogin(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"account": ["get_by_id"], "login": ["create_user_login"]}, m)

            self.account = self.canvas.get_account(1)
            self.login = self.account.create_user_login(
                user={"id": 1}, login={"unique_id": "belieber@example.com"}
            )

    # delete()
    def test_delete_user_login(self, m):
        register_uris({"login": ["delete_user_login"]}, m)

        deleted_user_login = self.login.delete()

        self.assertIsInstance(deleted_user_login, Login)
        self.assertTrue(hasattr(deleted_user_login, "unique_id"))
        self.assertEqual(deleted_user_login.unique_id, "belieber@example.com")

    # edit()
    def test_edit_user_login(self, m):
        register_uris({"login": ["edit_user_login"]}, m)

        unique_id = "newemail@example.com"
        edited_user_login = self.login.edit(
            user={"id": 1}, login={"unique_id": unique_id}
        )

        self.assertIsInstance(edited_user_login, Login)
        self.assertTrue(hasattr(edited_user_login, "unique_id"))
        self.assertEqual(edited_user_login.unique_id, unique_id)

    # __str__()
    def test__str__(self, m):
        string = str(self.login)
        self.assertIsInstance(string, str)
