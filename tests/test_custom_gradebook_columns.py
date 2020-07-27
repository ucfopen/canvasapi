import unittest
from urllib.parse import quote

import requests
import requests_mock

from canvasapi import Canvas
from canvasapi.custom_gradebook_columns import ColumnData
from canvasapi.paginated_list import PaginatedList
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestCustomGradebookColumn(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"course": ["get_by_id", "get_custom_columns"]}, m)

            self.course = self.canvas.get_course(1)
            self.gradebook_column = self.course.get_custom_columns()[1]

    # __str__()
    def test__str__(self, m):
        string = str(self.gradebook_column)
        self.assertIsInstance(string, str)

    # delete()
    def test_delete(self, m):
        register_uris({"custom_gradebook_columns": ["delete"]}, m)

        success = self.gradebook_column.delete()
        self.assertTrue(success)

    # get_column_entries()
    def test_get_column_entries(self, m):
        register_uris({"custom_gradebook_columns": ["get_column_entries"]}, m)

        column_entries = self.gradebook_column.get_column_entries()

        self.assertIsInstance(column_entries, PaginatedList)
        self.assertIsInstance(column_entries[0], ColumnData)
        self.assertTrue(hasattr(column_entries[0], "gradebook_column_id"))
        self.assertEqual(
            column_entries[0].gradebook_column_id, self.gradebook_column.id
        )

    # reorder_custom_columns()
    def test_reorder_custom_columns(self, m):
        def custom_matcher(request):
            match_text = "1,2,3"
            if request.text == "order={}".format(quote(match_text)):
                resp = requests.Response()
                resp._content = b'{"reorder": true, "order": [1, 2, 3]}'
                resp.status_code = 200
                return resp

        m.add_matcher(custom_matcher)

        order = [1, 2, 3]
        columns = self.gradebook_column.reorder_custom_columns(order=order)
        self.assertTrue(columns)

    def test_reorder_custom_columns_tuple(self, m):
        register_uris({"custom_gradebook_columns": ["reorder_custom_columns"]}, m)

        order = (1, 2, 3)
        columns = self.gradebook_column.reorder_custom_columns(order=order)
        self.assertTrue(columns)

    def test_reorder_custom_columns_comma_separated_string(self, m):
        register_uris({"custom_gradebook_columns": ["reorder_custom_columns"]}, m)

        order = "1,2,3"
        gradebook = self.gradebook_column.reorder_custom_columns(order=order)
        self.assertTrue(gradebook)

    def test_reorder_custom_columns_invalid_input(self, m):
        order = "invalid string"
        with self.assertRaises(ValueError):
            self.gradebook_column.reorder_custom_columns(order=order)

    # update_custom_column()
    def test_update_custom_column(self, m):
        register_uris({"custom_gradebook_columns": ["update_custom_column"]}, m)

        new_title = "Example title"
        self.gradebook_column.update_custom_column(column={"title": new_title})
        self.assertEqual(self.gradebook_column.title, new_title)


@requests_mock.Mocker()
class TestColumnData(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "course": ["get_by_id", "get_custom_columns"],
                "custom_gradebook_columns": ["get_column_entries"],
            }
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.gradebook_column = self.course.get_custom_columns()[1]
            self.data = self.gradebook_column.get_column_entries()[1]

    # __str__()
    def test__str__(self, m):
        string = str(self.data)
        self.assertIsInstance(string, str)

    # update_column_data()
    def test_update_column_data(self, m):
        register_uris({"custom_gradebook_columns": ["update_column_data"]}, m)

        new_content = "Updated content"
        self.data.update_column_data(column_data={"content": new_content})
        self.assertEqual(self.data.content, new_content)
