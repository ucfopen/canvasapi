import unittest

import requests_mock

from canvasapi.canvas import Canvas
from canvasapi.progress import Progress
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestProgress(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "course": ["get_by_id", "create_group_category"],
                "group": ["category_assign_members_false"],
            }

            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.group_category = self.course.create_group_category("Test String")
            self.progress = self.group_category.assign_members()

    # __str__()
    def test__str__(self, m):
        string = str(self.progress)
        self.assertIsInstance(string, str)

    # query()
    def test_query(self, m):
        register_uris({"progress": ["progress_query"]}, m)

        response = self.progress.query()
        self.assertIsInstance(response, Progress)
