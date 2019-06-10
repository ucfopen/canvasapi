from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.poll import Poll
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestPoll(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'poll': ['get_poll']}, m)
            self.poll = self.canvas.get_poll(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.poll)
        self.assertIsInstance(string, str)

    # get_polls()
    def test_get_polls(self, m):
        register_uris({'poll': ['get_polls']}, m)

        polls = self.canvas.get_polls()
        polls_list = [poll for poll in polls]

        self.assertEqual(len(polls_list), 2)
        self.assertIsInstance(polls_list[0], Poll)
        self.assertIsInstance(polls_list[1], Poll)

    # get_poll()
    def test_get_poll(self, m):
        register_uris({'poll': ['get_poll']}, m)

        poll_by_id = self.canvas.get_poll(1)
        self.assertIsInstance(poll_by_id, Poll)
        self.assertEqual(poll_by_id.question, 'Is this a question?')
        self.assertEqual(poll_by_id.description, 'This is a test.')
        self.assertEqual(poll_by_id.created_at, '2014-01-07T13:10:19Z')

        poll_by_obj = self.canvas.get_poll(poll_by_id)
        self.assertIsInstance(poll_by_obj, Poll)
        self.assertEqual(poll_by_obj.question, 'Is this a question?')
        self.assertEqual(poll_by_obj.description, 'This is a test.')
        self.assertEqual(poll_by_obj.created_at, '2014-01-07T13:10:19Z')

    # create_poll()
    def test_create_poll(self, m):
        register_uris({'poll': ['create_poll']}, m)

        new_poll = self.canvas.create_poll('Is this a question?', 'This is a test.')

        self.assertIsInstance(new_poll, Poll)
        self.assertTrue(hasattr(new_poll, 'question'))
        self.assertTrue(hasattr(new_poll, 'description'))

    # update()
    def test_update(self, m):
        register_uris({'poll': ['update']}, m)

        updated_poll = self.poll.update('Is this not a question?', 'This is a drill.')

        self.assertIsInstance(updated_poll, Poll)
        self.assertEqual(updated_poll.question, 'Is this not a question?')
        self.assertEqual(updated_poll.description, 'This is a drill.')

    # delete_poll()
    def test_delete_poll(self, m):
        register_uris({'poll': ['delete_poll']}, m)

        delete_by_id = self.canvas.delete_poll(1)
        self.assertTrue(delete_by_id)

        delete_by_obj = self.canvas.delete_poll(self.poll)
        self.assertTrue(delete_by_obj)
