from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import uuid

import requests_mock

from canvasapi import Canvas
from canvasapi.assignment import Assignment, AssignmentGroup, AssignmentOverride
from canvasapi.exceptions import CanvasException, RequiredFieldMissing
from canvasapi.peer_review import PeerReview
from canvasapi.progress import Progress
from canvasapi.submission import Submission
from canvasapi.user import UserDisplay
from tests import settings
from tests.util import register_uris, cleanup_file


@requests_mock.Mocker()
class TestAssignment(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"course": ["get_by_id", "get_assignment_by_id"]}, m)

            self.course = self.canvas.get_course(1)
            self.assignment = self.course.get_assignment(1)

    # create_override()
    def test_create_override(self, m):
        register_uris({"assignment": ["create_override"]}, m)

        override = self.assignment.create_override(
            assignment_override={
                "student_ids": [1, 2, 3],
                "title": "New Assignment Override",
            }
        )

        self.assertIsInstance(override, AssignmentOverride)
        self.assertEqual(override.title, "New Assignment Override")

    # delete()
    def test_delete_assignments(self, m):
        register_uris({"assignment": ["delete_assignment"]}, m)

        deleted_assignment = self.assignment.delete()

        self.assertIsInstance(deleted_assignment, Assignment)

    # edit()
    def test_edit_assignment(self, m):
        register_uris({"assignment": ["edit_assignment"]}, m)

        name = "New Name"
        edited_assignment = self.assignment.edit(assignment={"name": name})

        self.assertIsInstance(edited_assignment, Assignment)
        self.assertTrue(hasattr(edited_assignment, "name"))
        self.assertEqual(edited_assignment.name, name)

    # get_gradeable_students()
    def test_get_gradeable_students(self, m):
        register_uris({"course": ["list_gradeable_students"]}, m)

        students = self.assignment.get_gradeable_students()
        student_list = [student for student in students]

        self.assertEqual(len(student_list), 2)
        self.assertIsInstance(student_list[0], UserDisplay)

    # get_override()
    def test_get_override(self, m):
        register_uris({"assignment": ["get_assignment_override"]}, m)

        override = self.assignment.get_override(1)

        self.assertIsInstance(override, AssignmentOverride)

    # get_overrides()
    def test_get_overrides(self, m):
        register_uris(
            {
                "assignment": [
                    "list_assignment_overrides",
                    "list_assignment_overrides_p2",
                ]
            },
            m,
        )

        overrides = self.assignment.get_overrides()
        override_list = [override for override in overrides]

        self.assertEqual(len(override_list), 4)
        self.assertIsInstance(override_list[0], AssignmentOverride)
        self.assertIsInstance(override_list[3], AssignmentOverride)

    # get_peer_reviews()
    def test_get_peer_reviews(self, m):
        register_uris({"assignment": ["list_peer_reviews"]}, m)

        peer_reviews = self.assignment.get_peer_reviews()
        peer_review_list = [peer_review for peer_review in peer_reviews]

        self.assertEqual(len(peer_review_list), 2)
        self.assertIsInstance(peer_review_list[0], PeerReview)

    # get_submission()
    def test_get_submission(self, m):
        register_uris({"submission": ["get_by_id_course"], "user": ["get_by_id"]}, m)

        user_id = 1
        submission_by_id = self.assignment.get_submission(user_id)
        self.assertIsInstance(submission_by_id, Submission)
        self.assertTrue(hasattr(submission_by_id, "submission_type"))

        user = self.canvas.get_user(user_id)
        submission_by_obj = self.assignment.get_submission(user)
        self.assertIsInstance(submission_by_obj, Submission)
        self.assertTrue(hasattr(submission_by_obj, "submission_type"))

    # get_submissions()
    def test_get_submissions(self, m):
        register_uris({"submission": ["list_submissions"]}, m)

        submissions = self.assignment.get_submissions()
        submission_list_by_id = [submission for submission in submissions]

        self.assertEqual(len(submission_list_by_id), 2)
        self.assertIsInstance(submission_list_by_id[0], Submission)

    # submit()
    def test_submit(self, m):
        register_uris({"assignment": ["submit"]}, m)

        sub_type = "online_upload"
        sub_dict = {"submission_type": sub_type}
        submission = self.assignment.submit(sub_dict)

        self.assertIsInstance(submission, Submission)
        self.assertTrue(hasattr(submission, "submission_type"))
        self.assertEqual(submission.submission_type, sub_type)

    def test_submit_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.assignment.submit({})

    def test_submit_file(self, m):
        register_uris({"assignment": ["submit", "upload", "upload_final"]}, m)

        filename = "testfile_assignment_{}".format(uuid.uuid4().hex)

        try:
            with open(filename, "w+") as file:
                sub_type = "online_upload"
                sub_dict = {"submission_type": sub_type}
                submission = self.assignment.submit(sub_dict, file)

            self.assertIsInstance(submission, Submission)
            self.assertTrue(hasattr(submission, "submission_type"))
            self.assertEqual(submission.submission_type, sub_type)

        finally:
            cleanup_file(filename)

    def test_submit_file_wrong_type(self, m):
        filename = "testfile_assignment_{}".format(uuid.uuid4().hex)
        sub_type = "online_text_entry"
        sub_dict = {"submission_type": sub_type}

        with self.assertRaises(ValueError):
            self.assignment.submit(sub_dict, filename)

    def test_submit_file_upload_failure(self, m):
        register_uris({"assignment": ["submit", "upload", "upload_fail"]}, m)

        filename = "testfile_assignment_{}".format(uuid.uuid4().hex)

        try:
            with open(filename, "w+") as file:
                sub_type = "online_upload"
                sub_dict = {"submission_type": sub_type}
                with self.assertRaises(CanvasException):
                    self.assignment.submit(sub_dict, file)
        finally:
            cleanup_file(filename)

    # __str__()
    def test__str__(self, m):
        string = str(self.assignment)
        self.assertIsInstance(string, str)

    # submissions_bulk_update()
    def test_submissions_bulk_update(self, m):
        register_uris({"assignment": ["update_submissions"]}, m)
        register_uris({"progress": ["course_progress"]}, m)
        progress = self.assignment.submissions_bulk_update(
            grade_data={"1": {"posted_grade": 97}, "2": {"posted_grade": 98}}
        )
        self.assertIsInstance(progress, Progress)
        self.assertTrue(progress.context_type == "Course")
        progress = progress.query()
        self.assertTrue(progress.context_type == "Course")

    # upload_to_submission()
    def test_upload_to_submission_self(self, m):
        register_uris({"assignment": ["upload", "upload_final"]}, m)

        filename = "testfile_assignment_{}".format(uuid.uuid4().hex)

        try:
            with open(filename, "w+") as file:
                response = self.assignment.upload_to_submission(file)

            self.assertTrue(response[0])
            self.assertIsInstance(response[1], dict)
            self.assertIn("url", response[1])
        finally:
            cleanup_file(filename)

    def test_upload_to_submission_user(self, m):
        register_uris({"assignment": ["upload_by_id", "upload_final"]}, m)

        filename = "testfile_assignment_{}".format(uuid.uuid4().hex)

        user_id = 1

        try:
            with open(filename, "w+") as file:
                response = self.assignment.upload_to_submission(file, user_id)

            self.assertTrue(response[0])
            self.assertIsInstance(response[1], dict)
            self.assertIn("url", response[1])
        finally:
            cleanup_file(filename)


