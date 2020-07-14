import unittest
from canvasapi import Canvas

@requests_mock.Mocker()
class TestCustomGradebookColumn(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

    # __str__()
    def test__str__(self, m):
        pass

    # update_custom_column()
    def test_update_custom_column(self, m):
        pass


    # get_column_entries()
    def get_column_entries(self, m):
        pass

    # delete()
    def delete(self, m):
        pass

    # reorder_custom_columns()
    def reorder_custom_columns(self, m):
        pass

@requests_mock.Mocker()
class TestColumnData(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

    # __str__()
    def test__str__(self, m):
        pass

    # update_column_data()
    def test_update_column_data(self, m):
        pass