from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestNotificationPreference(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                'user': ['get_by_id', 'list_comm_channels'],
                'communication_channel': ['get_preference']
            }
            register_uris(requires, m)

            self.user = self.canvas.get_user(1)
            self.comm_chan = self.user.list_communication_channels()[0]
            self.notif_pref = self.comm_chan.get_preference('new_announcement')

    # __str__()
    def test__str__(self, m):
        string = str(self.notif_pref)
        self.assertIsInstance(string, str)
