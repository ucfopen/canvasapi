from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import warnings

import requests
import requests_mock

from canvasapi import Canvas
from canvasapi.course import Course
from canvasapi.gradebook_history import SubmissionHistory
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestGradebookHistory(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("always", DeprecationWarning)

        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "course": ["get_assignment_by_id", "get_by_id", "get_page"],
                "quiz": ["get_by_id"],
                "user": ["get_by_id"],
            }
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.uncollated_submission = self.course.get_uncollated_submissions()

    #get_submissions
    def test_get_submissions(self, m):
        register_uris({"gradebook_history": ["get_submissions"]}, m)

        submissions = self.uncollated_submission.get_submissions(1, 1, "03-26-2019")
        sub_list = [sub for sub in submissions]
        self.assertEqual(len(sub_list), 2)
        self.assertIsInstance(sub_list[0], SubmissionHistory)
        self.assertIsInstance(sub_list[1], SubmissionHistory)