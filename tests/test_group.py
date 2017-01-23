import os
import unittest
import uuid

import requests_mock

from pycanvas import Canvas
from pycanvas.group import Group, GroupMembership, GroupCategory
from pycanvas.course import Page
from pycanvas.discussion_topic import DiscussionTopic
from pycanvas.exceptions import RequiredFieldMissing
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestGroup(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'course': ['get_by_id'], 'group': ['get_by_id']}, m)

            self.course = self.canvas.get_course(1)
            self.group = self.canvas.get_group(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.group)
        assert isinstance(string, str)

    # show_front_page()
    def test_show_front_page(self, m):
        register_uris({'group': ['show_front_page']}, m)

        front_page = self.group.show_front_page()
        assert isinstance(front_page, Page)
        assert hasattr(front_page, 'url')
        assert hasattr(front_page, 'title')

    # create_front_page()
    def test_edit_front_page(self, m):
        register_uris({'group': ['edit_front_page']}, m)

        new_front_page = self.group.edit_front_page()
        assert isinstance(new_front_page, Page)
        assert hasattr(new_front_page, 'url')
        assert hasattr(new_front_page, 'title')

    # list_pages()
    def test_get_pages(self, m):
        register_uris({'group': ['get_pages', 'get_pages2']}, m)

        pages = self.group.get_pages()
        page_list = [page for page in pages]
        assert len(page_list) == 4
        assert isinstance(page_list[0], Page)
        assert hasattr(page_list[0], 'id')
        assert page_list[0].group_id == self.group.id

    # create_page()
    def test_create_page(self, m):
        register_uris({'group': ['create_page']}, m)

        title = 'New Page'
        new_page = self.group.create_page(wiki_page={'title': title})
        assert isinstance(new_page, Page)
        assert hasattr(new_page, 'title')
        assert new_page.title == title
        assert hasattr(new_page, 'id')
        assert new_page.group_id == self.group.id

    def test_create_page_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.group.create_page(settings.INVALID_ID)

    # get_page()
    def test_get_page(self, m):
        register_uris({'group': ['get_page']}, m)

        url = 'my-url'
        page = self.group.get_page(url)
        assert isinstance(page, Page)

    # edit()
    def test_edit(self, m):
        register_uris({'group': ['edit']}, m)

        new_title = "New Group"
        response = self.group.edit(description=new_title)
        assert isinstance(response, Group)
        assert hasattr(response, 'description')
        assert response.description == new_title

    # delete()
    def test_delete(self, m):
        register_uris({'group': ['delete']}, m)

        group = self.group.delete()
        assert isinstance(group, Group)
        assert hasattr(group, 'name')
        assert hasattr(group, 'description')

    # invite()
    def test_invite(self, m):
        register_uris({'group': ['invite']}, m)

        user_list = ["1", "2"]
        response = self.group.invite(user_list)
        gmembership_list = [groupmembership for groupmembership in response]
        assert isinstance(gmembership_list[0], GroupMembership)
        assert len(gmembership_list) == 2

    # list_users()
    def test_list_users(self, m):
        register_uris({'group': ['list_users', 'list_users_p2']}, m)

        from pycanvas.user import User
        users = self.group.list_users()
        user_list = [user for user in users]
        assert isinstance(user_list[0], User)
        assert len(user_list) == 4

    # remove_user()
    def test_remove_user(self, m):
        register_uris({'group': ['remove_user']}, m)

        from pycanvas.user import User
        response = self.group.remove_user(1)
        assert isinstance(response, User)

    # upload()
    def test_upload(self, m):
        register_uris({'group': ['upload', 'upload_final']}, m)

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
    def test_preview_processed_html(self, m):
        register_uris({'group': ['preview_processed_html']}, m)

        html_str = "<p>processed html</p>"
        response = self.group.preview_html(html_str)
        assert response == html_str

    # get_activity_stream_summary()
    def test_get_activity_stream_summary(self, m):
        register_uris({'group': ['activity_stream_summary']}, m)

        response = self.group.get_activity_stream_summary()
        assert len(response) == 2
        assert 'type' in response[0]

    # list_memberships()
    def test_list_memberships(self, m):
        register_uris({'group': ['list_memberships', 'list_memberships_p2']}, m)

        response = self.group.list_memberships()
        membership_list = [membership for membership in response]
        assert len(membership_list) == 4
        assert isinstance(membership_list[0], GroupMembership)
        assert hasattr(membership_list[0], 'id')

    # get_membership()
    def test_get_membership(self, m):
        register_uris({'group': ['get_membership']}, m)

        response = self.group.get_membership(1, "users")
        assert isinstance(response, GroupMembership)

    # create_membership()
    def test_create_membership(self, m):
        register_uris({'group': ['create_membership']}, m)

        response = self.group.create_membership(1)
        assert isinstance(response, GroupMembership)

    # update_membership()
    def test_update_membership(self, m):
        register_uris({'group': ['update_membership_user']}, m)

        response = self.group.update_membership(1)
        assert isinstance(response, GroupMembership)

    # get_discussion_topic()
    def test_get_discussion_topic(self, m):
        register_uris({'group':['get_discussion_topic']}, m)

        group_id = 1
        discussion = self.group.get_discussion_topic(group_id)
        self.assertIsInstance(discussion, DiscussionTopic)
        self.assertEquals(group_id, discussion.id)

    # get_discussion_topics()
    def test_get_discussion_topics(self, m):
        register_uris({'group': ['get_discussion_topics']}, m)

        response = self.group.get_discussion_topics()
        discussion_list = [discussion for discussion in response]
        self.assertIsInstance(discussion_list[0], DiscussionTopic)
        self.assertEquals(2, len(discussion_list))

    # create_discussion_topic()
    def test_create_discussion_topic(self, m):
        register_uris({'group': ['create_discussion_topic']}, m)

        discussion = self.group.create_discussion_topic()

        self.assertIsInstance(discussion, DiscussionTopic)

    # update_discussion_topic()
    def test_update_discussion_topic(self, m):
        register_uris({'group': ['update_discussion_topic']}, m)

        topic_id = 1
        discussion = self.group.update_discussion_topic(topic_id)
        self.assertIsInstance(discussion, DiscussionTopic)
        self.assertEquals(topic_id, discussion.id)

    # delete_discussion_topic()
    def test_delete_discussion_topic(self, m):
        register_uris({'group': ['delete_discussion_topic']}, m)

        topic_id = 1
        topic = self.group.delete_discussion_topic(topic_id)
        self.assertTrue(topic)

