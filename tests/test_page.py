import unittest

import requests_mock

import settings
from util import register_uris
from pycanvas.canvas import Canvas
from pycanvas.course import Course
from pycanvas.group import Group
from pycanvas.page import Page, PageRevision


class TestPage(unittest.TestCase):
    """
    Test Page methods
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': ['get_by_id'],
            'group': ['get_single_group', 'get_page'],
            'generic': ['not_found'],
            'page': [
                'get_page', 'edit', 'delete_page',
                'list_revisions', 'list_revisions2',
                'latest_revision', 'get_latest_rev_by_id',
                'get_latest_rev_by_id_group', 'revert_to_revision',
                'revert_to_revision_group'
            ]
        }
        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)
        self.group = self.canvas.get_group(1)
        self.page_course = self.course.get_page('my-url')
        self.page_group = self.group.get_page('my-url')

    #__str__()
    def test__str__(self):
        string = str(self.page_course)
        assert isinstance(string, str)

    def test_edit(self):
        new_title = "New Page"
        self.page_course.edit(page={'title': new_title})

        assert isinstance(self.page_course, Page)
        assert hasattr(self.page_course, 'title')
        assert self.page_course.title == new_title

        #reset for future tests
        self.page_course = self.course.get_page('my-url')

    def test_delete(self):
        page = self.course.get_page('my-url')
        deleted_page = page.delete()

        assert isinstance(deleted_page, Page)

    def test_list_revisions(self):
        revisions = self.page_course.list_revisions()
        rev_list = [rev for rev in revisions]

        assert len(rev_list) == 4
        assert isinstance(rev_list[0], PageRevision)

    def test_show_latest_revision(self):
        revision = self.page_course.show_latest_revision()

        assert isinstance(revision, PageRevision)

    def test_get_revision_by_id_course(self):
        revision = self.page_course.get_revision_by_id(2)

        assert isinstance(revision, PageRevision)

    def test_get_revision_by_id_group(self):
        revision = self.page_group.get_revision_by_id(2)

        assert isinstance(revision, PageRevision)

    def test_revert_to_revision_course(self):
        revision = self.page_course.revert_to_revision(3)

        assert isinstance(revision, PageRevision)

    def test_revert_to_revision_group(self):
        revision = self.page_group.revert_to_revision(3)

        assert isinstance(revision, PageRevision)

    # parent_id
    def test_parent_id_course(self):
        assert self.page_course.parent_id == 1

    def test_parent_id_group(self):
        assert self.page_group.parent_id == 1

    def test_parent_id_no_id(self):
        page = Page(self.canvas._Canvas__requester, {'url': 'my-url'})
        with self.assertRaises(ValueError):
            page.parent_id

    # parent_type
    def test_parent_type_course(self):
        assert self.page_course.parent_type == 'course'

    def test_parent_type_group(self):
        assert self.page_group.parent_type == 'group'

    def test_parent_type_no_id(self):
        page = Page(self.canvas._Canvas__requester, {'url': 'my-url'})
        with self.assertRaises(ValueError):
            page.parent_type

    # get_parent()
    def test_get_parent_course(self):
        assert isinstance(self.page_course.get_parent(), Course)

    def test_get_parent_group(self):
        assert isinstance(self.page_group.get_parent(), Group)


class TestPageRevision(unittest.TestCase):
    """
    Tests PageRevision methods
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': ['get_by_id', 'get_page'],
            'group': ['get_single_group', 'get_page'],
            'generic': ['not_found'],
            'page': ['get_latest_rev_by_id', 'get_latest_rev_by_id_group']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)
        self.group = self.canvas.get_group(1)
        self.page_course = self.course.get_page('my-url')
        self.page_group = self.group.get_page('my-url')
        self.revision = self.page_course.get_revision_by_id(2)
        self.group_revision = self.page_group.get_revision_by_id(2)

    # __str__()
    def test__str__(self):
        string = str(self.revision)
        assert isinstance(string, str)

    # parent_id
    def test_parent_id_course(self):
        assert self.revision.parent_id == 1

    def test_parent_id_no_id(self):
        page = PageRevision(self.canvas._Canvas__requester, {'url': 'my-url'})
        with self.assertRaises(ValueError):
            page.parent_id

    # parent_type
    def test_parent_type_course(self):
        assert self.page_course.parent_type == 'course'

    def test_parent_type_group(self):
        assert self.page_group.parent_type == 'group'

    def test_parent_type_no_id(self):
        page = PageRevision(self.canvas._Canvas__requester, {'url': 'my-url'})
        with self.assertRaises(ValueError):
            page.parent_type

    # get_parent()
    def test_get_parent_course(self):
        assert isinstance(self.revision.get_parent(), Course)

    def test_get_parent_group(self):
        assert isinstance(self.group_revision.get_parent(), Group)
