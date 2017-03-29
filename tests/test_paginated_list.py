import unittest

import requests_mock

from canvas_api import Canvas
from canvas_api.paginated_list import PaginatedList
from canvas_api.user import User
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestPaginatedList(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)
        self.requester = self.canvas._Canvas__requester

    # various length lists
    def test_paginated_list_empty(self, m):
        register_uris({'paginated_list': ['empty']}, m)

        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'empty_list'
        )
        item_list = [item for item in pag_list]
        self.assertEqual(len(item_list), 0)

    def test_paginated_list_single(self, m):
        register_uris({'paginated_list': ['single']}, m)

        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'single_item'
        )
        item_list = [item for item in pag_list]
        self.assertEqual(len(item_list), 1)
        self.assertIsInstance(item_list[0], User)

    def test_paginated_list_two_one_page(self, m):
        register_uris({'paginated_list': ['2_1_page']}, m)

        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'two_objects_one_page'
        )
        item_list = [item for item in pag_list]
        self.assertEqual(len(item_list), 2)
        self.assertIsInstance(item_list[0], User)

    def test_paginated_list_four_two_pages(self, m):
        register_uris({'paginated_list': ['4_2_pages_p1', '4_2_pages_p2']}, m)

        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'four_objects_two_pages'
        )
        item_list = [item for item in pag_list]
        self.assertEqual(len(item_list), 4)
        self.assertIsInstance(item_list[0], User)

    def test_paginated_list_six_three_pages(self, m):
        requires = {
            'paginated_list': ['6_3_pages_p1', '6_3_pages_p2', '6_3_pages_p3']
        }
        register_uris(requires, m)

        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        item_list = [item for item in pag_list]
        self.assertEqual(len(item_list), 6)
        self.assertIsInstance(item_list[0], User)

    # reusing iterator
    def test_iterator(self, m):
        requires = {
            'paginated_list': ['6_3_pages_p1', '6_3_pages_p2', '6_3_pages_p3']
        }
        register_uris(requires, m)

        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        list_1 = [item for item in pag_list]
        list_2 = [item for item in pag_list]
        self.assertEqual(cmp(list_1, list_2), 0)

    # get item
    def test_getitem_first(self, m):
        requires = {
            'paginated_list': ['6_3_pages_p1', '6_3_pages_p2', '6_3_pages_p3']
        }
        register_uris(requires, m)

        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        first_item = pag_list[0]
        self.assertIsInstance(first_item, User)

    def test_getitem_second_page(self, m):
        requires = {
            'paginated_list': ['6_3_pages_p1', '6_3_pages_p2', '6_3_pages_p3']
        }
        register_uris(requires, m)

        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        third_item = pag_list[2]
        self.assertIsInstance(third_item, User)

    # slicing
    def test_slice_beginning(self, m):
        requires = {
            'paginated_list': ['6_3_pages_p1', '6_3_pages_p2', '6_3_pages_p3']
        }
        register_uris(requires, m)

        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        first_two_items = pag_list[:2]
        item_list = [item for item in first_two_items]
        self.assertEqual(len(item_list), 2)
        self.assertIsInstance(item_list[0], User)
        self.assertTrue(hasattr(item_list[0], 'id'))
        self.assertEqual(item_list[0].id, '1')

    def test_slice_middle(self, m):
        requires = {
            'paginated_list': ['6_3_pages_p1', '6_3_pages_p2', '6_3_pages_p3']
        }
        register_uris(requires, m)

        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        middle_two_items = pag_list[2:4]
        item_list = [item for item in middle_two_items]
        self.assertEqual(len(item_list), 2)
        self.assertIsInstance(item_list[0], User)
        self.assertTrue(hasattr(item_list[0], 'id'))
        self.assertEqual(item_list[0].id, '3')

    def test_slice_end(self, m):
        requires = {
            'paginated_list': ['6_3_pages_p1', '6_3_pages_p2', '6_3_pages_p3']
        }
        register_uris(requires, m)

        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        middle_two_items = pag_list[4:6]
        item_list = [item for item in middle_two_items]
        self.assertEqual(len(item_list), 2)
        self.assertIsInstance(item_list[0], User)
        self.assertTrue(hasattr(item_list[0], 'id'))
        self.assertEqual(item_list[0].id, '5')

    # __repr__()
    def test_repr(self, m):
        requires = {
            'paginated_list': ['6_3_pages_p1', '6_3_pages_p2', '6_3_pages_p3']
        }
        register_uris(requires, m)

        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        self.assertEqual(pag_list.__repr__(), '<PaginatedList of type User>')
