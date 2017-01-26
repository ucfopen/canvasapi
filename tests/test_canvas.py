import unittest
from datetime import datetime

import requests_mock

from pycanvas import Canvas
from pycanvas.exceptions import RequiredFieldMissing
from pycanvas.account import Account
from pycanvas.appointment_group import AppointmentGroup
from pycanvas.calendar_event import CalendarEvent
from pycanvas.conversation import Conversation
from pycanvas.course import Course, CourseNickname
from pycanvas.group import Group, GroupCategory
from pycanvas.exceptions import ResourceDoesNotExist
from pycanvas.progress import Progress
from pycanvas.section import Section
from pycanvas.user import User
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestCanvas(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

    # create_account()
    def test_create_account(self, m):
        register_uris({'account': ['create']}, m)

        name = 'Newly Created Account'

        account_dict = {
            'name': name
        }
        account = self.canvas.create_account(account=account_dict)

        assert isinstance(account, Account)
        assert hasattr(account, 'name')
        assert account.name == name

    # get_account()
    def test_get_account(self, m):
        register_uris({'account': ['get_by_id']}, m)

        account = self.canvas.get_account(1)

        assert isinstance(account, Account)

    def test_get_account_fail(self, m):
        register_uris({'generic': ['not_found']}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_account(settings.INVALID_ID)

    # get_accounts()
    def test_get_accounts(self, m):
        register_uris({'account': ['multiple']}, m)

        accounts = self.canvas.get_accounts()
        account_list = [account for account in accounts]
        assert len(account_list) == 2

    # get_course_accounts()
    def test_get_course_accounts(self, m):
        register_uris({'account': ['multiple_course']}, m)

        accounts = self.canvas.get_course_accounts()
        account_list = [account for account in accounts]
        assert len(account_list) == 2

    # get_course()
    def test_get_course(self, m):
        register_uris({'course': ['get_by_id']}, m)

        course = self.canvas.get_course(1)

        assert isinstance(course, Course)
        assert hasattr(course, 'name')

    def test_get_course_with_start_date(self, m):
        register_uris({'course': ['start_at_date']}, m)

        course = self.canvas.get_course(2)

        assert hasattr(course, 'start_at')
        assert isinstance(course.start_at, (str, unicode))
        assert hasattr(course, 'start_at_date')
        assert isinstance(course.start_at_date, datetime)

    def test_get_course_non_unicode_char(self, m):
        register_uris({'course': ['unicode_encode_error']}, m)

        course = self.canvas.get_course(3)

        assert hasattr(course, 'name')

    def test_get_course_fail(self, m):
        register_uris({'generic': ['not_found']}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_course(settings.INVALID_ID)

    # get_user()
    def test_get_user(self, m):
        register_uris({'user': ['get_by_id']}, m)

        user = self.canvas.get_user(1)

        assert isinstance(user, User)
        assert hasattr(user, 'name')

    def test_get_user_by_id_type(self, m):
        register_uris({'user': ['get_by_id_type']}, m)

        user = self.canvas.get_user('jdoe', 'sis_user_id')

        assert isinstance(user, User)
        assert hasattr(user, 'name')

    def test_get_user_fail(self, m):
        register_uris({'generic': ['not_found']}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_user(settings.INVALID_ID)

    # get_courses()
    def test_get_courses(self, m):
        register_uris({'course': ['multiple', 'multiple_page_2']}, m)

        courses = self.canvas.get_courses(per_page=1)

        course_list = [course for course in courses]
        assert len(course_list) == 4
        assert isinstance(course_list[0], Course)

    # get_activity_stream_summary()
    def test_get_activity_stream_summary(self, m):
        register_uris({'user': ['activity_stream_summary']}, m)

        summary = self.canvas.get_activity_stream_summary()

        assert isinstance(summary, list)

    # get_todo_items()
    def test_get_todo_items(self, m):
        register_uris({'user': ['todo_items']}, m)

        todo_items = self.canvas.get_todo_items()

        assert isinstance(todo_items, list)

    # get_upcoming_events()
    def test_get_upcoming_events(self, m):
        register_uris({'user': ['upcoming_events']}, m)

        events = self.canvas.get_upcoming_events()

        assert isinstance(events, list)

    # get_course_nicknames()
    def test_get_course_nicknames(self, m):
        register_uris({'user': ['course_nicknames', 'course_nicknames_page_2']}, m)

        nicknames = self.canvas.get_course_nicknames()

        nickname_list = [name for name in nicknames]
        assert len(nickname_list) == 4
        assert isinstance(nickname_list[0], CourseNickname)
        assert hasattr(nickname_list[0], 'nickname')

    # get_course_nickname()
    def test_get_course_nickname(self, m):
        register_uris({'user': ['course_nickname']}, m)

        nickname = self.canvas.get_course_nickname(1)

        assert isinstance(nickname, CourseNickname)
        assert hasattr(nickname, 'nickname')

    def test_get_course_nickname_fail(self, m):
        register_uris({'generic': ['not_found']}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_course_nickname(settings.INVALID_ID)

    # set_course_nickname()
    def test_set_course_nickname(self, m):
        register_uris({'user': ['course_nickname_set']}, m)

        name = 'New Course Nickname'

        nickname = self.canvas.set_course_nickname(1, name)

        assert isinstance(nickname, CourseNickname)
        assert hasattr(nickname, 'nickname')
        assert nickname.nickname == name

    # clear_course_nicknames()
    def test_clear_course_nicknames(self, m):
        register_uris({'user': ['course_nicknames_delete']}, m)

        success = self.canvas.clear_course_nicknames()
        assert success

    # search_accounts()
    def test_search_accounts(self, m):
        register_uris({'account': ['domains']}, m)

        domains = self.canvas.search_accounts()

        assert isinstance(domains, list)
        assert len(domains) == 1
        assert 'name' in domains[0]

    # get_section()
    def test_get_section(self, m):
        register_uris({'section': ['get_by_id']}, m)

        info = self.canvas.get_section(1)

        assert isinstance(info, Section)

    # create_group()
    def test_create_group(self, m):
        register_uris({'group': ['create']}, m)

        group = self.canvas.create_group()

        assert isinstance(group, Group)
        assert hasattr(group, 'name')
        assert hasattr(group, 'description')

    # get_group()
    def test_get_group(self, m):
        register_uris({'group': ['get_by_id']}, m)

        group = self.canvas.get_group(1)

        assert isinstance(group, Group)
        assert hasattr(group, 'name')
        assert hasattr(group, 'description')

    # get_group_category()
    def test_get_group_category(self, m):
        register_uris({'group': ['get_category_by_id']}, m)

        response = self.canvas.get_group_category(1)
        assert isinstance(response, GroupCategory)

    # create_conversation()
    def test_create_conversation(self, m):
        register_uris({'conversation': ['create_conversation']}, m)

        recipients = ['1', '2']
        body = 'Test Conversation Body'

        conversations = self.canvas.create_conversation(recipients=recipients, body=body)
        conversation_list = [conversation for conversation in conversations]

        assert isinstance(conversation_list[0], Conversation)
        assert len(conversation_list) == 2

    # get_conversation()
    def test_get_conversation(self, m):
        register_uris({'conversation': ['get_by_id']}, m)

        convo = self.canvas.get_conversation(1)

        assert isinstance(convo, Conversation)
        assert hasattr(convo, 'subject')

    # get_conversations()
    def test_get_conversations(self, m):
        requires = {
            'conversation': ['get_conversations', 'get_conversations_2']
        }
        register_uris(requires, m)

        convos = self.canvas.get_conversations()
        conversation_list = [conversation for conversation in convos]

        assert len(conversation_list) == 4
        assert isinstance(conversation_list[0], Conversation)

    # mark_all_as_read()
    def test_conversations_mark_all_as_read(self, m):
        register_uris({'conversation': ['mark_all_as_read']}, m)

        result = self.canvas.conversations_mark_all_as_read()
        assert result is True

    # unread_count()
    def test_conversations_unread_count(self, m):
        register_uris({'conversation': ['unread_count']}, m)

        result = self.canvas.conversations_unread_count()
        assert result['unread_count'] == "7"

    # get_running_batches()
    def test_conversations_get_running_batches(self, m):
        register_uris({'conversation': ['get_running_batches']}, m)

        result = self.canvas.conversations_get_running_batches()
        assert len(result) == 2
        assert 'body' in result[0]['message']
        assert result[1]['message']['author_id'] == 1

    # batch_update()
    def test_conversations_batch_update(self, m):
        register_uris({'conversation': ['batch_update']}, m)

        conversation_ids = [1, 2]
        this_event = "mark_as_read"
        result = self.canvas.conversations_batch_update(
            event=this_event,
            conversation_ids=conversation_ids
        )
        assert isinstance(result, Progress)

    def test_conversations_batch_updated_fail_on_event(self, m):
        conversation_ids = [1, 2]
        this_event = "this doesn't work"
        result = self.canvas.conversations_batch_update(
            event=this_event,
            conversation_ids=conversation_ids
        )
        assert isinstance(result, ValueError)

    def test_conversations_batch_updated_fail_on_ids(self, m):
        conversation_ids = [None] * 501
        this_event = "mark_as_read"
        result = self.canvas.conversations_batch_update(
            event=this_event,
            conversation_ids=conversation_ids
        )
        assert isinstance(result, ValueError)

    # create_calendar_event()
    def test_create_calendar_event(self, m):
        register_uris({'calendar_event': ['create_calendar_event']}, m)

        cal_event = {
            "context_code": "course_123"
        }
        evnt = self.canvas.create_calendar_event(cal_event=cal_event)

        self.assertIsInstance(evnt, CalendarEvent)
        self.assertEqual(evnt.context_code, "course_123")
        self.assertEqual(evnt.id, 234)

    def test_create_calendar_event_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.canvas.create_calendar_event({})

    # list_calendar_events()
    def test_list_calendar_events(self, m):
        register_uris({'calendar_event': ['list_calendar_events']}, m)

        cal_events = self.canvas.list_calendar_events()
        cal_event_list = [cal_event for cal_event in cal_events]
        self.assertEqual(len(cal_event_list), 2)

    # get_calendar_event()
    def test_get_calendar_event(self, m):
        register_uris({'calendar_event': ['get_calendar_event']}, m)

        cal_event = self.canvas.get_calendar_event(567)
        self.assertIsInstance(cal_event, CalendarEvent)
        self.assertEqual(cal_event.title, "Test Event 3")

    # reserve_time_slot()
    def test_reserve_time_slot(self, m):
        register_uris({'calendar_event': ['reserve_time_slot']}, m)

        cal_event = self.canvas.reserve_time_slot(calendar_event_id=567)
        self.assertIsInstance(cal_event, CalendarEvent)
        self.assertEqual(cal_event.title, "Test Reservation")

    def test_reserve_time_slot_by_participant_id(self, m):
        register_uris({
            'calendar_event': ['reserve_time_slot_participant_id']
        }, m)

        cal_event = self.canvas.reserve_time_slot(
            calendar_event_id=567,
            participant_id=777
        )
        self.assertIsInstance(cal_event, CalendarEvent)
        self.assertEqual(cal_event.title, "Test Reservation")
        self.assertEqual(cal_event.user, 777)

    # list_appointment_groups()
    def test_list_appointment_groups(self, m):
        register_uris({'appointment_group': ['list_appointment_groups']}, m)

        appt_groups = self.canvas.list_appointment_groups()
        appt_groups_list = [appt_group for appt_group in appt_groups]
        self.assertEqual(len(appt_groups_list), 2)

    # get_appointment_group()
    def test_get_appointment_group(self, m):
        register_uris({'appointment_group': ['get_appointment_group']}, m)

        appt_group = self.canvas.get_appointment_group(567)
        self.assertIsInstance(appt_group, AppointmentGroup)
        self.assertEqual(appt_group.title, "Test Group 3")
