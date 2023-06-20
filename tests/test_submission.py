import unittest
import uuid

import requests_mock

from canvasapi import Canvas
from canvasapi.file import File
from canvasapi.peer_review import PeerReview
from canvasapi.submission import GroupedSubmission, Submission
from tests import settings
from tests.util import cleanup_file, register_uris


@requests_mock.Mocker()
class TestSubmission(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    "course": ["get_by_id", "get_assignment_by_id"],
                    "section": ["get_by_id"],
                    "submission": ["get_by_id_course"],
                },
                m,
            )

            self.course = self.canvas.get_course(1)
            self.assignment = self.course.get_assignment(1)
            self.submission = self.assignment.get_submission(1)

    # __init__()
    def test__init__attachments(self, m):
        register_uris({"submission": ["get_by_id_with_attachments"]}, m)

        submission = self.assignment.get_submission(1)

        self.assertTrue(hasattr(submission, "attachments"))
        self.assertIsInstance(submission.attachments, list)
        self.assertEqual(len(submission.attachments), 1)
        self.assertIsInstance(submission.attachments[0], File)
        self.assertTrue(hasattr(submission.attachments[0], "id"))
        self.assertEqual(submission.attachments[0].id, 123)

    # __str__()
    def test__str__(self, m):
        string = str(self.submission)
        self.assertIsInstance(string, str)

    # create_submission_peer_review()
    def test_create_submission_peer_review(self, m):
        register_uris({"submission": ["create_submission_peer_review"]}, m)

        created_peer_review = self.submission.create_submission_peer_review(1)

        self.assertIsInstance(created_peer_review, PeerReview)
        self.assertEqual(created_peer_review.user_id, 7)

    # delete_submission_peer_review()
    def test_delete_submission_peer_review(self, m):
        register_uris({"submission": ["delete_submission_peer_review"]}, m)

        deleted_peer_review = self.submission.delete_submission_peer_review(1)

        self.assertIsInstance(deleted_peer_review, PeerReview)
        self.assertEqual(deleted_peer_review.user_id, 7)

    # edit()
    def test_edit(self, m):
        register_uris({"submission": ["edit"]}, m)

        self.assertFalse(hasattr(self.submission, "excused"))

        self.submission.edit(submission={"excuse": True})

        self.assertIsInstance(self.submission, Submission)
        self.assertTrue(hasattr(self.submission, "excused"))
        self.assertTrue(self.submission.excused)

    # get_submission_peer_reviews()
    def test_get_submission_peer_reviews(self, m):
        register_uris({"submission": ["list_submission_peer_reviews"]}, m)

        submission_peer_reviews = self.submission.get_submission_peer_reviews()
        submission_peer_review_list = [
            peer_review for peer_review in submission_peer_reviews
        ]

        self.assertEqual(len(submission_peer_review_list), 2)
        self.assertIsInstance(submission_peer_review_list[0], PeerReview)

    # mark_read()
    def test_mark_read(self, m):
        register_uris({"course": ["mark_submission_as_read"]}, m)

        marked_read = self.submission.mark_read()
        self.assertTrue(marked_read)

    # mark_unread()
    def test_mark_unread(self, m):
        register_uris({"course": ["mark_submission_as_unread"]}, m)

        marked_unread = self.submission.mark_unread()
        self.assertTrue(marked_unread)

    # upload_comment()
    def test_upload_comment(self, m):
        register_uris(
            {"submission": ["upload_comment", "upload_comment_final", "edit"]}, m
        )

        filename = "testfile_submission_{}".format(uuid.uuid4().hex)

        try:
            with open(filename, "w+") as file:
                response = self.submission.upload_comment(file)

            self.assertTrue(response[0])
            self.assertIsInstance(response[1], dict)
            self.assertIn("url", response[1])
        finally:
            cleanup_file(filename)


class TestGroupedSubmission(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        self.grouped_submission = GroupedSubmission(
            self.canvas._Canvas__requester,
            {
                "user_id": 1,
                "submissions": [
                    {
                        "id": 1,
                        "assignment_id": 1,
                        "user_id": 1,
                        "html_url": "https://example.com/courses/1/assignments/1/submissions/1",
                        "submission_type": "online_upload",
                    }
                ],
            },
        )

    # __init__()
    def test__init__no_submission_key(self):
        grouped_submission = GroupedSubmission(
            self.canvas._Canvas__requester, {"user_id": 1}
        )

        self.assertIsInstance(grouped_submission, GroupedSubmission)
        self.assertTrue(hasattr(grouped_submission, "submissions"))
        self.assertIsInstance(grouped_submission.submissions, list)
        self.assertEqual(len(grouped_submission.submissions), 0)

    # __str__()
    def test__str__(self):
        string = str(self.grouped_submission)
        self.assertIsInstance(string, str)
        self.assertEqual(string, "1 submission(s) for User #1")
