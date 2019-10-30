from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.usage_rights import UsageRights
from tests import settings
from tests.util import register_uris

@requests_mock.Mocker()
class TestLicenses(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "user": ["get_by_id","list_licenses"]
            }

            register_uris(requires, m)

            self.user = self.canvas.get_user(1)
            self.licenses = list(self.user.list_licenses())

    # __str__()
    def test__str__(self, m):
        string = str(self.licenses[0])
        self.assertIsInstance(string, str)