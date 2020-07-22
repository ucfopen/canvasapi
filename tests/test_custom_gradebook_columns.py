import unittest

import requests
import requests_mock

from canvasapi import Canvas
from canvasapi.course import Course
from canvasapi.custom_gradebook_columns import CustomGradebookColumn, ColumnData
from canvasapi.paginated_list import PaginatedList
from canvasapi.user import User
from tests import settings
from tests.util import register_uris

@requests_mock.Mocker()
class TestCustomGradebookColumn(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"course": ["get_by_id", "get_custom_columns"]}, m)

            self.course = self.canvas.get_course(1)
            self.custom_gradebook_columns = self.course.get_custom_columns()

    # __str__() 
    def test__str__(self, m):
        string = str(self.custom_gradebook_columns)
        self.assertIsInstance(string, str)

    # delete() 
    def test_delete(self, m):
        register_uris({"custom_gradebook_columns": ["delete"]}, m)

        success = self.custom_gradebook_columns.delete()
        self.assertTrue(success)

    # get_column_entries() - paginated 
    def test_get_column_entries(self, m):
        register_uris({"custom_gradebook_columns": ["get_column_entries"]}, m)
        
        column_entries = self.custom_gradebook_columns.get_column_entries()
        self.assertIsInstance(column_entries, PaginatedList)
        self.assertIsInstance(column_entries[0], ColumnData)

    # reorder_custom_columns() - done?
    def test_reorder_custom_columns(self, m):
        def custom_matcher(request):
            match_test = "1,2,3"
            if request.text == "order={}".format(quote(match_text)):
                resp = requests.Response()
                resp._content = b'{"reorder": true, "order": [1, 2, 3]}'
                resp.status_code = 200
                return resp
        m.add_matcher(custom_matcher)

        order = [1, 2, 3]
        columns = self.custom_gradebook_columns.reorder_custom_columns(order=order)
        self.assertTrue(columns) 

    def test_reorder_custom_columns_tuple(self, m):
        register_uris({"custom_gradebook_columns": ["reorder_custom_columns"]}, m)

        order = (1, 2, 3)
        columns = self.custom_gradebook_columns.reorder_custom_columns(order=order)
        self.assertTrue(columns)
    
    def test_reorder_custom_columns_comma_separated_string(self, m):
        register_uris({"custom_gradebook_columns": ["reorder_custom_columns"]}, m)

        order = "1,2,3"
        gradebook = self.custom_gradebook_columns.reorder_custom_columns(order=order)
        self.assertTrue(gradebook)

    def test_reorder_custom_columns_invalid_input(self, m):
        order = "invalid string"
        with self.assertRaises(ValueError):
            self.custom_gradebook_columns.reorder_custom_columns(order=order)

    # update_custom_column() - not sure
    def test_update_custom_column(self, m):
        register_uris({"custom_gradebook_columns": ["update_custom_column"]}, m)

        new_title = "Example title"
        self.custom_gradebook_columns.update_custom_column(column={"title": new_title})
        self.assertEqual(self.custom_gradebook_columns.title, new_title)

"""
@requests_mock.Mocker()
class TestColumnData(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires_uris = ({"custom_gradebook_columns": ["get_custom_columns"]}, m)
            self.content.get_column_entries(1) # course - not sure what to put there

    # __str__()
    def test__str__(self, m):
        string = str(self.content)
        self.assertIsInstance(string, str)

    # update_column_data() - done?
    def test_update_column_data(self, m):
        register_uris({"custom_gradebook_columns": ["update_column_data"]}, m)

        new_content = "Updated content"
        self.custom_gradebook_columns.update_column_data(column_data={"content": new_content})
        self.assertEqual(self.custom_gradebook_columns.content, new_content)
"""