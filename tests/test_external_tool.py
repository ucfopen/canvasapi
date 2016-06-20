import unittest

import requests_mock

import settings
from util import register_uris
from pycanvas import Canvas
from pycanvas.account import Account
from pycanvas.course import Course
from pycanvas.exceptions import CanvasException
from pycanvas.external_tool import ExternalTool


class TestExternalTool(unittest.TestCase):
    """
    Tests Courses functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'account': ['get_by_id'],
            'course': ['get_by_id', 'get_by_id_2'],
            'external_tool': [
                'get_by_id_account', 'get_by_id_course', 'get_by_id_course_2',
                'get_sessionless_launch_url_course', 'sessionless_launch_no_url'
            ],
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)
        self.account = self.canvas.get_account(1)
        self.ext_tool_course = self.course.get_external_tool(1)
        self.ext_tool_account = self.account.get_external_tool(1)

    # __str__()
    def test__str__(self):
        string = str(self.ext_tool_course)
        assert isinstance(string, str)

    # parent_id
    def test_parent_id_account(self):
        assert self.ext_tool_account.parent_id == 1

    def test_parent_id_course(self):
        assert self.ext_tool_course.parent_id == 1

    def test_parent_id_no_id(self):
        tool = ExternalTool(self.canvas._Canvas__requester, {'id': 1})
        with self.assertRaises(ValueError):
            tool.parent_id

    # parent_type
    def test_parent_type_account(self):
        assert self.ext_tool_account.parent_type == 'account'

    def test_parent_type_course(self):
        assert self.ext_tool_course.parent_type == 'course'

    def test_parent_type_no_id(self):
        tool = ExternalTool(self.canvas._Canvas__requester, {'id': 1})
        with self.assertRaises(ValueError):
            tool.parent_type

    # get_parent()
    def test_get_parent_account(self):
        assert isinstance(self.ext_tool_account.get_parent(), Account)

    def test_get_parent_course(self):
        assert isinstance(self.ext_tool_course.get_parent(), Course)

    # get_sessionless_launch_url()
    def test_get_sessionless_launch_url(self):
        assert isinstance(self.ext_tool_course.get_sessionless_launch_url(), (str, unicode))

    def test_get_sessionless_launch_url_no_url(self):
        course = self.canvas.get_course(2)
        ext_tool = course.get_external_tool(2)
        with self.assertRaises(CanvasException):
            ext_tool.get_sessionless_launch_url()
