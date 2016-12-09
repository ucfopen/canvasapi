import unittest

import requests_mock

import settings
from pycanvas.canvas import Canvas
from pycanvas.course import Course
from pycanvas.group import Group, GroupCategory
from pycanvas.progress import Progress
from util import register_uris


class TestProgress(unittest.TestCase):
    """
    Tests Progress functionality.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'generic': ['not_found'],
            'course': ['get_by_id', 'create_group_category'],
            'group': ['category_create_group', 'category_assign_members_false'],
            'progress': ['progress_query']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)
        self.group_category = self.course.create_group_category("Shia Laboef")

        self.progress = self.group_category.assign_members()

    # __str__()
    def test__str__(self):
        string = str(self.progress)
        assert isinstance(string, str)

    # query()
    def test_query(self):
        response = self.progress.query()
        assert isinstance(response, Progress)
