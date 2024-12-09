import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestLTIResourceLink(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {
                    "course": ["get_by_id"],
                    "lti_resource_link": ["get_lti_resource_link"],
                },
                m,
            )

            self.course = self.canvas.get_course(1)
            self.resource_link = self.course.get_lti_resource_link(45)

    # __str__()
    def test__str__(self, m):
        string = str(self.resource_link)
        self.assertIsInstance(string, str)
