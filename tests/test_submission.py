from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import uuid
import warnings

import requests_mock

from canvasapi import Canvas
from canvasapi.submission import Submission
from tests import settings
from tests.util import cleanup_file, register_uris


@requests_mock.Mocker()
class TestSubmission(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({
                'course': ['get_by_id', 'get_assignment_by_id'],
                'section': ['get_by_id'],
                'submission': ['get_by_id_course', 'get_by_id_section']
            }, m)

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

    # edit()
    def test_edit(self, m):
        register_uris({
            'submission': ['edit']
        }, m)

        self.assertFalse(hasattr(self.submission_course, 'excused'))

        self.submission_course.edit(submission={'excuse': True})

        self.assertIsInstance(self.submission_course, Submission)
        self.assertTrue(hasattr(self.submission_course, 'excused'))
        self.assertTrue(self.submission_course.excused)

    # upload_comment()
    def test_upload_comment(self, m):
        register_uris({'submission': [
            'upload_comment',
            'upload_comment_final',
            'edit',
        ]}, m)

        filename = 'testfile_submission_{}'.format(uuid.uuid4().hex)

        try:
            with open(filename, 'w+') as file:
                response = self.submission_course.upload_comment(file)

            self.assertTrue(response[0])
            self.assertIsInstance(response[1], dict)
            self.assertIn('url', response[1])
        finally:
            cleanup_file(filename)

    def test_upload_comment_section(self, m):
        register_uris({'submission': [
            'upload_comment',
            'upload_comment_final',
            'edit',
        ]}, m)

        filename = 'testfile_submission_{}'.format(uuid.uuid4().hex)

        try:
            with open(filename, 'w+') as file:
                response = self.submission_section.upload_comment(file)

            self.assertTrue(response[0])
            self.assertIsInstance(response[1], dict)
            self.assertIn('url', response[1])
        finally:
            cleanup_file(filename)
