import unittest
import requests

import requests_mock

import settings
from util import register_uris
from pycanvas import Canvas
from pycanvas.course import Course, CourseNickname, Page


class TestGroup(unittest.TestCase):
    """
    Tests Group functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': ['get_by_id', 'show_front_page'],
            'generic': ['not_found'],
            'group': ['show_front_page', 'get_single_group']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)
        self.group = self.canvas.get_single_group(1)

    #show_front_page()
    def test_show_front_page(self):
        front_page = self.group.show_front_page()

        assert isinstance(front_page, Page)
        assert hasattr(front_page, 'url')
        assert hasattr(front_page, 'title')
