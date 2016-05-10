import unittest

import requests_mock

import settings
from pycanvas import Canvas
from pycanvas.paginated_list import PaginatedList
from pycanvas.user import User
from util import register_uris


class TestPaginatedList(unittest.TestCase):
    """
    Tests PaginatedList functionality.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'paginated_list': [
                '2_1_page', '4_2_pages_p1', '4_2_pages_p2', '6_3_pages_p1',
                '6_3_pages_p2', '6_3_pages_p3', 'empty', 'single',
            ]
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        self.requester = self.canvas._Canvas__requester
        register_uris(settings.BASE_URL, requires, adapter)

    # various length lists
    def test_paginated_list_empty(self):
        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'empty_list'
        )
        item_list = [item for item in pag_list]
        assert len(item_list) == 0

    def test_paginated_list_single(self):
        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'single_item'
        )
        item_list = [item for item in pag_list]
        assert len(item_list) == 1
        assert isinstance(item_list[0], User)

    def test_paginated_list_two_one_page(self):
        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'two_objects_one_page'
        )
        item_list = [item for item in pag_list]
        assert len(item_list) == 2
        assert isinstance(item_list[0], User)

    def test_paginated_list_four_two_pages(self):
        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'four_objects_two_pages'
        )
        item_list = [item for item in pag_list]
        assert len(item_list) == 4
        assert isinstance(item_list[0], User)

    def test_paginated_list_six_three_pages(self):
        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        item_list = [item for item in pag_list]
        assert len(item_list) == 6
        assert isinstance(item_list[0], User)

    # reusing iterator
    def test_iterator(self):
        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        list_1 = [item for item in pag_list]
        list_2 = [item for item in pag_list]
        assert cmp(list_1, list_2) == 0

    # get item
    def test_getitem_first(self):
        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        first_item = pag_list[0]
        assert isinstance(first_item, User)

    def test_getitem_second_page(self):
        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        third_item = pag_list[2]
        assert isinstance(third_item, User)

    # slicing
    def test_slice_beginning(self):
        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        first_two_items = pag_list[:2]
        item_list = [item for item in first_two_items]
        assert len(item_list) == 2
        assert isinstance(item_list[0], User)
        assert hasattr(item_list[0], 'id')
        assert item_list[0].id == '1'

    def test_slice_middle(self):
        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        middle_two_items = pag_list[2:4]
        item_list = [item for item in middle_two_items]
        assert len(item_list) == 2
        assert isinstance(item_list[0], User)
        assert hasattr(item_list[0], 'id')
        assert item_list[0].id == '3'

    def test_slice_end(self):
        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        middle_two_items = pag_list[4:6]
        item_list = [item for item in middle_two_items]
        assert len(item_list) == 2
        assert isinstance(item_list[0], User)
        assert hasattr(item_list[0], 'id')
        assert item_list[0].id == '5'

    # __repr__()
    def test_repr(self):
        pag_list = PaginatedList(
            User,
            self.requester,
            'GET',
            'six_objects_three_pages'
        )
        assert pag_list.__repr__() == '<PaginatedList of type User>'
