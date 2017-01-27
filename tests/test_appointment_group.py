import unittest

import requests_mock

from pycanvas import Canvas
from pycanvas.appointment_group import AppointmentGroup
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestAppointmentGroup(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'appointment_group': ['get_appointment_group']}, m)

            self.appointment_group = self.canvas.get_appointment_group(567)

    # delete()
    def test_delete_appointment_group(self, m):
        register_uris({'appointment_group': ['delete_appointment_group']}, m)

        deleted_appointment_group = self.appointment_group.delete()

        self.assertIsInstance(deleted_appointment_group, AppointmentGroup)
        self.assertTrue(hasattr(deleted_appointment_group, 'title'))
        self.assertEqual(deleted_appointment_group.title, 'Test Group 3')

    # edit()
    def test_edit_appointment_group(self, m):
        register_uris({'appointment_group': ['edit_appointment_group']}, m)

        title = 'New Name'
        edited_appointment_group = self.appointment_group.edit(
            appointment_group={'title': title}
        )

        self.assertIsInstance(edited_appointment_group, AppointmentGroup)
        self.assertTrue(hasattr(edited_appointment_group, 'title'))
        self.assertEqual(edited_appointment_group.title, title)

    # __str__()
    def test__str__(self, m):
        string = str(self.appointment_group)
        self.assertIsInstance(string, str)
