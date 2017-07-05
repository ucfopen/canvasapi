from __future__ import unicode_literals
import unittest

from builtins import str
import requests_mock

from canvasapi import Canvas
from canvasapi.notification_preference import NotificationPreference
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestCommunicationChannel(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'user': ['get_by_id', 'list_comm_channels']}, m)

            self.user = self.canvas.get_user(1)
            self.comm_chan = self.user.list_communication_channels()[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.comm_chan)
        self.assertIsInstance(string, str)

    # list_preferences()
    def test_list_preferences(self, m):
        register_uris({'communication_channel': ['list_preferences']}, m)

        preferences = self.comm_chan.list_preferences()
        preference_list = [preference for preference in preferences]

        self.assertEqual(len(preference_list), 2)
        self.assertEqual(preference_list[0]['notification'], 'new_announcement')

    # list_preference_categories()
    def test_list_preference_categories(self, m):
        register_uris({'communication_channel': ['list_preference_categories']}, m)

        categories = self.comm_chan.list_preference_categories()

        self.assertEqual(len(categories), 2)
        self.assertIsInstance(categories, list)
        self.assertEqual(categories[0], 'announcement')

    # get_preference()
    def test_get_preference(self, m):
        register_uris({'communication_channel': ['get_preference']}, m)

        preference = self.comm_chan.get_preference('new_announcement')
        self.assertIsInstance(preference, NotificationPreference)
        self.assertTrue(hasattr(preference, 'notification'))
        self.assertEqual(preference.notification, 'new_announcement')
