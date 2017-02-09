import unittest

import requests_mock

from pycanvas import Canvas
from pycanvas.account import Account
from pycanvas.course import Course
from pycanvas.exceptions import CanvasException
from pycanvas.external_tool import ExternalTool
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestExternalTool(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                'account': ['get_by_id'],
                'course': ['get_by_id'],
                'external_tool': ['get_by_id_account', 'get_by_id_course'],
            }
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.account = self.canvas.get_account(1)
            self.ext_tool_course = self.course.get_external_tool(1)
            self.ext_tool_account = self.account.get_external_tool(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.ext_tool_course)
        assert isinstance(string, str)

    # parent_id
    def test_parent_id_account(self, m):
        assert self.ext_tool_account.parent_id == 1

    def test_parent_id_course(self, m):
        assert self.ext_tool_course.parent_id == 1

    def test_parent_id_no_id(self, m):
        tool = ExternalTool(self.canvas._Canvas__requester, {'id': 1})
        with self.assertRaises(ValueError):
            tool.parent_id

    # parent_type
    def test_parent_type_account(self, m):
        assert self.ext_tool_account.parent_type == 'account'

    def test_parent_type_course(self, m):
        assert self.ext_tool_course.parent_type == 'course'

    def test_parent_type_no_id(self, m):
        tool = ExternalTool(self.canvas._Canvas__requester, {'id': 1})
        with self.assertRaises(ValueError):
            tool.parent_type

    # get_parent()
    def test_get_parent_account(self, m):
        register_uris({'account': ['get_by_id']}, m)
        assert isinstance(self.ext_tool_account.get_parent(), Account)

    def test_get_parent_course(self, m):
        register_uris({'course': ['get_by_id']}, m)
        assert isinstance(self.ext_tool_course.get_parent(), Course)

    # delete()
    def test_delete(self, m):
        register_uris({'external_tool': ['delete_tool_course']}, m)
        deleted_tool = self.ext_tool_course.delete()

        self.assertIsInstance(deleted_tool, ExternalTool)
        self.assertTrue(hasattr(deleted_tool, 'name'))

    # edit()
    def test_edit(self, m):
        register_uris({'external_tool': ['edit_tool_course']}, m)
        new_name = "New Tool Name"

        edited_tool = self.ext_tool_course.edit(name=new_name)

        self.assertEqual(self.ext_tool_course.name, new_name)
        self.assertIsInstance(edited_tool, ExternalTool)
        self.assertEqual(edited_tool.name, new_name)

    # get_sessionless_launch_url()
    def test_get_sessionless_launch_url(self, m):
        requires = {'external_tool': ['get_sessionless_launch_url_course']}
        register_uris(requires, m)

        assert isinstance(self.ext_tool_course.get_sessionless_launch_url(), (str, unicode))

    def test_get_sessionless_launch_url_no_url(self, m):
        requires = {
            'course': ['get_by_id_2'],
            'external_tool': [
                'get_by_id_course_2', 'sessionless_launch_no_url'
            ]
        }
        register_uris(requires, m)

        course = self.canvas.get_course(2)
        ext_tool = course.get_external_tool(2)
        with self.assertRaises(CanvasException):
            ext_tool.get_sessionless_launch_url()
