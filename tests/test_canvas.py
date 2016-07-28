import unittest
from datetime import datetime

import requests_mock

from pycanvas import Canvas
from pycanvas.account import Account
from pycanvas.conversation import Conversation
from pycanvas.course import Course, CourseNickname
from pycanvas.exceptions import ResourceDoesNotExist
from pycanvas.section import Section
from pycanvas.user import User
from tests import settings
from tests.util import register_uris


class TestCanvas(unittest.TestCase):
    """
    Test core Canvas functionality.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'account': [
                'create', 'domains', 'get_by_id', 'multiple', 'multiple_course'
            ],
            'conversation': [
                'get_by_id', 'get_conversations', 'get_conversations_2',
                'create_conversation', 'mark_all_as_read', 'unread_count',
                'get_running_batches', 'batch_update'
            ],
            'course': [
                'get_by_id', 'multiple', 'multiple_page_2', 'start_at_date',
                'unicode_encode_error'
            ],
            'section': ['get_by_id'],
            'user': [
                'activity_stream_summary', 'course_nickname', 'course_nickname_set',
                'course_nicknames', 'course_nicknames_delete',
                'course_nicknames_page_2', 'courses', 'courses_p2', 'get_by_id',
                'get_by_id_type', 'todo_items', 'upcoming_events'
            ]
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, {'generic': ['not_found']}, adapter)
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

    # create_conversation()
    def test_create_conversation(self):
        recipients = ['1', '2']
        body = 'Test Conversation Body'

        conversations = self.canvas.create_conversation(recipients=recipients, body=body)
        conversation_list = [conversation for conversation in conversations]

        assert isinstance(conversation_list[0], Conversation)
        assert len(conversation_list) == 2

    # get_conversation()
    def test_get_conversation(self):
        convo = self.canvas.get_conversation(1)

        assert isinstance(convo, Conversation)
        assert hasattr(convo, 'subject')

    # get_conversations()
    def test_get_conversations(self):
        convos = self.canvas.get_conversations()
        conversation_list = [conversation for conversation in convos]

        assert len(conversation_list) == 4
        assert isinstance(conversation_list[0], Conversation)

    # mark_all_as_read()
    def test_mark_all_as_read(self):
        result = self.canvas.mark_all_as_read()
        assert result is True

    # unread_count()
    def test_unread_count(self):
        result = self.canvas.unread_count()
        assert result['unread_count'] == "7"

    # get_running_batches()
    def test_get_running_batches(self):
        result = self.canvas.get_running_batches()
        assert len(result) == 2
        assert 'body' in result[0]['message']
        assert result[1]['message']['author_id'] == 1

    # batch_update()
    def test_batch_update(self):
        from pycanvas.process import Process
        conversation_ids= [1, 2]
        this_event = "mark_as_read"
        result = self.canvas.batch_update(event=this_event, conversation_ids=conversation_ids)
        assert isinstance(result, Process)

    def test_batch_updated_fail_on_event(self):
        conversation_ids= [1, 2]
        this_event = "this doesn't work"
        result = self.canvas.batch_update(event=this_event, conversation_ids=conversation_ids)
        assert isinstance(result, ValueError)

    def test_batch_updated_fail_on_ids(self):
        conversation_ids = [None] * 501
        this_event = "mark_as_read"
        result = self.canvas.batch_update(event=this_event, conversation_ids=conversation_ids)
        assert isinstance(result, ValueError)
