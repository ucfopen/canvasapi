import unittest
import requests_mock

import settings
from util import register_uris
from pycanvas import Canvas
from pycanvas.assignment import Assignment
from pycanvas.avatar import Avatar
from pycanvas.course import Course
from pycanvas.enrollment import Enrollment
from pycanvas.page_view import PageView
from pycanvas.user import User


class TestUser(unittest.TestCase):
    """
    Tests User functionality.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'generic': ['not_found'],
            'user': [
                'avatars', 'avatars_p2', 'color', 'color_update', 'colors',
                'courses', 'courses_p2', 'edit', 'get_by_id', 'get_by_id_2',
                'get_user_assignments', 'get_user_assignments2',
                'list_enrollments', 'list_enrollments_2', 'merge',
                'missing_sub', 'missing_sub_p2', 'page_views', 'page_views_p2',
                'profile', 'update_settings'
            ]
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.user = self.canvas.get_user(1)

    # __str__()
    def test__str__(self):
        string = str(self.user)
        assert isinstance(string, str)

    # get_profile()
    def test_get_profile(self):
        profile = self.user.get_profile()

        assert isinstance(profile, dict)
        assert 'name' in profile

    # get_page_views()
    def test_get_page_views(self):
        page_views = self.user.get_page_views()
        page_view_list = [view for view in page_views]

        assert len(page_view_list) == 4
        assert isinstance(page_view_list[0], PageView)

    # get_courses()
    def test_get_courses(self):
        courses = self.user.get_courses()
        course_list = [course for course in courses]

        assert len(course_list) == 4
        assert isinstance(course_list[0], Course)

    # get_missing_submissions()
    def test_get_missing_submissions(self):
        missing_assigments = self.user.get_missing_submissions()
        assignment_list = [assignment for assignment in missing_assigments]

        assert len(assignment_list) == 4
        assert isinstance(assignment_list[0], Assignment)

    # update_settings()
    def test_update_settings(self):
        settings = self.user.update_settings(manual_mark_as_read=True)

        assert isinstance(settings, dict)
        assert 'manual_mark_as_read' in settings
        assert settings['manual_mark_as_read'] is True

    # get_color()
    def test_get_color(self):
        color = self.user.get_color("course_1")

        assert isinstance(color, dict)
        assert 'hexcode' in color
        assert color['hexcode'] == "#abc123"

    # get_colors()
    def test_get_colors(self):
        colors = self.user.get_colors()

        assert isinstance(colors, dict)
        assert 'custom_colors' in colors
        assert isinstance(colors['custom_colors'], dict)

    # update_color()
    def test_update_color(self):
        new_hexcode = "#f00f00"
        color = self.user.update_color("course_1", new_hexcode)

        assert isinstance(color, dict)
        assert 'hexcode' in color
        assert color['hexcode'] == new_hexcode

    def test_update_color_no_hashtag(self):
        new_hexcode = "f00f00"
        color = self.user.update_color("course_1", new_hexcode)

        assert isinstance(color, dict)
        assert 'hexcode' in color
        assert color['hexcode'] == "#" + new_hexcode

    # edit()
    def test_edit(self):
        new_name = "New User Name"
        self.user.edit(user={'name': new_name})

        assert isinstance(self.user, User)
        assert hasattr(self.user, 'name')
        assert self.user.name == new_name

        # reset for future tests
        self.user = self.canvas.get_user(1)

    # merge_into()
    def test_merge_into_id(self):
        self.user.merge_into(2)

        assert isinstance(self.user, User)
        assert hasattr(self.user, 'name')
        assert self.user.name == 'John Smith'

        # reset for future tests
        self.user = self.canvas.get_user(1)

    def test_merge_into_user(self):
        other_user = self.canvas.get_user(2)
        self.user.merge_into(other_user)

        assert isinstance(self.user, User)
        assert hasattr(self.user, 'name')
        assert self.user.name == 'John Smith'

        # reset for future tests
        self.user = self.canvas.get_user(1)

    # get_avatars()
    def test_get_avatars(self):
        avatars = self.user.get_avatars()
        avatar_list = [avatar for avatar in avatars]

        assert len(avatar_list) == 4
        assert isinstance(avatar_list[0], Avatar)

    # get_assignments()
    def test_user_assignments(self):
        user = self.canvas.get_user(1)

        assignments = user.get_assignments(1)
        assignment_list = [assignment for assignment in assignments]

        assert isinstance(assignments[0], Assignment)
        assert len(assignment_list) == 4

    #list_enrollments()
    def test_list_enrollments(self):
        enrollments = self.user.list_enrollments()
        enrollment_list = [enrollment for enrollment in enrollments]

        assert len(enrollment_list) == 4
        assert isinstance(enrollment_list[0], Enrollment)
