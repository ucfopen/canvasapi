import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.communication_channel import CommunicationChannel
# from canvasapi.course import Course
# from canvasapi.exceptions import RequiredFieldMissing
# from canvasapi.group import Group
# from canvasapi.enrollment import Enrollment
# from canvasapi.page_view import PageView
# from canvasapi.user import User
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestCommunicationChannel(unittest.TestCase):

    @classmethod
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

    # delete()
    def test_delete(self, m):
        register_uris({'communication_channel': ['delete']}, m)
        response = self.comm_chan.delete()

        self.assertIsInstance(response, CommunicationChannel)
        self.assertTrue(hasattr(response, 'address'))
        self.assertEqual(response.address, 'user@example.com')
