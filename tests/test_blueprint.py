import unittest

import requests_mock

from canvasapi import Canvas
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestBlueprint(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                'course': ['get_blueprint', 'get_by_id']
            }
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.blueprint = self.course.get_blueprint(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.blueprint)
        self.assertIsInstance(string, str)
