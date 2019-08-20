from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import warnings

import requests_mock

from canvasapi import Canvas
from canvasapi.assignment import AssignmentOverride
from canvasapi.enrollment import Enrollment
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.progress import Progress
from canvasapi.section import Section
from canvasapi.submission import GroupedSubmission, Submission
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestSection(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("always", DeprecationWarning)

        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"section": ["get_by_id"]}, m)

            self.section = self.canvas.get_section(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.section)
        self.assertIsInstance(string, str)

    # get_assignment_override
    def test_get_assignment_override(self, m):
        register_uris({"assignment": ["override_section_alias"]}, m)

        override = self.section.get_assignment_override(1)

        self.assertIsInstance(override, AssignmentOverride)
        self.assertEqual(override.course_section_id, self.section.id)

    # get_enrollments()
    def test_get_enrollments(self, m):
        register_uris({"section": ["list_enrollments", "list_enrollments_2"]}, m)

        enrollments = self.section.get_enrollments()
        enrollment_list = [enrollment for enrollment in enrollments]

        self.assertEqual(len(enrollment_list), 4)
        self.assertIsInstance(enrollment_list[0], Enrollment)

    def test_cross_list_section(self, m):
        register_uris({"course": ["get_by_id_2"], "section": ["crosslist_section"]}, m)

        section_by_id = self.section.cross_list_section(2)
        self.assertIsInstance(section_by_id, Section)

        course_obj = self.canvas.get_course(2)
        section_by_obj = self.section.cross_list_section(course_obj)
        self.assertIsInstance(section_by_obj, Section)

    def test_decross_list_section(self, m):
        register_uris({"section": ["decross_section"]}, m)

        section = self.section.decross_list_section()

        self.assertIsInstance(section, Section)

    def test_edit(self, m):
        register_uris({"section": ["edit"]}, m)

        edit = self.section.edit()

        self.assertIsInstance(edit, Section)

    def test_delete(self, m):
        register_uris({"section": ["delete"]}, m)

        deleted_section = self.section.delete()

        self.assertIsInstance(deleted_section, Section)

    # submit_assignment()
    def test_submit_assignment(self, m):
        register_uris(
            {
                "assignment": ["submit"],
                "submission": ["get_by_id_section"],
                "user": ["get_by_id", "get_user_assignments"],
            },
            m,
        )

        assignment_id = 1
        sub_type = "online_upload"
        sub_dict = {"submission_type": sub_type}
        with warnings.catch_warnings(record=True) as warning_list:
            assignment_by_id = self.section.submit_assignment(assignment_id, sub_dict)

            self.assertIsInstance(assignment_by_id, Submission)
            self.assertTrue(hasattr(assignment_by_id, "submission_type"))
            self.assertEqual(assignment_by_id.submission_type, sub_type)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

        user_obj = self.canvas.get_user(1)
        assignments_obj = user_obj.get_assignments(1)
        sub_type = "online_upload"
        sub_dict = {"submission_type": sub_type}
        with warnings.catch_warnings(record=True) as warning_list:
            assignment_by_obj = self.section.submit_assignment(
                assignments_obj[0], sub_dict
            )

            self.assertIsInstance(assignment_by_obj, Submission)
            self.assertTrue(hasattr(assignment_by_obj, "submission_type"))
            self.assertEqual(assignment_by_obj.submission_type, sub_type)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    def test_subit_assignment_fail(self, m):
        with warnings.catch_warnings(record=True) as warning_list:
            with self.assertRaises(RequiredFieldMissing):
                self.section.submit_assignment(1, {})
            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # list_submissions()
    def test_list_submissions(self, m):
        register_uris(
            {
                "submission": ["list_submissions"],
                "user": ["get_by_id", "get_user_assignments"],
            },
            m,
        )

        assignment_id = 1
        with warnings.catch_warnings(record=True) as warning_list:
            submissions_by_id = self.section.list_submissions(assignment_id)
            submission_list_by_id = [submission for submission in submissions_by_id]

            self.assertEqual(len(submission_list_by_id), 2)
            self.assertIsInstance(submission_list_by_id[0], Submission)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

        user_obj = self.canvas.get_user(1)
        assignments_obj = user_obj.get_assignments(1)
        with warnings.catch_warnings(record=True) as warning_list:
            submissions_by_obj = self.section.list_submissions(assignments_obj[0])
            submission_list_by_obj = [submission for submission in submissions_by_obj]

            self.assertEqual(len(submission_list_by_obj), 2)
            self.assertIsInstance(submission_list_by_obj[0], Submission)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # list_multiple_submission()
    def test_list_multiple_submissions(self, m):
        register_uris({"section": ["list_multiple_submissions"]}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            submissions = self.section.list_multiple_submissions()
            submission_list = [submission for submission in submissions]

            self.assertEqual(len(submission_list), 2)
            self.assertIsInstance(submission_list[0], Submission)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_multiple_submission()
    def test_get_multiple_submissions(self, m):
        register_uris({"section": ["list_multiple_submissions"]}, m)

        submissions = self.section.get_multiple_submissions()
        submission_list = [submission for submission in submissions]

        self.assertEqual(len(submission_list), 2)
        self.assertIsInstance(submission_list[0], Submission)

    def test_get_multiple_submissions_grouped_true(self, m):
        register_uris({"section": ["list_multiple_submissions_grouped"]}, m)

        submissions = self.section.get_multiple_submissions(grouped=True)
        submission_list = [submission for submission in submissions]

        self.assertEqual(len(submission_list), 2)
        self.assertIsInstance(submission_list[0], GroupedSubmission)

    def test_get_multiple_submissions_grouped_false(self, m):
        register_uris({"section": ["list_multiple_submissions"]}, m)

        submissions = self.section.get_multiple_submissions(grouped=False)
        submission_list = [submission for submission in submissions]

        self.assertEqual(len(submission_list), 2)
        self.assertIsInstance(submission_list[0], Submission)

    def test_get_multiple_submissions_grouped_invalid(self, m):
        with self.assertRaises(ValueError) as cm:
            self.section.get_multiple_submissions(grouped="blargh")

        self.assertIn("Parameter `grouped` must", cm.exception.args[0])

    # get_submission()
    def test_get_submission(self, m):
        register_uris(
            {
                "submission": ["get_by_id_course"],
                "user": ["get_by_id", "get_user_assignments"],
            },
            m,
        )

        assignment_id = 1
        user_id = 1
        with warnings.catch_warnings(record=True) as warning_list:
            submission_by_id = self.section.get_submission(assignment_id, user_id)

            self.assertIsInstance(submission_by_id, Submission)
            self.assertTrue(hasattr(submission_by_id, "submission_type"))

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

        user_obj = self.canvas.get_user(1)
        assignments_obj = user_obj.get_assignments(1)
        with warnings.catch_warnings(record=True) as warning_list:
            submission_by_obj = self.section.get_submission(
                assignments_obj[0], user_obj
            )

            self.assertIsInstance(submission_by_obj, Submission)
            self.assertTrue(hasattr(submission_by_obj, "submission_type"))

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # update_submission()
    def test_update_submission(self, m):
        register_uris(
            {
                "submission": ["get_by_id_section", "edit"],
                "user": ["get_by_id", "get_user_assignments"],
            },
            m,
        )

        assignment_id = 1
        user_id = 1
        with warnings.catch_warnings(record=True) as warning_list:
            submission_by_id = self.section.update_submission(
                assignment_id, user_id, submission={"excuse": True}
            )

            self.assertIsInstance(submission_by_id, Submission)
            self.assertTrue(hasattr(submission_by_id, "excused"))

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

        user_obj = self.canvas.get_user(1)
        assignments_obj = user_obj.get_assignments(1)

        with warnings.catch_warnings(record=True) as warning_list:
            submission_by_obj = self.section.update_submission(
                assignments_obj[0], user_obj, submission={"excuse": True}
            )

            self.assertIsInstance(submission_by_obj, Submission)
            self.assertTrue(hasattr(submission_by_obj, "excused"))

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # mark_submission_as_read
    def test_mark_submission_as_read(self, m):
        register_uris(
            {
                "course": ["mark_submission_as_read"],
                "submission": ["get_by_id_section"],
                "user": ["get_by_id", "get_user_assignments"],
            },
            m,
        )

        submission_id = 1
        user_id = 1
        with warnings.catch_warnings(record=True) as warning_list:
            submission_by_id = self.section.mark_submission_as_read(
                submission_id, user_id
            )

            self.assertTrue(submission_by_id)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

        user_obj = self.canvas.get_user(1)
        with warnings.catch_warnings(record=True) as warning_list:
            assignments_obj = user_obj.get_assignments(1)
            submission_by_obj = self.section.mark_submission_as_read(
                assignments_obj[0], user_obj
            )

            self.assertTrue(submission_by_obj)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # mark_submission_as_unread
    def test_mark_submission_as_unread(self, m):
        register_uris(
            {
                "course": ["mark_submission_as_unread"],
                "submission": ["get_by_id_section"],
                "user": ["get_by_id", "get_user_assignments"],
            },
            m,
        )

        user_id = 1
        assignment_id = 1
        with warnings.catch_warnings(record=True) as warning_list:
            submission_by_id = self.section.mark_submission_as_unread(
                assignment_id, user_id
            )
            self.assertTrue(submission_by_id)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

        user_obj = self.canvas.get_user(1)
        assignments_obj = user_obj.get_assignments(1)
        with warnings.catch_warnings(record=True) as warning_list:
            submission_by_obj = self.section.mark_submission_as_unread(
                assignments_obj[0], user_obj
            )
            self.assertTrue(submission_by_obj)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    def test_submissions_bulk_update(self, m):
        register_uris({"section": ["update_submissions"]}, m)
        register_uris({"progress": ["course_progress"]}, m)
        progress = self.section.submissions_bulk_update(
            grade_data={"1": {"1": {"posted_grade": 97}, "2": {"posted_grade": 98}}}
        )
        self.assertIsInstance(progress, Progress)
        self.assertTrue(progress.context_type == "Course")
        progress = progress.query()
        self.assertTrue(progress.context_type == "Course")
