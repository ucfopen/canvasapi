import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestUsageRights(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"user": ["get_by_id", "set_usage_rights"]}

            register_uris(requires, m)

            self.user = self.canvas.get_user(1)
            self.usage_rights = self.user.set_usage_rights(
                file_ids=[1, 2], usage_rights={"use_justification": "fair_use"}
            )

    # __str__()
    def test__str__(self, m):
        string = str(self.usage_rights)
        self.assertIsInstance(string, str)
