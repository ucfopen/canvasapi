import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.assignment import AssignmentOverride
from canvasapi.enrollment import Enrollment
from canvasapi.progress import Progress
from canvasapi.section import Section
from canvasapi.submission import GroupedSubmission, Submission
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestSection(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "section": ["get_by_id"],
                "user": ["get_by_id"],
            }
            register_uris(requires, m)

            self.section = self.canvas.get_section(1)
            self.user = self.canvas.get_user(1)

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

    def test_enroll_user(self, m):
        requires = {"section": ["enroll_user"], "user": ["get_by_id"]}
        register_uris(requires, m)

        enrollment_type = "TeacherEnrollment"

        # by user ID
        enrollment_by_id = self.section.enroll_user(
            1, enrollment={"type": enrollment_type}
        )

        self.assertIsInstance(enrollment_by_id, Enrollment)
        self.assertTrue(hasattr(enrollment_by_id, "type"))
        self.assertEqual(enrollment_by_id.type, enrollment_type)

        # by user object
        enrollment_by_obj = self.section.enroll_user(
            self.user, enrollment={"type": enrollment_type}
        )

        self.assertIsInstance(enrollment_by_obj, Enrollment)
        self.assertTrue(hasattr(enrollment_by_obj, "type"))
        self.assertEqual(enrollment_by_obj.type, enrollment_type)
