from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.outcome import Outcome
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestOutcome(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            # CHAMGE THIS ################
            register_uris({'course': ['get_by_id'], 'group': ['get_by_id']}, m)

            self.course = self.canvas.get_course(1)
            self.outcome = self.canvas.get_group(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.outcome)
        self.assertIsInstance(string, str)

    # show()
    def test_show(self, m):
        return

    # update()
    def test_update(self, m):
        register_uris({'group': ['edit']}, m)

        new_title = "New Outcome"
        response = self.outcome.update(title=new_title)
        self.assertIsInstance(response, Outcome)
        self.assertTrue(hasattr(response, 'title'))
        self.assertEqual(response.title, new_title)
