from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.grading_period import GradingPeriod
from tests.util import register_uris
from tests import settings


@requests_mock.Mocker()
class TestGradingPeriod(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        self.grading_period = GradingPeriod(
            self.canvas._Canvas__requester,
            {"title": "grading period 1", "id": 1}
        )

    def test_str(self, m):

        test_str = str(self.grading_period)
        self.assertIsInstance(test_str, str)

    # update()
    def test_update(self, m):
        register_uris({'grading_period': ['update']}, m)

        edited_grading_period = self.grading_period.update(1, grading_period=[{'start_date': '2019-06-10T06:00:00Z', 'end_date': '2019-06-15T06:00:00Z'}])

        self.assertIsInstance(edited_grading_period, GradingPeriod)
        self.assertTrue(hasattr(edited_grading_period, 'title'))
        self.assertEqual(edited_grading_period.title, 'Grading period 1')
        self.assertTrue(hasattr(edited_grading_period, 'start_date'))
        self.assertTrue(hasattr(edited_grading_period, 'end_date'))
        self.assertEqual(edited_grading_period.start_date, '2019-05-23T06:00:00Z')
        self.assertEqual(edited_grading_period.end_date, '2019-08-23T06:00:00Z')

    # delete()
    def test_delete(self, m):
        register_uris({'grading_period': ['delete']}, m)
        self.assertTrue(self.grading_period.delete(1))