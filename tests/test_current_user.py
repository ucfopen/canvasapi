from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import uuid

import requests_mock

from canvasapi import Canvas
from canvasapi.assignment import Assignment
from canvasapi.avatar import Avatar
from canvasapi.bookmark import Bookmark
from canvasapi.calendar_event import CalendarEvent
from canvasapi.course import Course
from canvasapi.file import File
from canvasapi.group import Group
from canvasapi.enrollment import Enrollment
from canvasapi.user import User
from canvasapi.login import Login
from tests import settings
from tests.util import cleanup_file, register_uris


@requests_mock.Mocker()
class TestCurrentUser(unittest.TestCase):
	def setUp(self):
		self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)
		with requests_mock.Mocker() as m:
			register_uris({'current_user': ['get_by_id']}, m)
		self.user = self.canvas.get_current_user()

	# list_groups()
 	def test_list_groups(self, m):
		register_uris({'user': ['list_groups', 'list_groups2']}, m)

		groups = self.user.list_groups()
		group_list = [group for group in groups]

		self.assertEqual(len(group_list), 4)
		self.assertIsInstance(group_list[0], Group)

 	# list_bookmarks()
 	def test_list_bookmarks(self, m):
 		register_uris({'bookmark': ['list_bookmarks']}, m)
		
		bookmarks = self.user.list_bookmarks()
		bookmark_list = [bookmark for bookmark in bookmarks]
		self.assertEqual(len(bookmark_list), 2)
		self.assertIsInstance(bookmark_list[0], Bookmark)

 	# get_bookmark()
 	def test_get_bookmark(self, m):
 		register_uris({'bookmark': ['get_bookmark']}, m)

 		bookmark_by_id = self.user.get_bookmark(45)
 		self.assertIsInstance(bookmark_by_id, Bookmark)
 		self.assertEqual(bookmark_by_id.name, "Test Bookmark 3")
 		bookmark_by_obj = self.user.get_bookmark(bookmark_by_id)
 		self.assertIsInstance(bookmark_by_obj, Bookmark)
 		self.assertEqual(bookmark_by_obj.name, "Test Bookmark 3")

 	# create_bookmark()
 	def test_create_bookmark(self, m):
 		register_uris({'bookmark': ['create_bookmark']}, m)
		evnt = self.user.create_bookmark(
			name="Test Bookmark",
			url="https://www.google.com"
		)
		self.assertIsInstance(evnt, Bookmark)
		self.assertEqual(evnt.name, "Test Bookmark")
		self.assertEqual(evnt.url, "https://www.google.com")

	# list_calendar_events_for_user()
	def test_list_calendar_events_for_user(self, m):
		register_uris({'user': ['list_calendar_events_for_user']}, m)

		cal_events = self.user.list_calendar_events_for_user()
		cal_event_list = [cal_event for cal_event in cal_events]
		self.assertEqual(len(cal_event_list), 2)
		self.assertIsInstance(cal_event_list[0], CalendarEvent)
