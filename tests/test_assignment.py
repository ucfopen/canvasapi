from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.assignment import Assignment, AssignmentGroup
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.submission import Submission
from canvasapi.user import UserDisplay
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestAssignment(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'course': ['get_by_id', 'get_assignment_by_id']}, m)

            self.course = self.canvas.get_course(1)
            self.assignment = self.course.get_assignment(1)

    # delete()
    def test_delete_assignments(self, m):
        register_uris({'assignment': ['delete_assignment']}, m)

        deleted_assignment = self.assignment.delete()

        self.assertIsInstance(deleted_assignment, Assignment)

    # edit()
    def test_edit_assignment(self, m):
        register_uris({'assignment': ['edit_assignment']}, m)

        name = 'New Name'
        edited_assignment = self.assignment.edit(assignment={'name': name})

        self.assertIsInstance(edited_assignment, Assignment)
        self.assertTrue(hasattr(edited_assignment, 'name'))
        self.assertEqual(edited_assignment.name, name)

    # get_gradeable_students()
    def test_get_gradeable_students(self, m):
        register_uris({'course': ['list_gradeable_students']}, m)

        students = self.assignment.get_gradeable_students()
        student_list = [student for student in students]

        self.assertEqual(len(student_list), 2)
        self.assertIsInstance(student_list[0], UserDisplay)

    # get_submission()
    def test_get_submission(self, m):
        register_uris({
            'submission': ['get_by_id_course'],
            'user': ['get_by_id']
        }, m)

        user_id = 1
        submission_by_id = self.assignment.get_submission(user_id)
        self.assertIsInstance(submission_by_id, Submission)
        self.assertTrue(hasattr(submission_by_id, 'submission_type'))

        user = self.canvas.get_user(user_id)
        submission_by_obj = self.assignment.get_submission(user)
        self.assertIsInstance(submission_by_obj, Submission)
        self.assertTrue(hasattr(submission_by_obj, 'submission_type'))

    # get_submissions()
    def test_get_submissions(self, m):
        register_uris({'submission': ['list_submissions']}, m)

        submissions = self.assignment.get_submissions()
        submission_list_by_id = [submission for submission in submissions]

        self.assertEqual(len(submission_list_by_id), 2)
        self.assertIsInstance(submission_list_by_id[0], Submission)

    # submit()
    def test_submit(self, m):
        register_uris({'assignment': ['submit']}, m)

        sub_type = "online_upload"
        sub_dict = {'submission_type': sub_type}
        submission = self.assignment.submit(sub_dict)

        self.assertIsInstance(submission, Submission)
        self.assertTrue(hasattr(submission, 'submission_type'))
        self.assertEqual(submission.submission_type, sub_type)

    def test_submit_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.assignment.submit({})

    # __str__()
    def test__str__(self, m):
        string = str(self.assignment)
        self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestAssignmentGroup(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({
                'course': ['get_by_id'],
                'assignment': ['get_assignment_group']
            }, m)

            self.course = self.canvas.get_course(1)
            self.assignment_group = self.course.get_assignment_group(5)

    # edit()
    def test_edit_assignment_group(self, m):
        register_uris({'assignment': ['edit_assignment_group']}, m)

        name = 'New Name'
        edited_assignment_group = self.assignment_group.edit(
            assignment_group={'name': name}
        )

        self.assertIsInstance(edited_assignment_group, AssignmentGroup)
        self.assertTrue(hasattr(edited_assignment_group, 'name'))
        self.assertEqual(edited_assignment_group.name, name)

    # delete()
    def test_delete_assignment_group(self, m):
        register_uris({'assignment': ['delete_assignment_group']}, m)

        deleted_assignment_group = self.assignment_group.delete()

        self.assertIsInstance(deleted_assignment_group, AssignmentGroup)
        self.assertTrue(hasattr(deleted_assignment_group, 'name'))
        self.assertEqual(deleted_assignment_group.name, 'Assignment Group 5')

    # __str__()
    def test__str__(self, m):
        string = str(self.assignment_group)
        self.assertIsInstance(string, str)
