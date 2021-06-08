import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.poll_submission import PollSubmission
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestPollSubmission(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "poll": ["get_poll"],
                "poll_session": ["get_session"],
                "poll_submission": ["get_submission"],
            }
            register_uris(requires, m)

            self.poll = self.canvas.get_poll(1)
            self.poll.poll_session = self.poll.get_session(1)
            self.poll.poll_session.poll_submission = (
                self.poll.poll_session.get_submission(1)
            )

    # __str__()
    def test__str__(self, m):
        string = str(self.poll.poll_session.poll_submission)
        self.assertIsInstance(string, str)

    # get_submission()
    def test_get_submission(self, m):
        register_uris({"poll_submission": ["get_submission"]}, m)

        choice_by_id = self.poll.poll_session.get_submission(1)
        self.assertIsInstance(choice_by_id, PollSubmission)
        self.assertTrue(hasattr(choice_by_id, "id"))
        self.assertTrue(hasattr(choice_by_id, "poll_choice_id"))
        self.assertTrue(hasattr(choice_by_id, "user_id"))
        self.assertTrue(hasattr(choice_by_id, "created_at"))

        choice_by_obj = self.poll.poll_session.get_submission(choice_by_id)
        self.assertIsInstance(choice_by_obj, PollSubmission)
        self.assertTrue(hasattr(choice_by_obj, "id"))
        self.assertTrue(hasattr(choice_by_obj, "poll_choice_id"))
        self.assertTrue(hasattr(choice_by_obj, "user_id"))
        self.assertTrue(hasattr(choice_by_obj, "created_at"))

    # create_submission()
    def test_create_submission(self, m):
        register_uris({"poll_submission": ["create_submission"]}, m)

        new_submission = self.poll.poll_session.create_submission(
            [{"poll_choice_id": 1}]
        )
        self.assertIsInstance(new_submission, PollSubmission)
        self.assertEqual(new_submission.poll_choice_id, 1)

    # create_submission()
    def test_create_submission_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.poll.poll_session.create_submission(poll_submissions={})
