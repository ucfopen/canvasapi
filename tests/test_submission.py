import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestSubmission(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({
                'section': ['get_by_id', 'get_submission']
            }, m)

            self.section = self.canvas.get_section(1)
            self.submission = self.section.get_submission(1, 1)

    # __str__()
    def test__str__(self, m):
        string = str(self.submission)
        self.assertIsInstance(string, str)