@requests_mock.Mocker()
class TestGroupMembership(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'group': ['get_by_id', 'get_membership']}, m)

            self.group = self.canvas.get_group(1)
            self.membership = self.group.get_membership(1, "users")

    # __str__()
    def test__str__(self, m):
        string = str(self.membership)
        assert isinstance(string, str)

    # update()
    def test_update(self, m):
        register_uris({'group': ['update_membership_membership']}, m)

        response = self.membership.update(mem_id=1, moderator=False)
        assert isinstance(response, GroupMembership)

    # remove_user()
    def test_remove_user(self, m):
        register_uris({'group': ['remove_user']}, m)

        response = self.membership.remove_user(1)
        # the response should be an empty dict that evaluates to false
        assert not response

    # remove_self()
    def test_remove_self(self, m):
        register_uris({'group': ['remove_self']}, m)

        response = self.membership.remove_self()
        # the response should be an empty dict that evaluates to false
        assert not response


@requests_mock.Mocker()
class TestGroupCategory(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)
        with requests_mock.Mocker() as m:
            register_uris({'course': ['get_by_id', 'create_group_category']}, m)

            self.course = self.canvas.get_course(1)
            self.group_category = self.course.create_group_category("Test String")

    # __str__()
    def test__str__(self, m):
        string = str(self.group_category)
        assert isinstance(string, str)

    # create_group()
    def test_create_group(self, m):
        register_uris({'group': ['category_create_group']}, m)

        test_str = "Test Create Group"
        response = self.group_category.create_group(name=test_str)
        assert isinstance(response, Group)
        assert hasattr(response, 'name')
        assert response.name == test_str

    # update()
    def test_update(self, m):
        register_uris({'group': ['category_update']}, m)

        new_name = "Test Update Category"
        response = self.group_category.update(name=new_name)
        assert isinstance(response, GroupCategory)

    # delete_category()
    def test_delete_category(self, m):
        register_uris({'group': ['category_delete_category']}, m)

        response = self.group_category.delete()
        # the response should be an empty dict that evaluates to false
        assert not response

    # list_groups()
    def test_list_groups(self, m):
        register_uris({'group': ['category_list_groups']}, m)

        response = self.group_category.list_groups()
        group_list = [group for group in response]
        assert len(group_list) == 2
        assert isinstance(group_list[0], Group)
        assert hasattr(group_list[0], 'id')

    # list_users()
    def test_list_users(self, m):
        from pycanvas.user import User

        register_uris({'group': ['category_list_users']}, m)

        response = self.group_category.list_users()
        user_list = [user for user in response]
        assert len(user_list) == 4
        assert isinstance(user_list[0], User)
        assert hasattr(user_list[0], 'user_id')

    # assign_members()
    def test_assign_members(self, m):
        from pycanvas.progress import Progress
        from pycanvas.paginated_list import PaginatedList

        requires = {
            'group': [
                'category_assign_members_true',
                'category_assign_members_false'
            ]
        }
        register_uris(requires, m)

        result_true = self.group_category.assign_members(sync=True)
        return_false = self.group_category.assign_members()

        assert isinstance(result_true, PaginatedList)
        assert isinstance(return_false, Progress)
