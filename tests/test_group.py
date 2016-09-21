import unittest

import requests_mock

import settings
from util import register_uris
from pycanvas import Canvas
from pycanvas.group import Group
from pycanvas.group import GroupMembership
from pycanvas.group import GroupCategories
from pycanvas.course import Page
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
                'canvas_create_group', 'canvas_get_group',
                'group_create_page', 'group_edit_front_page',
                'group_show_front_page', 'group_get_page',
                'group_get_pages', 'group_get_pages2',
                'group_edit', 'group_delete',
                'group_list_users', 'group_list_users_p2',
                'group_invite', 'group_remove_user',
                'group_upload', 'group_upload_final',
                'group_preview_processed_html', 'group_get_activity_stream_summary',
                'group_list_memberships', 'group_list_memberships_p2',
                'group_get_membership', 'group_create_membership',
                'group_update_membership',
                'membership_update', 'membership_remove_user', 'membership_remove_self'
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
        self.membership = self.group.get_membership(1, "users")
        self.page = self.group.get_page('my-url')

    # __str__()
    def test__str__(self):
        string = str(self.group)
        assert isinstance(string, str)

    # show_front_page()
    def test_show_front_page(self):
        front_page = self.group.show_front_page()
        assert isinstance(front_page, Page)
        assert hasattr(front_page, 'url')
        assert hasattr(front_page, 'title')

    # create_front_page()
    def test_edit_front_page(self):
        new_front_page = self.group.edit_front_page()
        assert isinstance(new_front_page, Page)
        assert hasattr(new_front_page, 'url')
        assert hasattr(new_front_page, 'title')

    # list_pages()
    def test_get_pages(self):
        pages = self.group.get_pages()
        page_list = [page for page in pages]
        assert len(page_list) == 4
        assert isinstance(page_list[0], Page)
        assert hasattr(page_list[0], 'group_id')
        assert page_list[0].group_id == self.group.id

    # create_page()
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

    # get_page()
    def test_get_page(self):
        url = 'my-url'
        page = self.group.get_page(url)
        assert isinstance(page, Page)

    # edit()
    def test_edit(self):
        new_title = "New Group"
        response = self.group.edit(description=new_title)
        assert isinstance(response, Group)
        assert hasattr(response, 'description')
        assert response.description == new_title

        # # reset for future tests
        # self.group = self.group.get_page('my-url')

    # delete()
    def test_delete(self):
        group = self.group.delete()
        assert isinstance(group, Group)
        assert hasattr(group, 'name')
        assert hasattr(group, 'description')

    # invite()
    def test_invite(self):
        user_list = ["1", "2"]
        response = self.group.invite(user_list)
        gmembership_list = [groupmembership for groupmembership in response]
        assert isinstance(gmembership_list[0], GroupMembership)
        assert len(gmembership_list) == 2

    # list_users()
    def test_list_users(self):
        from pycanvas.user import User
        users = self.group.list_users()
        user_list = [user for user in users]
        assert isinstance(user_list[0], User)
        assert len(user_list) == 4

    # remove_user()
    def test_remove_user(self):
        from pycanvas.user import User
        response = self.group.remove_user(1)
        assert isinstance(response, User)

    # upload()
    def test_upload(self):
        import uuid
        import os
        filename = 'testfile_%s' % uuid.uuid4().hex
        file = open(filename, 'w+')
        response = self.group.upload(file)
        assert response[0] is True
        assert isinstance(response[1], dict)
        assert 'url' in response[1]
        # http://stackoverflow.com/a/10840586
        # Not as stupid as it looks.
        try:
            os.remove(filename)
        except OSError:
            pass

    # preview_processed_html()
    def test_preview_processed_html(self):
        html_str = "<p>processed html</p>"
        response = self.group.preview_html(html_str)
        assert response == html_str

    # # get_activity_stream() - not implemented
    # def test_activity_stream(self):
    #     return None

    # get_activity_stream_summary()
    def test_get_activity_stream_summary(self):
        response = self.group.get_activity_stream_summary()
        assert len(response) == 2
        assert 'type' in response[0]

    # list_memberships()
    def test_list_memberships(self):
        response = self.group.list_memberships()
        membership_list = [membership for membership in response]
        assert len(membership_list) == 4
        assert isinstance(membership_list[0], GroupMembership)
        assert hasattr(membership_list[0], 'group_id')

    # get_membership()
    def test_get_membership(self):
        response = self.group.get_membership(1, "users")
        assert isinstance(response, GroupMembership)

    # create_membership()
    def test_create_membership(self):
        response = self.group.create_membership(1)
        assert isinstance(response, GroupMembership)

    # update_membership()
    def test_update_membership(self):
        response = self.group.update_membership(1)
        assert isinstance(response, GroupMembership)

################################################
    # membership.update()
    def test_membership_update(self):
        response = self.membership.update(mem_id=1, moderator=False)
        assert isinstance(response, GroupMembership)

    # membership.remove_user()
    def test_membership_remove_user(self):
        response = self.membership.remove_user(1)
        assert not response

    # membership.remove_self()
    def test_membership_remove_self(self):
        response = self.membership.remove_self()
        assert not response

################################################
