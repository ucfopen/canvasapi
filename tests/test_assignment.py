import unittest
import uuid
from pathlib import Path

import requests_mock

from canvasapi import Canvas
from canvasapi.assignment import (
    Assignment,
    AssignmentExtension,
    AssignmentGroup,
    AssignmentOverride,
)
from canvasapi.exceptions import CanvasException, RequiredFieldMissing
from canvasapi.grade_change_log import GradeChangeEvent
from canvasapi.paginated_list import PaginatedList
from canvasapi.peer_review import PeerReview
from canvasapi.progress import Progress
from canvasapi.submission import Submission
from canvasapi.user import User, UserDisplay
from tests import settings
from tests.util import cleanup_file, register_uris


@requests_mock.Mocker()
class TestAssignment(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"course": ["get_by_id", "get_assignment_by_id"]}, m)

            self.course = self.canvas.get_course(1)
            self.assignment = self.course.get_assignment(1)

    def test__init__overrides(self, m):
        register_uris({"assignment": ["get_assignment_with_overrides"]}, m)

        assignment = self.course.get_assignment(1)

        self.assertTrue(hasattr(assignment, "overrides"))
        self.assertIsInstance(assignment.overrides, list)
        self.assertEqual(len(assignment.overrides), 1)
        self.assertIsInstance(assignment.overrides[0], AssignmentOverride)

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

    # get_grade_change_events()
    def test_get_grade_change_events(self, m):
        register_uris({"assignment": ["get_grade_change_events"]}, m)

        response = self.assignment.get_grade_change_events()

        self.assertIsInstance(response, PaginatedList)
        self.assertEqual(len([event for event in response]), 2)

        for event in response:
            self.assertEqual(event.links["course"], self.assignment.id)
            self.assertIsInstance(event, GradeChangeEvent)
            self.assertEqual(event.event_type, "grade_change")

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

    # get_students_selected_for_moderation()
    def test_get_students_selected_for_moderation(self, m):
        register_uris({"assignment": ["get_students_selected_moderation"]}, m)

        selected_students = self.assignment.get_students_selected_for_moderation()
        selected_student_list = list(selected_students)

        self.assertEqual(len(selected_student_list), 2)
        self.assertIsInstance(selected_student_list[0], User)

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

    # set_extensions()
    def test_set_extensions(self, m):
        register_uris({"assignment": ["set_extensions"]}, m)

        extension = self.assignment.set_extensions(
            [{"user_id": 3, "extra_attempts": 2}, {"user_id": 2, "extra_attempts": 2}]
        )

        self.assertIsInstance(extension, list)
        self.assertEqual(len(extension), 2)

        self.assertIsInstance(extension[0], AssignmentExtension)
        self.assertEqual(extension[0].user_id, 3)
        self.assertTrue(hasattr(extension[0], "extra_attempts"))
        self.assertEqual(extension[0].extra_attempts, 2)

        self.assertIsInstance(extension[1], AssignmentExtension)
        self.assertEqual(extension[1].user_id, 2)
        self.assertTrue(hasattr(extension[1], "extra_attempts"))
        self.assertEqual(extension[1].extra_attempts, 2)

    def test_set_extensions_not_list(self, m):
        with self.assertRaises(ValueError):
            self.assignment.set_extensions({"user_id": 3, "exrra_attempts": 2})

    def test_set_extensions_empty_list(self, m):
        with self.assertRaises(ValueError):
            self.assignment.set_extensions([])

    def test_set_extensions_non_dicts(self, m):
        with self.assertRaises(ValueError):
            self.assignment.set_extensions([("user_id", 1), ("extra_attempts", 2)])

    def test_set_extensions_missing_key(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.assignment.set_extensions([{"extra_attempts": 3}])

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

    def test_submit_file_pathlib(self, m):
        register_uris({"assignment": ["submit", "upload", "upload_final"]}, m)

        filename = Path("testfile_assignment_{}".format(uuid.uuid4().hex))
        filename.write_bytes(b"test data")

        try:
            sub_type = "online_upload"
            sub_dict = {"submission_type": sub_type}
            submission = self.assignment.submit(sub_dict, filename)

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

    # get_provisional_grades_status
    def test_get_provisional_grades_status(self, m):
        register_uris(
            {"assignment": ["get_provisional_grades_status"], "user": ["get_by_id"]}, m
        )
        student_id = 1
        user = self.canvas.get_user(student_id)
        status = self.assignment.get_provisional_grades_status(user)
        self.assertIsInstance(status, bool)
        self.assertFalse(status)

    # select_students_for_moderation()
    def test_select_students_for_moderation(self, m):
        register_uris({"assignment": ["select_students_for_moderation"]}, m)

        selected_students = self.assignment.select_students_for_moderation(
            student_ids=[11, 12]
        )
        selected_student_list = list(selected_students)

        self.assertEqual(len(selected_student_list), 2)
        self.assertIsInstance(selected_student_list[0], User)

    # selected_provisional_grade
    def test_selected_provisional_grade(self, m):
        register_uris({"assignment": ["selected_provisional_grade"]}, m)
        provisional_grade_id = 1
        selected_provisional_grade = self.assignment.selected_provisional_grade(
            provisional_grade_id
        )
        self.assertIsInstance(selected_provisional_grade, dict)
        self.assertIn("assignment_id", selected_provisional_grade)

    # publish_provisional_grades
    def test_publish_provisional_grades(self, m):
        register_uris({"assignment": ["publish_provisional_grades"]}, m)
        publish = self.assignment.publish_provisional_grades()
        self.assertIsInstance(publish, dict)
        self.assertIn("message", publish)

    # show_provisional_grades_for_student
    def test_show_provisonal_grades_for_student(self, m):
        register_uris(
            {
                "assignment": ["show_provisonal_grades_for_student"],
                "user": ["get_by_id"],
            },
            m,
        )
        anonymous_id = 1
        user = self.canvas.get_user(anonymous_id)
        show_status = self.assignment.show_provisonal_grades_for_student(user)

        self.assertIsInstance(show_status, bool)
        self.assertFalse(show_status)


@requests_mock.Mocker()
class TestAssignmentExtension(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        self.extension = AssignmentExtension(
            self.canvas._Canvas__requester,
            {"assignment_id": 2, "user_id": 3, "extra_attempts": 2},
        )

    # __str__()
    def test__str__(self, m):
        string = str(self.extension)
        self.assertIsInstance(string, str)


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
