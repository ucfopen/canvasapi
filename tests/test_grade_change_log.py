from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestGradeChangeLog(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"course": ["get_grade_change_log", "get_by_id"]}
            register_uris(requires, m)

            course = self.canvas.get_course(1)
            self.log = course.get_grade_change_log()

    # __str__()
    def test__str__(self, m):
        self.assertIsInstance(str(self.log), str)


@requests_mock.Mocker()
class TestGradeChangeEvent(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"course": ["get_grade_change_log", "get_by_id"]}
            register_uris(requires, m)

            course = self.canvas.get_course(1)
            self.events = course.get_grade_change_log().events

    # __str__()
    def test__str__(self, m):
        self.assertIsInstance(str(self.events[0]), str)
