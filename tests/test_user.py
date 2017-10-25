from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import uuid

import requests_mock

from canvasapi import Canvas
from canvasapi.assignment import Assignment
from canvasapi.avatar import Avatar
from canvasapi.bookmark import Bookmark
from canvasapi.calendar_event import CalendarEvent
from canvasapi.communication_channel import CommunicationChannel
from canvasapi.course import Course
from canvasapi.file import File
from canvasapi.folder import Folder
from canvasapi.group import Group
from canvasapi.enrollment import Enrollment
from canvasapi.page_view import PageView
from canvasapi.user import User
from canvasapi.login import Login
from tests import settings
from tests.util import cleanup_file, register_uris


@requests_mock.Mocker()
class TestUser(unittest.TestCase):

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

        filename = 'testfile_user_{}'.format(uuid.uuid4().hex)
        with open(filename, 'w+') as file:
            response = self.user.upload(file)

        self.assertTrue(response[0])
        self.assertIsInstance(response[1], dict)
        self.assertIn('url', response[1])

        cleanup_file(filename)

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

    # list_communication_channels()
    def test_list_communication_channels(self, m):
        register_uris({'user': ['list_comm_channels', 'list_comm_channels2']}, m)

        comm_channels = self.user.list_communication_channels()
        channel_list = [channel for channel in comm_channels]
        self.assertEqual(len(channel_list), 4)
        self.assertIsInstance(channel_list[0], CommunicationChannel)

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

    # list_files()
    def test_user_files(self, m):
        register_uris({'user': ['get_user_files', 'get_user_files2']}, m)

        files = self.user.list_files()
        file_list = [file for file in files]
        self.assertEqual(len(file_list), 4)
        self.assertIsInstance(file_list[0], File)

    # get_file()
    def test_get_file_id(self, m):
        register_uris({'user': ['get_file']}, m)

        file = self.user.get_file(1)
        self.assertIsInstance(file, File)
        self.assertEqual(file.display_name, 'User_File.docx')
        self.assertEqual(file.size, 1024)

    # get_file()
    def test_get_file_obj(self, m):
        register_uris({'user': ['get_file', 'get_user_files']}, m)

        files = self.user.list_files()

        example_file = files[0]

        file = self.user.get_file(example_file)
        self.assertIsInstance(file, File)
        self.assertEqual(file.display_name, 'User_File.docx')
        self.assertEqual(file.size, 1024)

    # get_folder()
    def test_get_folder_id(self, m):
        register_uris({'user': ['get_folder']}, m)

        folder = self.user.get_folder(1)
        self.assertEqual(folder.name, "Folder 1")
        self.assertIsInstance(folder, Folder)

    # get_folder()
    def test_get_folder_obj(self, m):
        register_uris(
            {
                'user': ['create_folder', 'get_folder_2']
            }, m)

        name_str = "Test String"
        folder_obj = self.user.create_folder(name=name_str)

        folder = self.user.get_folder(folder_obj)
        self.assertEqual(folder.name, "Folder 2")
        self.assertIsInstance(folder, Folder)

    # list_folders()
    def test_list_folders(self, m):
        register_uris({'user': ['list_folders']}, m)

        folders = self.user.list_folders()
        folder_list = [folder for folder in folders]
        self.assertEqual(len(folder_list), 2)
        self.assertIsInstance(folder_list[0], Folder)

    # create_folder()
    def test_create_folder(self, m):
        register_uris({'user': ['create_folder']}, m)

        name_str = "Test String"
        response = self.user.create_folder(name=name_str)
        self.assertIsInstance(response, Folder)

    # list_user_logins()
    def test_list_user_logins(self, m):
        requires = {'user': ['list_user_logins', 'list_user_logins_2']}
        register_uris(requires, m)

        response = self.user.list_user_logins()
        login_list = [login for login in response]

        self.assertIsInstance(login_list[0], Login)
        self.assertEqual(len(login_list), 2)

    # list_observees()
    def test_list_observees(self, m):
        requires = {'user': ['list_observees', 'list_observees_2']}
        register_uris(requires, m)

        response = self.user.list_observees()
        observees_list = [observees for observees in response]

        self.assertIsInstance(observees_list[0], User)
        self.assertEqual(len(observees_list), 4)

    # add_observee_with_credentials()
    def test_add_observee_with_credentials(self, m):
        register_uris({'user': ['add_observee_with_credentials']}, m)

        response = self.user.add_observee_with_credentials()

        self.assertIsInstance(response, User)

    # show_observee()
    def test_show_observee(self, m):
        register_uris({'user': ['show_observee']}, m)

        response = self.user.show_observee(6)

        self.assertIsInstance(response, User)

    # add_observee()
    def test_add_observee(self, m):
        register_uris({'user': ['add_observee']}, m)

        response = self.user.add_observee(7)

        self.assertIsInstance(response, User)

    # remove_observee()
    def test_remove_observee(self, m):
        register_uris({'user': ['remove_observee']}, m)

        response = self.user.remove_observee(8)

        self.assertIsInstance(response, User)


@requests_mock.Mocker()
class TestUserDisplay(unittest.TestCase):

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
