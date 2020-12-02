import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.course import Course
from canvasapi.discussion_topic import DiscussionEntry, DiscussionTopic
from canvasapi.exceptions import Forbidden
from canvasapi.group import Group
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestDiscussionTopic(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "course": ["get_by_id", "get_discussion_topic"],
                "group": ["get_by_id", "get_discussion_topic"],
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
        register_uris({"discussion_topic": ["delete"]}, m)

        response = self.discussion_topic.delete()
        self.assertTrue(response)

    # update()
    def test_update(self, m):
        register_uris({"discussion_topic": ["update"]}, m)

        discussion = self.discussion_topic.update()
        self.assertIsInstance(discussion, DiscussionTopic)
        self.assertTrue(hasattr(discussion, "course_id"))

    # post_entry()
    def test_post_entry(self, m):
        register_uris({"discussion_topic": ["post_entry"]}, m)

        entry = self.discussion_topic.post_entry()
        self.assertTrue(entry)

    # get_topic_entries()
    def test_get_topic_entries(self, m):
        register_uris({"discussion_topic": ["list_topic_entries"]}, m)

        entries = self.discussion_topic.get_topic_entries()
        entry_list = [entry for entry in entries]
        self.assertEqual(len(entry_list), 2)

        self.assertIsInstance(entry_list[0], DiscussionEntry)
        self.assertTrue(hasattr(entry_list[0], "id"))
        self.assertEqual(entry_list[0].id, 1)
        self.assertTrue(hasattr(entry_list[0], "user_id"))
        self.assertEqual(entry_list[0].user_id, 1)

    # get_entries()
    def test_get_entries(self, m):
        register_uris({"discussion_topic": ["list_entries"]}, m)

        entries_by_id = self.discussion_topic.get_entries([1, 2, 3])
        entry_list_by_id = [entry for entry in entries_by_id]
        self.assertTrue(len(entry_list_by_id), 3)

        entry_by_id = entry_list_by_id[-1]
        self.assertIsInstance(entry_by_id, DiscussionEntry)
        self.assertTrue(hasattr(entry_by_id, "id"))
        self.assertEqual(entry_by_id.id, 3)
        self.assertTrue(hasattr(entry_by_id, "message"))
        self.assertEqual(entry_by_id.message, "Lower level entry")

        entries_by_obj = self.discussion_topic.get_entries(entries_by_id)
        entry_list_by_obj = [entry for entry in entries_by_obj]
        self.assertTrue(len(entry_list_by_obj), 3)

        entry_by_obj = entry_list_by_obj[-1]
        self.assertIsInstance(entry_by_obj, DiscussionEntry)
        self.assertTrue(hasattr(entry_by_obj, "id"))
        self.assertEqual(entry_by_obj.id, 3)
        self.assertTrue(hasattr(entry_by_obj, "message"))
        self.assertEqual(entry_by_obj.message, "Lower level entry")

    # mark_as_read()
    def test_mark_as_read(self, m):
        register_uris({"discussion_topic": ["mark_as_read"]}, m)

        topic = self.discussion_topic.mark_as_read()
        self.assertTrue(topic)

    def test_mark_as_read_403(self, m):
        register_uris({"discussion_topic": ["mark_as_read_403"]}, m)

        with self.assertRaises(Forbidden):
            topic = self.discussion_topic.mark_as_read()
            self.assertFalse(topic)

    # mark_as_unread()
    def test_mark_as_unread(self, m):
        register_uris({"discussion_topic": ["mark_as_unread"]}, m)

        topic = self.discussion_topic.mark_as_unread()
        self.assertTrue(topic)

    def test_mark_as_unread_403(self, m):
        register_uris({"discussion_topic": ["mark_as_unread_403"]}, m)

        with self.assertRaises(Forbidden):
            topic = self.discussion_topic.mark_as_unread()
            self.assertFalse(topic)

    # mark_entries_as_read()
    def test_mark_entries_as_read(self, m):
        register_uris({"discussion_topic": ["mark_entries_as_read"]}, m)

        entries = self.discussion_topic.mark_entries_as_read()
        self.assertTrue(entries)

    def test_mark_entries_as_read_403(self, m):
        register_uris({"discussion_topic": ["mark_entries_as_read_403"]}, m)

        with self.assertRaises(Forbidden):
            entries = self.discussion_topic.mark_entries_as_read()
            self.assertFalse(entries)

    # mark_entries_as_unread()
    def test_mark_entries_as_unread(self, m):
        register_uris({"discussion_topic": ["mark_entries_as_unread"]}, m)

        entries = self.discussion_topic.mark_entries_as_unread()
        self.assertTrue(entries)

    def test_mark_entries_as_unread_403(self, m):
        register_uris({"discussion_topic": ["mark_entries_as_unread_403"]}, m)

        with self.assertRaises(Forbidden):
            entries = self.discussion_topic.mark_entries_as_unread()
            self.assertFalse(entries)

    # subscribe()
    def test_subscribe(self, m):
        register_uris({"discussion_topic": ["subscribe"]}, m)

        subscribe = self.discussion_topic.subscribe()
        self.assertTrue(subscribe)

    def test_subscribe_403(self, m):
        register_uris({"discussion_topic": ["subscribe_403"]}, m)

        with self.assertRaises(Forbidden):
            subscribe = self.discussion_topic.subscribe()
            self.assertFalse(subscribe)

    # unsubscribe()
    def test_unsubscribe(self, m):
        register_uris({"discussion_topic": ["unsubscribe"]}, m)

        unsubscribe = self.discussion_topic.unsubscribe()
        self.assertTrue(unsubscribe)

    def test_unsubscribe_403(self, m):
        register_uris({"discussion_topic": ["unsubscribe_403"]}, m)

        with self.assertRaises(Forbidden):
            unsubscribe = self.discussion_topic.unsubscribe()
            self.assertFalse(unsubscribe)

    # _parent_id
    def test_parent_id_course(self, m):
        self.assertEqual(self.discussion_topic._parent_id, 1)

    def test_parent_id_group(self, m):
        self.assertEqual(self.discussion_topic_group._parent_id, 1)

    def test_parent_id_no_id(self, m):
        discussion = DiscussionTopic(self.canvas._Canvas__requester, {"id": 1})
        with self.assertRaises(ValueError):
            discussion._parent_id

    # _parent_type
    def test_parent_type_course(self, m):
        self.assertEqual(self.discussion_topic._parent_type, "course")

    def test_parent_type_group(self, m):
        self.assertEqual(self.discussion_topic_group._parent_type, "group")

    def test_parent_type_no_id(self, m):
        discussion = DiscussionTopic(self.canvas._Canvas__requester, {"id": 1})
        with self.assertRaises(ValueError):
            discussion._parent_type

    # get_parent()
    def test_get_parent_course(self, m):
        register_uris({"course": ["get_by_id"]}, m)

        self.assertIsInstance(self.discussion_topic.get_parent(), Course)

    def test_get_parent_group(self, m):
        register_uris({"group": ["get_by_id"]}, m)

        self.assertIsInstance(self.discussion_topic_group.get_parent(), Group)


@requests_mock.Mocker()
class TestDiscussionEntry(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "course": ["get_by_id", "get_discussion_topic"],
                "discussion_topic": [
                    "list_entries_single",
                    "list_entries_single_group",
                ],
                "group": ["get_by_id", "get_discussion_topic"],
            }
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.group = self.canvas.get_group(1)
            self.discussion_topic = self.course.get_discussion_topic(1)
            self.discussion_topic_group = self.group.get_discussion_topic(1)
            self.discussion_entry = self.discussion_topic.get_entries([1])[0]
            self.discussion_entry_group = self.discussion_topic_group.get_entries([1])[
                0
            ]

    # __str__()
    def test__str__(self, m):
        string = str(self.discussion_entry)
        self.assertIsInstance(string, str)

    # _discussion_parent_id
    def test_discussion_parent_id_course(self, m):
        self.assertEqual(self.discussion_entry._discussion_parent_id, 1)

    def test_discussion_parent_id_group(self, m):
        self.assertEqual(self.discussion_entry_group._discussion_parent_id, 1)

    def test_discussion_parent_id_no_id(self, m):
        discussion = DiscussionEntry(self.canvas._Canvas__requester, {"id": 1})
        with self.assertRaises(ValueError):
            discussion._discussion_parent_id

    # _discussion_parent_type
    def test_discussion_parent_type_course(self, m):
        self.assertEqual(self.discussion_entry._discussion_parent_type, "course")

    def test_discussion_parent_type_group(self, m):
        self.assertEqual(self.discussion_entry_group._discussion_parent_type, "group")

    def test_discussion_parent_type_no_id(self, m):
        discussion = DiscussionEntry(self.canvas._Canvas__requester, {"id": 1})
        with self.assertRaises(ValueError):
            discussion._discussion_parent_type

    # get_discussion()
    def test_get_discussion(self, m):
        register_uris({"course": ["get_discussion_topic"]}, m)

        discussion = self.discussion_entry.get_discussion()
        self.assertIsInstance(discussion, DiscussionTopic)
        self.assertTrue(hasattr(discussion, "id"))
        self.assertEqual(self.discussion_topic.id, discussion.id)
        self.assertTrue(hasattr(discussion, "title"))
        self.assertEqual(self.discussion_topic.title, discussion.title)

    # delete()
    def test_delete(self, m):
        register_uris({"discussion_topic": ["delete_entry"]}, m)

        response = self.discussion_entry.delete()
        self.assertTrue(response)

    # post_reply()
    def test_post_reply(self, m):
        register_uris({"discussion_topic": ["post_reply"]}, m)

        message = "Reply message 1"
        reply = self.discussion_entry.post_reply(message=message)
        self.assertIsInstance(reply, DiscussionEntry)
        self.assertTrue(hasattr(reply, "message"))
        self.assertEqual(reply.message, message)
        self.assertTrue(hasattr(reply, "created_at"))

    # get_replies()
    def test_get_replies(self, m):
        register_uris({"discussion_topic": ["list_entry_replies"]}, m)

        replies = self.discussion_entry.get_replies()
        reply_list = [reply for reply in replies]
        self.assertTrue(len(reply_list), 5)

        reply = reply_list[0]
        self.assertIsInstance(reply, DiscussionEntry)
        self.assertTrue(hasattr(reply, "id"))
        self.assertEqual(reply.id, 5)
        self.assertTrue(hasattr(reply, "message"))
        self.assertEqual(reply.message, "Reply message 1")

    # mark_as_read()
    def test_mark_as_read(self, m):
        register_uris({"discussion_topic": ["mark_entry_as_read"]}, m)

        response = self.discussion_entry.mark_as_read()
        self.assertTrue(response)

    def test_mark_as_read_403(self, m):
        register_uris({"discussion_topic": ["mark_entry_as_read_403"]}, m)

        with self.assertRaises(Forbidden):
            self.discussion_entry.mark_as_read()

    # mark_as_unread()
    def test_mark_as_unread(self, m):
        register_uris({"discussion_topic": ["mark_entry_as_unread"]}, m)

        response = self.discussion_entry.mark_as_unread()
        self.assertTrue(response)

    def test_mark_as_unread_403(self, m):
        register_uris({"discussion_topic": ["mark_entry_as_unread_403"]}, m)

        with self.assertRaises(Forbidden):
            response = self.discussion_entry.mark_as_unread()
            self.assertFalse(response)

    # update()
    def test_update(self, m):
        register_uris({"discussion_topic": ["update_entry"]}, m)

        self.assertEqual(self.discussion_entry.message, "Top Level Entry")

        new_message = "Top Level Entry [Updated]"
        response = self.discussion_entry.update(message=new_message)

        self.assertTrue(response)
        self.assertIsInstance(self.discussion_entry, DiscussionEntry)
        self.assertEqual(self.discussion_entry.message, new_message)

    # rate()
    def test_rate(self, m):
        register_uris({"discussion_topic": ["rate_entry"]}, m)

        response = self.discussion_entry.rate(1)
        self.assertTrue(response)

    def test_rate_invalid_rating(self, m):
        with self.assertRaises(ValueError):
            self.discussion_entry.rate(2)
