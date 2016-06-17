import unittest

import requests_mock

import settings
from util import register_uris
from pycanvas import Canvas


class TestExternalTool(unittest.TestCase):
    """
    Tests Courses functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': ['get_by_id'],
            'external_tool': ['get_by_id_course'],
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)
        self.ext_tool = self.course.get_external_tool(1)

    # __str__()
    def test__str__(self):
        string = str(self.ext_tool)
        assert isinstance(string, str)
