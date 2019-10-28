from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.grade_change_event import GradeChangeEvent
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestCommMessage(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"course": ["get_grade_change_log", "get_by_id"]}
            register_uris(requires, m)

            course = self.canvas.get_course(1)
            grade_change_log = course.get_grade_change_log()
            self.grade_change_event = grade_change_log[0]

    # __str__()
    def test__str__(self, m):
        self.assertIsInstance(self.grade_change_event, GradeChangeEvent)
        self.assertIsInstance(str(self.grade_change_event), str)
