import unittest
from datetime import datetime

import requests_mock

import settings
from pycanvas import Canvas
from pycanvas.account import Account
from pycanvas.course import Course, CourseNickname
from pycanvas.group import Group
from pycanvas.exceptions import ResourceDoesNotExist
from pycanvas.section import Section
from pycanvas.user import User
from util import register_uris


class TestCanvas(unittest.TestCase):
    """
    Tests core Canvas functionality.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'account': [
                'create', 'domains', 'get_by_id', 'multiple', 'multiple_course'
            ],
            'course': [
                'get_by_id', 'multiple', 'multiple_page_2', 'start_at_date',
                'unicode_encode_error'
            ],
            'group': ['get_single_group'],
            'section': ['get_by_id'],
            'user': [
                'activity_stream_summary', 'course_nickname', 'course_nickname_set',
                'course_nicknames', 'course_nicknames_delete',
                'course_nicknames_page_2', 'courses', 'courses_p2', 'get_by_id',
                'get_by_id_type', 'todo_items', 'upcoming_events'
            ],
        }

        require_generic = {
            'generic': ['not_found']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, require_generic, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

    # create_account()
    def test_create_account(self):
        name = 'Newly Created Account'

        account_dict = {
            'name': name
        }
        account = self.canvas.create_account(account=account_dict)

        assert isinstance(account, Account)
        assert hasattr(account, 'name')
        assert account.name == name

    # get_account()
    def test_get_account(self):
        account = self.canvas.get_account(1)

        assert isinstance(account, Account)

    def test_get_account_fail(self):
        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_account(settings.INVALID_ID)

    # get_accounts()
    def test_get_accounts(self):
        accounts = self.canvas.get_accounts()
        account_list = [account for account in accounts]
        assert len(account_list) == 2

    # get_course_accounts()
    def test_get_course_accounts(self):
        accounts = self.canvas.get_course_accounts()
        account_list = [account for account in accounts]
        assert len(account_list) == 2

    # get_course()
    def test_get_course(self):
        course = self.canvas.get_course(1)

        assert isinstance(course, Course)
        assert hasattr(course, 'name')

    def test_get_course_with_start_date(self):
        course = self.canvas.get_course(2)

        assert hasattr(course, 'start_at')
        assert isinstance(course.start_at, (str, unicode))
        assert hasattr(course, 'start_at_date')
        assert isinstance(course.start_at_date, datetime)

    def test_get_course_non_unicode_char(self):
        course = self.canvas.get_course(3)

        assert hasattr(course, 'name')

    def test_get_course_fail(self):
        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_course(settings.INVALID_ID)

    # get_user()
    def test_get_user(self):
        user = self.canvas.get_user(1)

        assert isinstance(user, User)
        assert hasattr(user, 'name')

    def test_get_user_by_id_type(self):
        user = self.canvas.get_user('jdoe', 'sis_user_id')

        assert isinstance(user, User)
        assert hasattr(user, 'name')

    def test_get_user_fail(self):
        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_user(settings.INVALID_ID)

    # get_courses()
    def test_get_courses(self):
        courses = self.canvas.get_courses(per_page=1)

        course_list = [course for course in courses]
        assert len(course_list) == 4
        assert isinstance(course_list[0], Course)

    # get_activity_stream_summary()
    def test_get_activity_stream_summary(self):
        summary = self.canvas.get_activity_stream_summary()

        assert isinstance(summary, list)

    # get_todo_items()
    def test_get_todo_items(self):
        todo_items = self.canvas.get_todo_items()

        assert isinstance(todo_items, list)

    # get_upcoming_events()
    def test_get_upcoming_events(self):
        events = self.canvas.get_upcoming_events()

        assert isinstance(events, list)

    # get_course_nicknames()
    def test_get_course_nicknames(self):
        nicknames = self.canvas.get_course_nicknames()

        nickname_list = [name for name in nicknames]
        assert len(nickname_list) == 4
        assert isinstance(nickname_list[0], CourseNickname)
        assert hasattr(nickname_list[0], 'nickname')

    # get_course_nickname()
    def test_get_course_nickname(self):
        nickname = self.canvas.get_course_nickname(1)

        assert isinstance(nickname, CourseNickname)
        assert hasattr(nickname, 'nickname')

    def test_get_course_nickname_fail(self):
        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_course_nickname(settings.INVALID_ID)

    # set_course_nickname()
    def test_set_course_nickname(self):
        name = 'New Course Nickname'

        nickname = self.canvas.set_course_nickname(1, name)

        assert isinstance(nickname, CourseNickname)
        assert hasattr(nickname, 'nickname')
        assert nickname.nickname == name

    # clear_course_nicknames()
    def test_clear_course_nicknames(self):
        success = self.canvas.clear_course_nicknames()
        assert success

    # search_accounts()
    def test_search_accounts(self):
        domains = self.canvas.search_accounts()

        assert isinstance(domains, list)
        assert len(domains) == 1
        assert 'name' in domains[0]

    # get_section()
    def test_section(self):
        info = self.canvas.get_section(1)

        assert isinstance(info, Section)

    # get_single_group()
    def test_get_single_group(self):
        group = self.canvas.get_single_group(1)

        assert isinstance(group, Group)
        assert hasattr(group, 'name')
        assert hasattr(group, 'description')
