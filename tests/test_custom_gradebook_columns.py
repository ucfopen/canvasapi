"""
import unittest
from canvasapi import Canvas
from canvasapi.course import Course
from canvasapi.user import User
from tests.util import register_uris

@requests_mock.Mocker()
class TestCustomGradebookColumn(unittest.TestCase):
    def setUp(self):

        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"course": ["get_by_id"], "custom_gradebook_columns": [""]}
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.gradebook = self.course.get_custom_columns(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.gradebook)
        self.assertIsInstance(string, str)
        pass

    # delete()
    def test_delete(self, m):
        register_uris({"custom_gradebook_columns": ["delete"]}, m)

        success = self.gradebook.delete()
        self.assertTrue(success)
        pass

    # get_column_entries() - paginated
    def test_get_column_entries(self, m):
        register_uris(
            {"custom_gradebook_columns": ["get_column_entries, get_column_entries_p2"]}, m
        )
        columns = self.gradebook.get_column_entries()
        column_entries = [col for col in columns]
        self.assertEqual(len(column_entries), 4)
        self.assertIsInstance(column_entries[0], ColumnData)
        pass

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
        columns = self.gradebooks.reorder_custom_columns(order=order)
        self.assertTrue(columns) 

    def test_reorder_custom_columns_tuple(self, m):
        register_uris({"custom_gradebook_columns": ["reorder_custom_columns"]}, m)

        order = (1, 2, 3)
        columns = self.gradebooks.reorder_custom_columns(order=order)
        self.assertTrue(columns)
    
    def test_reorder_custom_columns_comma_separated_string(self, m):
        register_uris({"custom_gradebook_columns": ["reorder_custom_columns"]}, m)

        order = "1,2,3"
        gradebook = self.course.reorder_custom_columns(order=order)
        self.assertTrue(gradebook)

    def test_reorder_custom_columns_invalid_input(self, m):
        order = "invalid string"
        with self.assertRaises(ValueError):
            self.course.reorder_custom_columns(order=order)

    # update_custom_column()
    def test_update_custom_column(self, m):
        register_uris({"custom_gradebook_columns": ["update_custom_column"]}, m)

        update_column = self.gradebook.update_custom_column()
        pass

@requests_mock.Mocker()
class TestColumnData(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({}, m)

    # __str__()
    def test__str__(self, m):
        string = str(self.data)
        self.assertIsInstance(string, str)
        pass

    # update_column_data()
    def test_update_column_data(self, m):
        register_uris({"custom_gradebook_columns": ["update_column_data"]}, m)

        new_content = "New Content"
        self.gradebook.update_column_data()
        pass
"""
