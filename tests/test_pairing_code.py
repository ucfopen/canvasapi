import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.pairing_code import PairingCode
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestPairingCode(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"user": ["get_by_id"]}
            register_uris(requires, m)

            self.user = self.canvas.get_user(1)

    # __str__()
    def test__str__(self, m):
        register_uris({"user": ["observer_pairing_codes"]}, m)

        pairing_code = self.user.create_pairing_code()
        self.assertIsInstance(pairing_code, PairingCode)
        self.assertEqual("1 - abc123", pairing_code.__str__())
