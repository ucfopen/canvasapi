from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

from builtins import str
import requests_mock

from canvasapi import Canvas
from canvasapi.enrollment import Enrollment
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.section import Section
from canvasapi.submission import Submission
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestSection(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'section': ['get_by_id']}, m)

            self.section = self.canvas.get_section(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.section)
        self.assertIsInstance(string, str)

    # list_enrollments()
    def test_get_enrollments(self, m):
        register_uris({'section': ['list_enrollments', 'list_enrollments_2']}, m)

        enrollments = self.section.get_enrollments()
        enrollment_list = [enrollment for enrollment in enrollments]

        self.assertEqual(len(enrollment_list), 4)
        self.assertIsInstance(enrollment_list[0], Enrollment)

    def test_cross_list_section(self, m):
        register_uris({'section': ['crosslist_section']}, m)

        section = self.section.cross_list_section(2)

        self.assertIsInstance(section, Section)

    def test_decross_list_section(self, m):
        register_uris({'section': ['decross_section']}, m)

        section = self.section.decross_list_section()

        self.assertIsInstance(section, Section)

    def test_edit(self, m):
        register_uris({'section': ['edit']}, m)

        edit = self.section.edit()

        self.assertIsInstance(edit, Section)

    def test_delete(self, m):
        register_uris({'section': ['delete']}, m)

        deleted_section = self.section.delete()

        self.assertIsInstance(deleted_section, Section)

    # submit_assignment()
    def test_submit_assignment(self, m):
        register_uris({'section': ['submit_assignment']}, m)

        assignment_id = 1
        sub_type = "online_upload"
        sub_dict = {'submission_type': sub_type}
        assignment = self.section.submit_assignment(assignment_id, sub_dict)

        self.assertIsInstance(assignment, Submission)
        self.assertTrue(hasattr(assignment, 'submission_type'))
        self.assertEqual(assignment.submission_type, sub_type)

    def test_subit_assignment_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.section.submit_assignment(1, {})

    # list_submissions()
    def test_list_submissions(self, m):
        register_uris({'section': ['list_submissions']}, m)

        assignment_id = 1
        submissions = self.section.list_submissions(assignment_id)
        submission_list = [submission for submission in submissions]

        self.assertEqual(len(submission_list), 2)
        self.assertIsInstance(submission_list[0], Submission)

    # list_multiple_submission()
    def test_list_multiple_submissions(self, m):
        register_uris({'section': ['list_multiple_submissions']}, m)

        submissions = self.section.list_multiple_submissions()
        submission_list = [submission for submission in submissions]

        self.assertEqual(len(submission_list), 2)
        self.assertIsInstance(submission_list[0], Submission)

    # get_submission()
    def test_get_submission(self, m):
        register_uris({'section': ['get_submission']}, m)

        assignment_id = 1
        user_id = 1
        submission = self.section.get_submission(assignment_id, user_id)

        self.assertIsInstance(submission, Submission)
        self.assertTrue(hasattr(submission, 'submission_type'))

    # update_submission()
    def test_update_submission(self, m):
        register_uris({'section': ['update_submission', 'get_submission']}, m)

        assignment_id = 1
        user_id = 1
        submission = self.section.update_submission(
            assignment_id,
            user_id,
            submission={'excuse': True}
        )

        self.assertIsInstance(submission, Submission)
        self.assertTrue(hasattr(submission, 'excused'))

    # mark_submission_as_read
    def test_mark_submission_as_read(self, m):
        register_uris({'section': ['mark_submission_as_read']}, m)

        submission_id = 1
        user_id = 1
        submission = self.section.mark_submission_as_read(submission_id, user_id)

        self.assertTrue(submission)

    # mark_submission_as_unread
    def test_mark_submission_as_unread(self, m):
        register_uris({'section': ['mark_submission_as_unread']}, m)

        submission_id = 1
        user_id = 1
        submission = self.section.mark_submission_as_unread(submission_id, user_id)

        self.assertTrue(submission)