@requests_mock.Mocker()
class TestAssignmentGroup(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {"course": ["get_by_id"], "assignment": ["get_assignment_group"]}, m
            )

            self.course = self.canvas.get_course(1)
            self.assignment_group = self.course.get_assignment_group(5)

    # edit()
    def test_edit_assignment_group(self, m):
        register_uris({"assignment": ["edit_assignment_group"]}, m)

        name = "New Name"
        edited_assignment_group = self.assignment_group.edit(
            assignment_group={"name": name}
        )

        self.assertIsInstance(edited_assignment_group, AssignmentGroup)
        self.assertTrue(hasattr(edited_assignment_group, "name"))
        self.assertEqual(edited_assignment_group.name, name)

    # delete()
    def test_delete_assignment_group(self, m):
        register_uris({"assignment": ["delete_assignment_group"]}, m)

        deleted_assignment_group = self.assignment_group.delete()

        self.assertIsInstance(deleted_assignment_group, AssignmentGroup)
        self.assertTrue(hasattr(deleted_assignment_group, "name"))
        self.assertEqual(deleted_assignment_group.name, "Assignment Group 5")

    # __str__()
    def test__str__(self, m):
        string = str(self.assignment_group)
        self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestAssignmentOverride(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    "course": ["get_by_id", "get_assignment_by_id"],
                    "assignment": ["get_assignment_override"],
                },
                m,
            )

            self.course = self.canvas.get_course(1)
            self.assignment = self.course.get_assignment(1)
            self.assignment_override = self.assignment.get_override(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.assignment_override)
        self.assertIsInstance(string, str)
        self.assertEqual(string, "Assignment Override 1 (1)")

    # delete()
    def test_delete(self, m):
        register_uris({"assignment": ["delete_override"]}, m)

        deleted = self.assignment_override.delete()
        self.assertIsInstance(deleted, AssignmentOverride)
        self.assertEqual(deleted.id, self.assignment_override.id)

    # edit()
    def test_edit(self, m):
        register_uris({"assignment": ["edit_override"]}, m)

        edited = self.assignment_override.edit(
            assignment_override={
                "title": "New Title",
                "student_ids": self.assignment_override.student_ids,
            }
        )

        self.assertEqual(edited, self.assignment_override)
        self.assertIsInstance(self.assignment_override, AssignmentOverride)
        self.assertEqual(edited.title, "New Title")
