import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.poll import Poll
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestPoll(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"poll": ["get_poll"]}, m)
            self.poll = self.canvas.get_poll(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.poll)
        self.assertIsInstance(string, str)

    # get_polls()
    def test_get_polls(self, m):
        register_uris({"poll": ["get_polls"]}, m)

        polls_list = self.canvas.get_polls()

        self.assertIsInstance(polls_list[0], Poll)
        self.assertIsInstance(polls_list[1], Poll)

    # get_poll()
    def test_get_poll(self, m):
        register_uris({"poll": ["get_poll"]}, m)

        poll_by_id = self.canvas.get_poll(1)
        self.assertIsInstance(poll_by_id, Poll)
        self.assertEqual(poll_by_id.question, "Is this a question?")
        self.assertEqual(poll_by_id.description, "This is a test.")
        self.assertEqual(poll_by_id.created_at, "2014-01-07T13:10:19Z")

        poll_by_obj = self.canvas.get_poll(poll_by_id)
        self.assertIsInstance(poll_by_obj, Poll)
        self.assertEqual(poll_by_obj.question, "Is this a question?")
        self.assertEqual(poll_by_obj.description, "This is a test.")
        self.assertEqual(poll_by_obj.created_at, "2014-01-07T13:10:19Z")

    # update()
    def test_update(self, m):
        register_uris({"poll": ["update"]}, m)

        updated_poll_q = self.poll.update([{"question": "Is this not a question?"}])
        self.assertIsInstance(updated_poll_q, Poll)
        self.assertEqual(updated_poll_q.question, "Is this not a question?")

        updated_poll_q_and_d = self.poll.update(
            [
                {"question": "Is this not a question?"},
                {"description": "This is not a test."},
            ]
        )
        self.assertIsInstance(updated_poll_q_and_d, Poll)
        self.assertEqual(updated_poll_q_and_d.question, "Is this not a question?")
        self.assertEqual(updated_poll_q_and_d.description, "This is not a test.")

    # update
    def test_update_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.poll.update(poll={})

    # delete_poll()
    def test_delete(self, m):
        register_uris({"poll": ["delete"]}, m)

        result = self.poll.delete()
        self.assertTrue(result)
