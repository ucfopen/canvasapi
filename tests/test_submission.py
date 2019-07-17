from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import uuid
import warnings

import requests_mock

from canvasapi import Canvas
from canvasapi.peer_review import PeerReview
from canvasapi.submission import GroupedSubmission, Submission
from tests import settings
from tests.util import cleanup_file, register_uris


@requests_mock.Mocker()
class TestSubmission(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("always", DeprecationWarning)

        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    "course": ["get_by_id", "get_assignment_by_id"],
                    "section": ["get_by_id"],
                    "submission": ["get_by_id_course", "get_by_id_section"],
                },
                m,
            )

            with warnings.catch_warnings(record=True) as warning_list:
                self.course = self.canvas.get_course(1)
                self.submission_course = self.course.get_submission(1, 1)

                self.section = self.canvas.get_section(1)
                self.submission_section = self.section.get_submission(1, 1)

                self.assertEqual(len(warning_list), 2)
                self.assertEqual(warning_list[0].category, DeprecationWarning)
                self.assertEqual(warning_list[1].category, DeprecationWarning)

    # __str__()
    def test__str__(self, m):
        string = str(self.submission_course)
        self.assertIsInstance(string, str)

    # create_submission_peer_review()
    def test_create_submission_peer_review(self, m):
        register_uris({"submission": ["create_submission_peer_review"]}, m)

        created_peer_review = self.submission_course.create_submission_peer_review(1)

        self.assertIsInstance(created_peer_review, PeerReview)
        self.assertEqual(created_peer_review.user_id, 7)

    # delete_submission_peer_review()
    def test_delete_submission_peer_review(self, m):
        register_uris({"submission": ["delete_submission_peer_review"]}, m)

        deleted_peer_review = self.submission_course.delete_submission_peer_review(1)

        self.assertIsInstance(deleted_peer_review, PeerReview)
        self.assertEqual(deleted_peer_review.user_id, 7)

    # edit()
    def test_edit(self, m):
        register_uris({"submission": ["edit"]}, m)

        self.assertFalse(hasattr(self.submission_course, "excused"))

        self.submission_course.edit(submission={"excuse": True})

        self.assertIsInstance(self.submission_course, Submission)
        self.assertTrue(hasattr(self.submission_course, "excused"))
        self.assertTrue(self.submission_course.excused)

    # get_submission_peer_reviews()
    def test_get_submission_peer_reviews(self, m):
        register_uris({"submission": ["list_submission_peer_reviews"]}, m)

        submission_peer_reviews = self.submission_course.get_submission_peer_reviews()
        submission_peer_review_list = [
            peer_review for peer_review in submission_peer_reviews
        ]

        self.assertEqual(len(submission_peer_review_list), 2)
        self.assertIsInstance(submission_peer_review_list[0], PeerReview)

    # upload_comment()
    def test_upload_comment(self, m):
        register_uris(
            {"submission": ["upload_comment", "upload_comment_final", "edit"]}, m
        )

        filename = "testfile_submission_{}".format(uuid.uuid4().hex)

        try:
            with open(filename, "w+") as file:
                response = self.submission_course.upload_comment(file)

            self.assertTrue(response[0])
            self.assertIsInstance(response[1], dict)
            self.assertIn("url", response[1])
        finally:
            cleanup_file(filename)

    def test_upload_comment_section(self, m):
        register_uris(
            {"submission": ["upload_comment", "upload_comment_final", "edit"]}, m
        )

        filename = "testfile_submission_{}".format(uuid.uuid4().hex)

        try:
            with open(filename, "w+") as file:
                response = self.submission_section.upload_comment(file)

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
