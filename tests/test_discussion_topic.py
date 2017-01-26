import unittest

import requests_mock

from pycanvas import Canvas
from pycanvas.discussion_topic import DiscussionTopic
from pycanvas.course import Course
from pycanvas.group import Group
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestDiscussionTopic(unittest.TestCase):

    @classmethod
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

    def test__str__(self, m):
        string = str(self.discussion_topic)
        self.assertIsInstance(string, str)

    def test_delete(self, m):
        register_uris({'discussion_topic': ['delete']}, m)

        topic_id = 1
        topic = self.discussion_topic.delete(topic_id)
        self.assertTrue(topic)

    def test_update_entry(self, m):
        register_uris({'discussion_topic': ['update_entry']}, m)

        entry_id = 1
        entry = self.discussion_topic.update_entry(entry_id)
        self.assertTrue(entry)

    def test_delete_entry(self, m):
        register_uris({'discussion_topic': ['delete_entry']}, m)

        entry_id = 1
        entry = self.discussion_topic.delete_entry(entry_id)
        self.assertTrue(entry)

    # parent_id
    def test_parent_id_course(self, m):
        self.assertEquals(self.discussion_topic.parent_id, 1)

    def test_parent_id_group(self, m):
        self.assertEquals(self.discussion_topic_group.parent_id, 1)

    def test_parent_id_no_id(self, m):
        discussion = DiscussionTopic(self.canvas._Canvas__requester, {'id': 1})
        with self.assertRaises(ValueError):
            discussion.parent_id

    # parent_type
    def test_parent_type_course(self, m):
        self.assertEquals(self.discussion_topic.parent_type, 'course')

    def test_parent_type_group(self, m):
        self.assertEquals(self.discussion_topic_group.parent_type, 'group')

    def test_parent_type_no_id(self, m):
        discussion = DiscussionTopic(self.canvas._Canvas__requester, {'id': 1})
        with self.assertRaises(ValueError):
            discussion.parent_type

    # get_parent()
    def test_get_parent_course(self, m):
        register_uris({'course': ['get_by_id']}, m)

        assert isinstance(self.discussion_topic.get_parent(), Course)

    def test_get_parent_group(self, m):
        register_uris({'group': ['get_by_id']}, m)

        assert isinstance(self.discussion_topic_group.get_parent(), Group)
