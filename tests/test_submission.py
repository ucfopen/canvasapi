from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import uuid

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import cleanup_file, register_uris


@requests_mock.Mocker()
class TestSubmission(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({
                'course': ['get_by_id'],
                'section': ['get_by_id'],
                'submission': ['get_by_id_course', 'get_by_id_section']
            }, m)

            self.course = self.canvas.get_course(1)
            self.submission_course = self.course.get_submission(1, 1)
            self.section = self.canvas.get_section(1)
            self.submission_section = self.section.get_submission(1, 1)

    # __str__()
    def test__str__(self, m):
        string = str(self.submission_course)
        self.assertIsInstance(string, str)

    # upload_comment()
    def test_upload_comment(self, m):
        register_uris({'submission': [
            'upload_comment',
            'upload_comment_final',
            'update_submission',
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
        # Sections do not support uploading file comments
        with self.assertRaises(ValueError):
            self.submission_section.upload_comment('fakefilename.txt')
