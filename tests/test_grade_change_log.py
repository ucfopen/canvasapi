import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestGradeChangeEvent(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"course": ["get_by_id"]}
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)

    # __str__()
    def test__str__(self, m):
        requires = {"course": ["get_grade_change_events"]}
        register_uris(requires, m)

        for event in self.course.get_grade_change_events():
            self.assertIsInstance(str(event), str)
