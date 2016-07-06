import unittest
import requests

import requests_mock

import settings
from util import register_uris
from pycanvas import Canvas
from pycanvas.course import Course, CourseNickname, Page
from pycanvas.exceptions import RequiredFieldMissing


class TestGroup(unittest.TestCase):
    """
    Tests Group functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': ['get_by_id', 'show_front_page'],
            'group': [
                'create_page', 'show_front_page',
                'get_single_group', 'create_front_page',
                'get_page', 'get_pages', 'get_pages2'
            ]
        }

        require_generic = {
            'generic': ['not_found']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, require_generic, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)
        self.group = self.canvas.get_group(1)

    #__str__()
    def test__str__(self):
        string = str(self.group)
        assert isinstance(string, str)

    #show_front_page()
    def test_show_front_page(self):
        front_page = self.group.show_front_page()

        assert isinstance(front_page, Page)
        assert hasattr(front_page, 'url')
        assert hasattr(front_page, 'title')

    #create_front_page()
    def test_create_front_page(self):
        new_front_page = self.group.create_front_page()

        assert isinstance(new_front_page, Page)
        assert hasattr(new_front_page, 'url')
        assert hasattr(new_front_page, 'title')

    #list_pages()
    def test_get_pages(self):
        pages = self.group.get_pages()
        page_list = [page for page in pages]

        assert len(page_list) == 4
        assert isinstance(page_list[0], Page)

    #create_page()
    def test_create_page(self):
        title = 'New Page'
        new_page = self.group.create_page(wiki_page={'title': title})

        assert isinstance(new_page, Page)
        assert hasattr(new_page, 'title')
        assert new_page.title == title
        assert hasattr(new_page, 'group_id')
        assert new_page.group_id == self.group.id

    def test_create_page_fail(self):
        with self.assertRaises(RequiredFieldMissing):
            self.group.create_page(settings.INVALID_ID)

    #get_page()
    def test_get_page(self):
        url = 'my-url'
        page = self.group.get_page(url)

        assert isinstance(page, Page)
