import os
import unittest
import uuid

import requests_mock

from canvasapi import Canvas
from canvasapi.group import Group, GroupMembership, GroupCategory
from canvasapi.course import Page
from canvasapi.discussion_topic import DiscussionTopic
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.file import File
from canvasapi.folder import Folder
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
        self.assertIsInstance(string, str)

    # show_front_page()
    def test_show_front_page(self, m):
        register_uris({'group': ['show_front_page']}, m)

        front_page = self.group.show_front_page()
        self.assertIsInstance(front_page, Page)
        self.assertTrue(hasattr(front_page, 'url'))
        self.assertTrue(hasattr(front_page, 'title'))

    # create_front_page()
    def test_edit_front_page(self, m):
        register_uris({'group': ['edit_front_page']}, m)

        new_front_page = self.group.edit_front_page()
        self.assertIsInstance(new_front_page, Page)
        self.assertTrue(hasattr(new_front_page, 'url'))
        self.assertTrue(hasattr(new_front_page, 'title'))

    # list_pages()
    def test_get_pages(self, m):
        register_uris({'group': ['get_pages', 'get_pages2']}, m)

        pages = self.group.get_pages()
        page_list = [page for page in pages]
        self.assertEqual(len(page_list), 4)
        self.assertIsInstance(page_list[0], Page)
        self.assertTrue(hasattr(page_list[0], 'id'))
        self.assertEqual(page_list[0].group_id, self.group.id)

    # create_page()
    def test_create_page(self, m):
        register_uris({'group': ['create_page']}, m)

        title = 'New Page'
        new_page = self.group.create_page(wiki_page={'title': title})
        self.assertIsInstance(new_page, Page)
        self.assertTrue(hasattr(new_page, 'title'))
        self.assertEqual(new_page.title, title)
        self.assertTrue(hasattr(new_page, 'id'))
        self.assertEqual(new_page.group_id, self.group.id)

    def test_create_page_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.group.create_page(settings.INVALID_ID)

    # get_page()
    def test_get_page(self, m):
        register_uris({'group': ['get_page']}, m)

        url = 'my-url'
        page = self.group.get_page(url)
        self.assertIsInstance(page, Page)

    # edit()
    def test_edit(self, m):
        register_uris({'group': ['edit']}, m)

        new_title = "New Group"
        response = self.group.edit(description=new_title)
        self.assertIsInstance(response, Group)
        self.assertTrue(hasattr(response, 'description'))
        self.assertEqual(response.description, new_title)

    # delete()
    def test_delete(self, m):
        register_uris({'group': ['delete']}, m)

        group = self.group.delete()
        self.assertIsInstance(group, Group)
        self.assertTrue(hasattr(group, 'name'))
        self.assertTrue(hasattr(group, 'description'))

    # invite()
    def test_invite(self, m):
        register_uris({'group': ['invite']}, m)

        user_list = ["1", "2"]
        response = self.group.invite(user_list)
        gmembership_list = [groupmembership for groupmembership in response]
        self.assertIsInstance(gmembership_list[0], GroupMembership)
        self.assertEqual(len(gmembership_list), 2)

    # list_users()
    def test_list_users(self, m):
        register_uris({'group': ['list_users', 'list_users_p2']}, m)

        from canvasapi.user import User
        users = self.group.list_users()
        user_list = [user for user in users]
        self.assertIsInstance(user_list[0], User)
        self.assertEqual(len(user_list), 4)

    # remove_user()
    def test_remove_user(self, m):
        register_uris({'group': ['remove_user']}, m)

        from canvasapi.user import User
        response = self.group.remove_user(1)
        self.assertIsInstance(response, User)

    # upload()
    def test_upload(self, m):
        register_uris({'group': ['upload', 'upload_final']}, m)

        filename = 'testfile_%s' % uuid.uuid4().hex
        file = open(filename, 'w+')
        response = self.group.upload(file)
        self.assertTrue(response[0])
        self.assertIsInstance(response[1], dict)
        self.assertIn('url', response[1])
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
        self.assertEqual(response, html_str)

    # get_activity_stream_summary()
    def test_get_activity_stream_summary(self, m):
        register_uris({'group': ['activity_stream_summary']}, m)

        response = self.group.get_activity_stream_summary()
        self.assertEqual(len(response), 2)
        self.assertIn('type', response[0])

    # list_memberships()
    def test_list_memberships(self, m):
        register_uris({'group': ['list_memberships', 'list_memberships_p2']}, m)

        response = self.group.list_memberships()
        membership_list = [membership for membership in response]
        self.assertEqual(len(membership_list), 4)
        self.assertIsInstance(membership_list[0], GroupMembership)
        self.assertTrue(hasattr(membership_list[0], 'id'))

    # get_membership()
    def test_get_membership(self, m):
        register_uris({'group': ['get_membership']}, m)

        response = self.group.get_membership(1, "users")
        self.assertIsInstance(response, GroupMembership)

    # create_membership()
    def test_create_membership(self, m):
        register_uris({'group': ['create_membership']}, m)

        response = self.group.create_membership(1)
        self.assertIsInstance(response, GroupMembership)

    # update_membership()
    def test_update_membership(self, m):
        register_uris({'group': ['update_membership_user']}, m)

        response = self.group.update_membership(1)
        self.assertIsInstance(response, GroupMembership)

    # get_discussion_topic()
    def test_get_discussion_topic(self, m):
        register_uris({'group': ['get_discussion_topic']}, m)

        group_id = 1
        discussion = self.group.get_discussion_topic(group_id)
        self.assertIsInstance(discussion, DiscussionTopic)
        self.assertTrue(hasattr(discussion, 'group_id'))
        self.assertEquals(group_id, discussion.id)
        self.assertEquals(discussion.group_id, 1)

    # get_full_discussion_topic
    def test_get_full_discussion_topic(self, m):
        register_uris({'group': ['get_full_discussion_topic']}, m)

        topic_id = 1
        discussion = self.group.get_full_discussion_topic(topic_id)
        self.assertIsInstance(discussion, DiscussionTopic)
        self.assertTrue(hasattr(discussion, 'view'))
        self.assertTrue(hasattr(discussion, 'participants'))
        self.assertEquals(discussion.group_id, 1)

    # get_discussion_topics()
    def test_get_discussion_topics(self, m):
        register_uris({'group': ['get_discussion_topics']}, m)

        response = self.group.get_discussion_topics()
        discussion_list = [discussion for discussion in response]
        self.assertIsInstance(discussion_list[0], DiscussionTopic)
        self.assertTrue(hasattr(discussion_list[0], 'group_id'))
        self.assertEquals(2, len(discussion_list))

    # create_discussion_topic()
    def test_create_discussion_topic(self, m):
        register_uris({'group': ['create_discussion_topic']}, m)

        title = "Topic 1"
        discussion = self.group.create_discussion_topic()
        self.assertTrue(hasattr(discussion, 'group_id'))
        self.assertIsInstance(discussion, DiscussionTopic)
        self.assertEquals(discussion.title, title)
        self.assertEquals(discussion.group_id, 1)

    # reorder_pinned_topics()
    def test_reorder_pinned_topics(self, m):
        register_uris({'group': ['reorder_pinned_topics']}, m)

        order = [1, 2, 3]

        discussions = self.group.reorder_pinned_topics(order=order)
        self.assertTrue(discussions)

    def test_reorder_pinned_topics_no_list(self, m):
        register_uris({'group': ['reorder_pinned_topics_no_list']}, m)

        order = "1, 2, 3"

        with self.assertRaises(ValueError):
            self.group.reorder_pinned_topics(order=order)

    # list_files()
    def test_group_files(self, m):
        register_uris({'group': ['list_group_files', 'list_group_files2']}, m)

        files = self.group.list_files()
        file_list = [file for file in files]
        self.assertEqual(len(file_list), 4)
        self.assertIsInstance(file_list[0], File)

    # get_folder()
    def test_get_folder(self, m):
        register_uris({'group': ['get_folder']}, m)

        folder = self.group.get_folder(1)
        self.assertEqual(folder.name, "Folder 1")
        self.assertIsInstance(folder, Folder)

    # list_folders()
    def test_list_folders(self, m):
        register_uris({'group': ['list_folders']}, m)

        folders = self.group.list_folders()
        folder_list = [folder for folder in folders]
        self.assertEqual(len(folder_list), 2)
        self.assertIsInstance(folder_list[0], Folder)

    # create_folder()
    def test_create_folder(self, m):
        register_uris({'group': ['create_folder']}, m)

        name_str = "Test String"
        response = self.group.create_folder(name=name_str)
        self.assertIsInstance(response, Folder)


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
        self.assertIsInstance(string, str)

    # update()
    def test_update(self, m):
        register_uris({'group': ['update_membership_membership']}, m)

        response = self.membership.update(mem_id=1, moderator=False)
        self.assertIsInstance(response, GroupMembership)

    # remove_user()
    def test_remove_user(self, m):
        register_uris({'group': ['remove_user']}, m)

        response = self.membership.remove_user(1)

        self.assertIsInstance(response, dict)
        self.assertEqual(len(response), 0)

    # remove_self()
    def test_remove_self(self, m):
        register_uris({'group': ['remove_self']}, m)

        response = self.membership.remove_self()

        self.assertIsInstance(response, dict)
        self.assertEqual(len(response), 0)


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
        self.assertIsInstance(string, str)

    # create_group()
    def test_create_group(self, m):
        register_uris({'group': ['category_create_group']}, m)

        test_str = "Test Create Group"
        response = self.group_category.create_group(name=test_str)
        self.assertIsInstance(response, Group)
        self.assertTrue(hasattr(response, 'name'))
        self.assertEqual(response.name, test_str)

    # update()
    def test_update(self, m):
        register_uris({'group': ['category_update']}, m)

        new_name = "Test Update Category"
        response = self.group_category.update(name=new_name)
        self.assertIsInstance(response, GroupCategory)

    # delete_category()
    def test_delete_category(self, m):
        register_uris({'group': ['category_delete_category']}, m)

        response = self.group_category.delete()

        self.assertIsInstance(response, dict)
        self.assertEqual(len(response), 0)

    # list_groups()
    def test_list_groups(self, m):
        register_uris({'group': ['category_list_groups']}, m)

        response = self.group_category.list_groups()
        group_list = [group for group in response]
        self.assertEqual(len(group_list), 2)
        self.assertIsInstance(group_list[0], Group)
        self.assertTrue(hasattr(group_list[0], 'id'))

    # list_users()
    def test_list_users(self, m):
        from canvasapi.user import User

        register_uris({'group': ['category_list_users']}, m)

        response = self.group_category.list_users()
        user_list = [user for user in response]
        self.assertEqual(len(user_list), 4)
        self.assertIsInstance(user_list[0], User)
        self.assertTrue(hasattr(user_list[0], 'user_id'))

    # assign_members()
    def test_assign_members(self, m):
        from canvasapi.progress import Progress
        from canvasapi.paginated_list import PaginatedList

        requires = {
            'group': [
                'category_assign_members_true',
                'category_assign_members_false'
            ]
        }
        register_uris(requires, m)

        result_true = self.group_category.assign_members(sync=True)
        return_false = self.group_category.assign_members()

        self.assertIsInstance(result_true, PaginatedList)
        self.assertIsInstance(return_false, Progress)
