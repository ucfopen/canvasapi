from __future__ import unicode_literals
import unittest

from builtins import str
import requests_mock

from canvasapi import Canvas
from canvasapi.discussion_topic import DiscussionTopic
from canvasapi.course import Course
from canvasapi.group import Group
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestDiscussionTopic(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                'course': ['get_by_id', 'get_discussion_topic'],
                'group': ['get_by_id', 'get_discussion_topic']
            }
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.group = self.canvas.get_group(1)
            self.discussion_topic = self.course.get_discussion_topic(1)
            self.discussion_topic_group = self.group.get_discussion_topic(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.discussion_topic)
        self.assertIsInstance(string, str)

    # delete()
    def test_delete(self, m):
        register_uris({'discussion_topic': ['delete']}, m)

        topic_id = 1
        topic = self.discussion_topic.delete(topic_id)
        self.assertTrue(topic)

    # update()
    def test_update(self, m):
        register_uris({'discussion_topic': ['update']}, m)

        discussion = self.discussion_topic.update()
        self.assertIsInstance(discussion, DiscussionTopic)
        self.assertTrue(hasattr(discussion, 'course_id'))
        self.assertEqual(discussion.course_id, 1)

    # update_entry()
    def test_update_entry(self, m):
        register_uris({'discussion_topic': ['update_entry']}, m)

        entry_id = 1
        entry = self.discussion_topic.update_entry(entry_id)
        self.assertTrue(entry)

    # delete_entry();
    def test_delete_entry(self, m):
        register_uris({'discussion_topic': ['delete_entry']}, m)

        entry_id = 1
        entry = self.discussion_topic.delete_entry(entry_id)
        self.assertTrue(entry)

    # post_entry()
    def test_post_entry(self, m):
        register_uris({'discussion_topic': ['post_entry']}, m)

        entry = self.discussion_topic.post_entry()
        self.assertTrue(entry)

    # list_topic_entries()
    def test_list_topic_entries(self, m):
        register_uris({'discussion_topic': ['list_topic_entries']}, m)

        entries = self.discussion_topic.list_topic_entries()
        entry_list = [entry for entry in entries]
        self.assertIsInstance(entry_list[0], DiscussionTopic)
        self.assertEqual(entry_list[0].id, 1)
        self.assertEqual(entry_list[0].user_id, 1)

    # post_reply()
    def test_post_reply(self, m):
        register_uris({'discussion_topic': ['post_reply']}, m)

        message = "Message 1"
        reply = self.discussion_topic.post_reply(1)
        self.assertIsInstance(reply, DiscussionTopic)
        self.assertEqual(reply.message, message)
        self.assertTrue(hasattr(reply, 'created_at'))
        self.assertTrue(hasattr(reply, 'message'))

    # list_entry_replies()
    def test_list_entry_replies(self, m):
        register_uris({'discussion_topic': ['list_entry_replies']}, m)

        replies = self.discussion_topic.list_entry_replies(1)
        reply_list = [reply for reply in replies]
        self.assertIsInstance(reply_list[0], DiscussionTopic)
        self.assertEqual(reply_list[0].id, 1)

    # list_entries()
    def test_list_entries(self, m):
        register_uris({'discussion_topic': ['list_entries']}, m)

        entries = self.discussion_topic.list_entries()
        entry_list = [entry for entry in entries]
        self.assertIsInstance(entry_list[0], DiscussionTopic)
        self.assertEqual(entry_list[0].id, 1)

    # mark_as_read()
    def test_mark_as_read(self, m):
        register_uris({'discussion_topic': ['mark_as_read']}, m)

        topic = self.discussion_topic.mark_as_read()
        self.assertTrue(topic)

    def test_mark_as_read_status(self, m):
        register_uris({'discussion_topic': ['mark_as_read_status']}, m)

        topic = self.discussion_topic.mark_as_read()
        self.assertFalse(topic)

    # mark_as_unread()
    def test_mark_as_unread(self, m):
        register_uris({'discussion_topic': ['mark_as_unread']}, m)

        topic = self.discussion_topic.mark_as_unread()
        self.assertTrue(topic)

    def test_mark_as_unread_status(self, m):
        register_uris({'discussion_topic': ['mark_as_unread_status']}, m)

        topic = self.discussion_topic.mark_as_unread()
        self.assertFalse(topic)

    # mark_entry_as_read()
    def test_mark_entry_as_read(self, m):
        register_uris({'discussion_topic': ['mark_entry_as_read']}, m)

        entry_id = 1
        entry = self.discussion_topic.mark_entry_as_read(entry_id)
        self.assertTrue(entry)

    def test_mark_entry_as_read_status(self, m):
        register_uris({'discussion_topic': ['mark_entry_as_read_status']}, m)

        entry_id = 1
        topic = self.discussion_topic.mark_entry_as_read(entry_id)
        self.assertFalse(topic)

    # mark_entry_as_unread()
    def test_mark_entry_as_unread(self, m):
        register_uris({'discussion_topic': ['mark_entry_as_unread']}, m)

        entry_id = 1
        entry = self.discussion_topic.mark_entry_as_unread(entry_id)
        self.assertTrue(entry)

    def test_mark_entry_as_unread_status(self, m):
        register_uris({'discussion_topic': ['mark_entry_as_unread_status']}, m)

        entry_id = 1
        topic = self.discussion_topic.mark_entry_as_unread(entry_id)
        self.assertFalse(topic)

    # mark_entries_as_read()
    def test_mark_entries_as_read(self, m):
        register_uris({'discussion_topic': ['mark_entries_as_read']}, m)

        entries = self.discussion_topic.mark_entries_as_read()
        self.assertTrue(entries)

    def test_mark_entries_as_read_status(self, m):
        register_uris({'discussion_topic': ['mark_entries_as_read_status']}, m)

        entries = self.discussion_topic.mark_entries_as_read()
        self.assertFalse(entries)

    # mark_entries_as_unread()
    def test_mark_entries_as_unread(self, m):
        register_uris({'discussion_topic': ['mark_entries_as_unread']}, m)

        entries = self.discussion_topic.mark_entries_as_unread()
        self.assertTrue(entries)

    def test_mark_entries_as_unread_status(self, m):
        register_uris({'discussion_topic': ['mark_entries_as_unread_status']}, m)

        entries = self.discussion_topic.mark_entries_as_unread()
        self.assertFalse(entries)

    # rate_entry()
    def test_rate_entry(self, m):
        register_uris({'discussion_topic': ['rate_entry']}, m)

        entry_id = 1
        entry = self.discussion_topic.rate_entry(entry_id)
        self.assertTrue(entry)

    # subscribe()
    def test_subscribe(self, m):
        register_uris({'discussion_topic': ['subscribe']}, m)

        subscribe = self.discussion_topic.subscribe()
        self.assertTrue(subscribe)

    def test_subscribe_status(self, m):
        register_uris({'discussion_topic': ['subscribe_status']}, m)

        subscribe = self.discussion_topic.subscribe()
        self.assertFalse(subscribe)

    # unsubscribe()
    def test_unsubscribe(self, m):
        register_uris({'discussion_topic': ['unsubscribe']}, m)

        unsubscribe = self.discussion_topic.unsubscribe()
        self.assertTrue(unsubscribe)

    def test_unsubscribe_status(self, m):
        register_uris({'discussion_topic': ['unsubscribe_status']}, m)

        unsubscribe = self.discussion_topic.unsubscribe()
        self.assertFalse(unsubscribe)

    # parent_id
    def test_parent_id_course(self, m):
        self.assertEqual(self.discussion_topic.parent_id, 1)

    def test_parent_id_group(self, m):
        self.assertEqual(self.discussion_topic_group.parent_id, 1)

    def test_parent_id_no_id(self, m):
        discussion = DiscussionTopic(self.canvas._Canvas__requester, {'id': 1})
        with self.assertRaises(ValueError):
            discussion.parent_id

    # parent_type
    def test_parent_type_course(self, m):
        self.assertEqual(self.discussion_topic.parent_type, 'course')

    def test_parent_type_group(self, m):
        self.assertEqual(self.discussion_topic_group.parent_type, 'group')

    def test_parent_type_no_id(self, m):
        discussion = DiscussionTopic(self.canvas._Canvas__requester, {'id': 1})
        with self.assertRaises(ValueError):
            discussion.parent_type

    # get_parent()
    def test_get_parent_course(self, m):
        register_uris({'course': ['get_by_id']}, m)

        self.assertIsInstance(self.discussion_topic.get_parent(), Course)

    def test_get_parent_group(self, m):
        register_uris({'group': ['get_by_id']}, m)

        self.assertIsInstance(self.discussion_topic_group.get_parent(), Group)
