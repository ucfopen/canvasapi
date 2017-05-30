import unittest
import uuid
import os

import requests_mock

from canvasapi import Canvas
from canvasapi.assignment import Assignment
from canvasapi.avatar import Avatar
from canvasapi.bookmark import Bookmark
from canvasapi.calendar_event import CalendarEvent
from canvasapi.course import Course
from canvasapi.group import Group
from canvasapi.enrollment import Enrollment
from canvasapi.page_view import PageView
from canvasapi.user import User
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestUser(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'user': ['get_by_id']}, m)

            self.user = self.canvas.get_user(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.user)
        self.assertIsInstance(string, str)

    # get_profile()
    def test_get_profile(self, m):
        register_uris({'user': ['profile']}, m)

        profile = self.user.get_profile()

        self.assertIsInstance(profile, dict)
        self.assertIn('name', profile)

    # get_page_views()
    def test_get_page_views(self, m):
        register_uris({'user': ['page_views', 'page_views_p2']}, m)

        page_views = self.user.get_page_views()
        page_view_list = [view for view in page_views]

        self.assertEqual(len(page_view_list), 4)
        self.assertIsInstance(page_view_list[0], PageView)

    # get_courses()
    def test_get_courses(self, m):
        register_uris({'user': ['courses', 'courses_p2']}, m)

        courses = self.user.get_courses()
        course_list = [course for course in courses]

        self.assertEqual(len(course_list), 4)
        self.assertIsInstance(course_list[0], Course)

    # get_missing_submissions()
    def test_get_missing_submissions(self, m):
        register_uris({'user': ['missing_sub', 'missing_sub_p2']}, m)

        missing_assigments = self.user.get_missing_submissions()
        assignment_list = [assignment for assignment in missing_assigments]

        self.assertEqual(len(assignment_list), 4)
        self.assertIsInstance(assignment_list[0], Assignment)

    # update_settings()
    def test_update_settings(self, m):
        register_uris({'user': ['update_settings']}, m)

        settings = self.user.update_settings(manual_mark_as_read=True)

        self.assertIsInstance(settings, dict)
        self.assertIn('manual_mark_as_read', settings)
        self.assertTrue(settings['manual_mark_as_read'])

    # get_color()
    def test_get_color(self, m):
        register_uris({'user': ['color']}, m)

        color = self.user.get_color("course_1")

        self.assertIsInstance(color, dict)
        self.assertIn('hexcode', color)
        self.assertEqual(color['hexcode'], "#abc123")

    # get_colors()
    def test_get_colors(self, m):
        register_uris({'user': ['colors']}, m)

        colors = self.user.get_colors()

        self.assertIsInstance(colors, dict)
        self.assertIn('custom_colors', colors)
        self.assertIsInstance(colors['custom_colors'], dict)

    # update_color()
    def test_update_color(self, m):
        register_uris({'user': ['color_update']}, m)

        new_hexcode = "#f00f00"
        color = self.user.update_color("course_1", new_hexcode)

        self.assertIsInstance(color, dict)
        self.assertIn('hexcode', color)
        self.assertEqual(color['hexcode'], new_hexcode)

    def test_update_color_no_hashtag(self, m):
        register_uris({'user': ['color_update']}, m)

        new_hexcode = "f00f00"
        color = self.user.update_color("course_1", new_hexcode)

        self.assertIsInstance(color, dict)
        self.assertIn('hexcode', color)
        self.assertEqual(color['hexcode'], "#" + new_hexcode)

    # edit()
    def test_edit(self, m):
        register_uris({'user': ['edit']}, m)

        new_name = "New User Name"
        self.user.edit(user={'name': new_name})

        self.assertIsInstance(self.user, User)
        self.assertTrue(hasattr(self.user, 'name'))
        self.assertEqual(self.user.name, new_name)

    # merge_into()
    def test_merge_into_id(self, m):
        register_uris({'user': ['merge']}, m)

        self.user.merge_into(2)

        self.assertIsInstance(self.user, User)
        self.assertTrue(hasattr(self.user, 'name'))
        self.assertEqual(self.user.name, 'John Smith')

    def test_merge_into_user(self, m):
        register_uris({'user': ['get_by_id_2', 'merge']}, m)

        other_user = self.canvas.get_user(2)
        self.user.merge_into(other_user)

        self.assertIsInstance(self.user, User)
        self.assertTrue(hasattr(self.user, 'name'))
        self.assertEqual(self.user.name, 'John Smith')

    # get_avatars()
    def test_get_avatars(self, m):
        register_uris({'user': ['avatars', 'avatars_p2']}, m)

        avatars = self.user.get_avatars()
        avatar_list = [avatar for avatar in avatars]

        self.assertEqual(len(avatar_list), 4)
        self.assertIsInstance(avatar_list[0], Avatar)

    # get_assignments()
    def test_user_assignments(self, m):
        register_uris({'user': ['get_user_assignments', 'get_user_assignments2']}, m)

        assignments = self.user.get_assignments(1)
        assignment_list = [assignment for assignment in assignments]

        self.assertIsInstance(assignments[0], Assignment)
        self.assertEqual(len(assignment_list), 4)

    # list_enrollments()
    def test_list_enrollments(self, m):
        register_uris({'user': ['list_enrollments', 'list_enrollments_2']}, m)

        enrollments = self.user.get_enrollments()
        enrollment_list = [enrollment for enrollment in enrollments]

        self.assertEqual(len(enrollment_list), 4)
        self.assertIsInstance(enrollment_list[0], Enrollment)

    # upload()
    def test_upload(self, m):
        register_uris({'user': ['upload', 'upload_final']}, m)

        filename = 'testfile_%s' % uuid.uuid4().hex
        file = open(filename, 'w+')

        response = self.user.upload(file)

        self.assertTrue(response[0])
        self.assertIsInstance(response[1], dict)
        self.assertIn('url', response[1])

        # http://stackoverflow.com/a/10840586
        # Not as stupid as it looks.
        try:
            os.remove(filename)
        except OSError:
            pass

    # list_groups()
    def test_list_groups(self, m):
        register_uris({'user': ['list_groups', 'list_groups2']}, m)

        groups = self.user.list_groups()
        group_list = [group for group in groups]

        self.assertEqual(len(group_list), 4)
        self.assertIsInstance(group_list[0], Group)

    # list_calendar_events_for_user()
    def test_list_calendar_events_for_user(self, m):
        register_uris({'user': ['list_calendar_events_for_user']}, m)

        cal_events = self.user.list_calendar_events_for_user()
        cal_event_list = [cal_event for cal_event in cal_events]
        self.assertEqual(len(cal_event_list), 2)
        self.assertIsInstance(cal_event_list[0], CalendarEvent)

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

        bookmark = self.user.get_bookmark(45)
        self.assertIsInstance(bookmark, Bookmark)
        self.assertEqual(bookmark.name, "Test Bookmark 3")

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


@requests_mock.Mocker()
class TestUserDisplay(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({
                'course': ['get_by_id', 'list_gradeable_students']
            }, m)

            self.course = self.canvas.get_course(1)
            self.userDisplays = self.course.list_gradeable_students(1)
            self.userDisplayList = [ud for ud in self.userDisplays]
            self.userDisplay = self.userDisplayList[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.userDisplay)
        self.assertIsInstance(string, str)
