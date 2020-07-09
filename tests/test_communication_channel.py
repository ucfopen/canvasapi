import unittest

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
            register_uris({"user": ["get_by_id", "list_comm_channels"]}, m)

            self.user = self.canvas.get_user(1)
            self.comm_chan = self.user.get_communication_channels()[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.comm_chan)
        self.assertIsInstance(string, str)

    # get_preferences()
    def test_get_preferences(self, m):
        register_uris({"communication_channel": ["list_preferences"]}, m)

        preferences = self.comm_chan.get_preferences()
        preference_list = [preference for preference in preferences]

        self.assertEqual(len(preference_list), 2)
        self.assertEqual(preference_list[0]["notification"], "new_announcement")

    # get_preference_categories()
    def test_get_preference_categories(self, m):
        register_uris({"communication_channel": ["list_preference_categories"]}, m)

        categories = self.comm_chan.get_preference_categories()

        self.assertEqual(len(categories), 2)
        self.assertIsInstance(categories, list)
        self.assertEqual(categories[0], "announcement")

    # get_preference()
    def test_get_preference(self, m):
        register_uris({"communication_channel": ["get_preference"]}, m)

        preference = self.comm_chan.get_preference("new_announcement")
        self.assertIsInstance(preference, NotificationPreference)
        self.assertTrue(hasattr(preference, "notification"))
        self.assertEqual(preference.notification, "new_announcement")

    # update_preference()
    def test_update_preference(self, m):
        register_uris({"communication_channel": ["update_preference"]}, m)
        notification = "new_announcement"
        frequency = "daily"

        updated_pref = self.comm_chan.update_preference(
            notification=notification, frequency=frequency
        )

        self.assertIsInstance(updated_pref, NotificationPreference)
        self.assertEqual(updated_pref.frequency, frequency)
        self.assertEqual(updated_pref.notification, notification)
        self.assertEqual(updated_pref.category, "announcement")

    # update_preferences_by_category()
    def test_update_preferences_by_category(self, m):
        register_uris({"communication_channel": ["update_preferences_by_category"]}, m)
        category = "course_content"
        frequency = "daily"

        updated_prefs = self.comm_chan.update_preferences_by_catagory(
            category=category, frequency=frequency
        )

        self.assertEqual(len(updated_prefs), 3)
        self.assertEqual(updated_prefs[0]["frequency"], frequency)
        self.assertEqual(updated_prefs[0]["category"], category)
        self.assertEqual(updated_prefs[0]["notification"], "assignment_changed")

    # update_multiple_preferences()
    def test_update_multiple_preferences(self, m):
        register_uris({"communication_channel": ["update_multiple_preferences"]}, m)

        notification_preferences = {
            "assignment_due_date_changed": {"frequency": "daily"},
            "assignment_changed": {"frequency": "daily"},
        }

        updated_prefs = self.comm_chan.update_multiple_preferences(
            notification_preferences=notification_preferences
        )

        self.assertEqual(len(updated_prefs), 2)
        self.assertEqual(updated_prefs[0]["frequency"], "daily")

        empty_notification_preferences = {}
        self.assertFalse(
            self.comm_chan.update_multiple_preferences(
                notification_preferences=empty_notification_preferences
            )
        )

        frequency_empty_notification_preferences = {"got_no_freq": {"frequency": ""}}
        self.assertFalse(
            self.comm_chan.update_multiple_preferences(
                notification_preferences=frequency_empty_notification_preferences
            )
        )

        no_frequency_notification_preferences = {"got_no_freq": {"nope": "no_way"}}
        self.assertFalse(
            self.comm_chan.update_multiple_preferences(
                notification_preferences=no_frequency_notification_preferences
            )
        )

    # delete()
    def test_delete(self, m):
        register_uris(
            {"communication_channel": ["create_comm_channel", "delete_comm_channel"]}, m
        )

        channel = {"type": "email", "address": "username@example.org"}
        new_channel = self.user.create_communication_channel(
            communication_channel=channel
        )
        self.assertTrue(new_channel.delete())
