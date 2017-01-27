import unittest
import uuid
import os

import requests_mock

from pycanvas import Canvas
from pycanvas.assignment import Assignment
from pycanvas.avatar import Avatar
from pycanvas.bookmark import Bookmark
from pycanvas.calendar_event import CalendarEvent
from pycanvas.course import Course
from pycanvas.group import Group
from pycanvas.enrollment import Enrollment
from pycanvas.page_view import PageView
from pycanvas.user import User
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
        assert isinstance(string, str)

    # get_profile()
    def test_get_profile(self, m):
        register_uris({'user': ['profile']}, m)

        profile = self.user.get_profile()

        assert isinstance(profile, dict)
        assert 'name' in profile

    # get_page_views()
    def test_get_page_views(self, m):
        register_uris({'user': ['page_views', 'page_views_p2']}, m)

        page_views = self.user.get_page_views()
        page_view_list = [view for view in page_views]

        assert len(page_view_list) == 4
        assert isinstance(page_view_list[0], PageView)

    # get_courses()
    def test_get_courses(self, m):
        register_uris({'user': ['courses', 'courses_p2']}, m)

        courses = self.user.get_courses()
        course_list = [course for course in courses]

        assert len(course_list) == 4
        assert isinstance(course_list[0], Course)

    # get_missing_submissions()
    def test_get_missing_submissions(self, m):
        register_uris({'user': ['missing_sub', 'missing_sub_p2']}, m)

        missing_assigments = self.user.get_missing_submissions()
        assignment_list = [assignment for assignment in missing_assigments]

        assert len(assignment_list) == 4
        assert isinstance(assignment_list[0], Assignment)

    # update_settings()
    def test_update_settings(self, m):
        register_uris({'user': ['update_settings']}, m)

        settings = self.user.update_settings(manual_mark_as_read=True)

        assert isinstance(settings, dict)
        assert 'manual_mark_as_read' in settings
        assert settings['manual_mark_as_read'] is True

    # get_color()
    def test_get_color(self, m):
        register_uris({'user': ['color']}, m)

        color = self.user.get_color("course_1")

        assert isinstance(color, dict)
        assert 'hexcode' in color
        assert color['hexcode'] == "#abc123"

    # get_colors()
    def test_get_colors(self, m):
        register_uris({'user': ['colors']}, m)

        colors = self.user.get_colors()

        assert isinstance(colors, dict)
        assert 'custom_colors' in colors
        assert isinstance(colors['custom_colors'], dict)

    # update_color()
    def test_update_color(self, m):
        register_uris({'user': ['color_update']}, m)

        new_hexcode = "#f00f00"
        color = self.user.update_color("course_1", new_hexcode)

        assert isinstance(color, dict)
        assert 'hexcode' in color
        assert color['hexcode'] == new_hexcode

    def test_update_color_no_hashtag(self, m):
        register_uris({'user': ['color_update']}, m)

        new_hexcode = "f00f00"
        color = self.user.update_color("course_1", new_hexcode)

        assert isinstance(color, dict)
        assert 'hexcode' in color
        assert color['hexcode'] == "#" + new_hexcode

    # edit()
    def test_edit(self, m):
        register_uris({'user': ['edit']}, m)

        new_name = "New User Name"
        self.user.edit(user={'name': new_name})

        assert isinstance(self.user, User)
        assert hasattr(self.user, 'name')
        assert self.user.name == new_name

    # merge_into()
    def test_merge_into_id(self, m):
        register_uris({'user': ['merge']}, m)

        self.user.merge_into(2)

        assert isinstance(self.user, User)
        assert hasattr(self.user, 'name')
        assert self.user.name == 'John Smith'

    def test_merge_into_user(self, m):
        register_uris({'user': ['get_by_id_2', 'merge']}, m)

        other_user = self.canvas.get_user(2)
        self.user.merge_into(other_user)

        assert isinstance(self.user, User)
        assert hasattr(self.user, 'name')
        assert self.user.name == 'John Smith'

    # get_avatars()
    def test_get_avatars(self, m):
        register_uris({'user': ['avatars', 'avatars_p2']}, m)

        avatars = self.user.get_avatars()
        avatar_list = [avatar for avatar in avatars]

        assert len(avatar_list) == 4
        assert isinstance(avatar_list[0], Avatar)

    # get_assignments()
    def test_user_assignments(self, m):
        register_uris({'user': ['get_user_assignments', 'get_user_assignments2']}, m)

        assignments = self.user.get_assignments(1)
        assignment_list = [assignment for assignment in assignments]

        assert isinstance(assignments[0], Assignment)
        assert len(assignment_list) == 4

    # list_enrollments()
    def test_list_enrollments(self, m):
        register_uris({'user': ['list_enrollments', 'list_enrollments_2']}, m)

        enrollments = self.user.get_enrollments()
        enrollment_list = [enrollment for enrollment in enrollments]

        assert len(enrollment_list) == 4
        assert isinstance(enrollment_list[0], Enrollment)

    # upload()
    def test_upload(self, m):
        register_uris({'user': ['upload', 'upload_final']}, m)

        filename = 'testfile_%s' % uuid.uuid4().hex
        file = open(filename, 'w+')

        response = self.user.upload(file)

        assert response[0] is True
        assert isinstance(response[1], dict)
        assert 'url' in response[1]

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

        assert len(group_list) == 4
        assert isinstance(group_list[0], Group)

    # list_calendar_events_for_user()
    def test_list_calendar_events_for_user(self, m):
        register_uris({'user': ['list_calendar_events_for_user']}, m)

        cal_events = self.user.list_calendar_events_for_user()
        cal_event_list = [cal_event for cal_event in cal_events]
        self.assertEqual(len(cal_event_list), 2)
        self.assertIsInstance(cal_event_list[0], CalendarEvent)

    # get_bookmark()
    def test_get_bookmark(self, m):
        register_uris({'bookmark': ['get_bookmark']}, m)

        bookmark = self.user.get_bookmark(45)
        self.assertIsInstance(bookmark, Bookmark)
        self.assertEqual(bookmark.name, "Test Bookmark 3")
