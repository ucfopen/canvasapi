import unittest
from datetime import datetime

import requests_mock

from canvasapi import Canvas
from canvasapi.account import Account
from canvasapi.appointment_group import AppointmentGroup
from canvasapi.calendar_event import CalendarEvent
from canvasapi.conversation import Conversation
from canvasapi.course import Course, CourseNickname
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.group import Group, GroupCategory
from canvasapi.exceptions import ResourceDoesNotExist
from canvasapi.progress import Progress
from canvasapi.section import Section
from canvasapi.user import User
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

        self.assertIsInstance(account, Account)
        self.assertTrue(hasattr(account, 'name'))
        self.assertEqual(account.name, name)

    # get_account()
    def test_get_account(self, m):
        register_uris({'account': ['get_by_id']}, m)

        account = self.canvas.get_account(1)

        self.assertIsInstance(account, Account)

    def test_get_account_fail(self, m):
        register_uris({'generic': ['not_found']}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_account(settings.INVALID_ID)

    # get_accounts()
    def test_get_accounts(self, m):
        register_uris({'account': ['multiple']}, m)

        accounts = self.canvas.get_accounts()
        account_list = [account for account in accounts]
        self.assertEqual(len(account_list), 2)

    # get_course_accounts()
    def test_get_course_accounts(self, m):
        register_uris({'account': ['multiple_course']}, m)

        accounts = self.canvas.get_course_accounts()
        account_list = [account for account in accounts]
        self.assertEqual(len(account_list), 2)

    # get_course()
    def test_get_course(self, m):
        register_uris({'course': ['get_by_id']}, m)

        course = self.canvas.get_course(1)

        self.assertIsInstance(course, Course)
        self.assertTrue(hasattr(course, 'name'))

    def test_get_course_with_start_date(self, m):
        register_uris({'course': ['start_at_date']}, m)

        course = self.canvas.get_course(2)

        self.assertTrue(hasattr(course, 'start_at'))
        self.assertIsInstance(course.start_at, (str, unicode))
        self.assertTrue(hasattr(course, 'start_at_date'))
        self.assertIsInstance(course.start_at_date, datetime)

    def test_get_course_non_unicode_char(self, m):
        register_uris({'course': ['unicode_encode_error']}, m)

        course = self.canvas.get_course(3)

        self.assertTrue(hasattr(course, 'name'))

    def test_get_course_fail(self, m):
        register_uris({'generic': ['not_found']}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_course(settings.INVALID_ID)

    # get_user()
    def test_get_user(self, m):
        register_uris({'user': ['get_by_id']}, m)

        user = self.canvas.get_user(1)

        self.assertIsInstance(user, User)
        self.assertTrue(hasattr(user, 'name'))

    def test_get_user_by_id_type(self, m):
        register_uris({'user': ['get_by_id_type']}, m)

        user = self.canvas.get_user('jdoe', 'sis_user_id')

        self.assertIsInstance(user, User)
        self.assertTrue(hasattr(user, 'name'))

    def test_get_user_fail(self, m):
        register_uris({'generic': ['not_found']}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_user(settings.INVALID_ID)

    # get_courses()
    def test_get_courses(self, m):
        register_uris({'course': ['multiple', 'multiple_page_2']}, m)

        courses = self.canvas.get_courses(per_page=1)

        course_list = [course for course in courses]
        self.assertEqual(len(course_list), 4)
        self.assertIsInstance(course_list[0], Course)

    # get_activity_stream_summary()
    def test_get_activity_stream_summary(self, m):
        register_uris({'user': ['activity_stream_summary']}, m)

        summary = self.canvas.get_activity_stream_summary()

        self.assertIsInstance(summary, list)

    # get_todo_items()
    def test_get_todo_items(self, m):
        register_uris({'user': ['todo_items']}, m)

        todo_items = self.canvas.get_todo_items()

        self.assertIsInstance(todo_items, list)

    # get_upcoming_events()
    def test_get_upcoming_events(self, m):
        register_uris({'user': ['upcoming_events']}, m)

        events = self.canvas.get_upcoming_events()

        self.assertIsInstance(events, list)

    # get_course_nicknames()
    def test_get_course_nicknames(self, m):
        register_uris({'user': ['course_nicknames', 'course_nicknames_page_2']}, m)

        nicknames = self.canvas.get_course_nicknames()

        nickname_list = [name for name in nicknames]
        self.assertEqual(len(nickname_list), 4)
        self.assertIsInstance(nickname_list[0], CourseNickname)
        self.assertTrue(hasattr(nickname_list[0], 'nickname'))

    # get_course_nickname()
    def test_get_course_nickname(self, m):
        register_uris({'user': ['course_nickname']}, m)

        nickname = self.canvas.get_course_nickname(1)

        self.assertIsInstance(nickname, CourseNickname)
        self.assertTrue(hasattr(nickname, 'nickname'))

    def test_get_course_nickname_fail(self, m):
        register_uris({'generic': ['not_found']}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_course_nickname(settings.INVALID_ID)

    # set_course_nickname()
    def test_set_course_nickname(self, m):
        register_uris({'user': ['course_nickname_set']}, m)

        name = 'New Course Nickname'

        nickname = self.canvas.set_course_nickname(1, name)

        self.assertIsInstance(nickname, CourseNickname)
        self.assertTrue(hasattr(nickname, 'nickname'))
        self.assertEqual(nickname.nickname, name)

    # clear_course_nicknames()
    def test_clear_course_nicknames(self, m):
        register_uris({'user': ['course_nicknames_delete']}, m)

        success = self.canvas.clear_course_nicknames()
        self.assertTrue(success)

    # search_accounts()
    def test_search_accounts(self, m):
        register_uris({'account': ['domains']}, m)

        domains = self.canvas.search_accounts()

        self.assertIsInstance(domains, list)
        self.assertEqual(len(domains), 1)
        self.assertIn('name', domains[0])

    # get_section()
    def test_get_section(self, m):
        register_uris({'section': ['get_by_id']}, m)

        info = self.canvas.get_section(1)

        self.assertIsInstance(info, Section)

    # create_group()
    def test_create_group(self, m):
        register_uris({'group': ['create']}, m)

        group = self.canvas.create_group()

        self.assertIsInstance(group, Group)
        self.assertTrue(hasattr(group, 'name'))
        self.assertTrue(hasattr(group, 'description'))

    # get_group()
    def test_get_group(self, m):
        register_uris({'group': ['get_by_id']}, m)

        group = self.canvas.get_group(1)

        self.assertIsInstance(group, Group)
        self.assertTrue(hasattr(group, 'name'))
        self.assertTrue(hasattr(group, 'description'))

    # get_group_category()
    def test_get_group_category(self, m):
        register_uris({'group': ['get_category_by_id']}, m)

        response = self.canvas.get_group_category(1)
        self.assertIsInstance(response, GroupCategory)

    # create_conversation()
    def test_create_conversation(self, m):
        register_uris({'conversation': ['create_conversation']}, m)

        recipients = ['1', '2']
        body = 'Test Conversation Body'

        conversations = self.canvas.create_conversation(recipients=recipients, body=body)
        conversation_list = [conversation for conversation in conversations]

        self.assertIsInstance(conversation_list[0], Conversation)
        self.assertEqual(len(conversation_list), 2)

    # get_conversation()
    def test_get_conversation(self, m):
        register_uris({'conversation': ['get_by_id']}, m)

        convo = self.canvas.get_conversation(1)

        self.assertIsInstance(convo, Conversation)
        self.assertTrue(hasattr(convo, 'subject'))

    # get_conversations()
    def test_get_conversations(self, m):
        requires = {
            'conversation': ['get_conversations', 'get_conversations_2']
        }
        register_uris(requires, m)

        convos = self.canvas.get_conversations()
        conversation_list = [conversation for conversation in convos]

        self.assertEqual(len(conversation_list), 4)
        self.assertIsInstance(conversation_list[0], Conversation)

    # mark_all_as_read()
    def test_conversations_mark_all_as_read(self, m):
        register_uris({'conversation': ['mark_all_as_read']}, m)

        result = self.canvas.conversations_mark_all_as_read()
        self.assertTrue(result)

    # unread_count()
    def test_conversations_unread_count(self, m):
        register_uris({'conversation': ['unread_count']}, m)

        result = self.canvas.conversations_unread_count()
        self.assertEqual(result['unread_count'], "7")

    # get_running_batches()
    def test_conversations_get_running_batches(self, m):
        register_uris({'conversation': ['get_running_batches']}, m)

        result = self.canvas.conversations_get_running_batches()
        self.assertEqual(len(result), 2)
        self.assertIn('body', result[0]['message'])
        self.assertEqual(result[1]['message']['author_id'], 1)

    # batch_update()
    def test_conversations_batch_update(self, m):
        register_uris({'conversation': ['batch_update']}, m)

        conversation_ids = [1, 2]
        this_event = "mark_as_read"
        result = self.canvas.conversations_batch_update(
            event=this_event,
            conversation_ids=conversation_ids
        )
        self.assertIsInstance(result, Progress)

    def test_conversations_batch_updated_fail_on_event(self, m):
        conversation_ids = [1, 2]
        this_event = "this doesn't work"
        result = self.canvas.conversations_batch_update(
            event=this_event,
            conversation_ids=conversation_ids
        )
        self.assertIsInstance(result, ValueError)

    def test_conversations_batch_updated_fail_on_ids(self, m):
        conversation_ids = [None] * 501
        this_event = "mark_as_read"
        result = self.canvas.conversations_batch_update(
            event=this_event,
            conversation_ids=conversation_ids
        )
        self.assertIsInstance(result, ValueError)

    # create_calendar_event()
    def test_create_calendar_event(self, m):
        register_uris({'calendar_event': ['create_calendar_event']}, m)

        cal_event = {
            "context_code": "course_123"
        }
        evnt = self.canvas.create_calendar_event(calendar_event=cal_event)

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

        cal_event = self.canvas.reserve_time_slot(calendar_event_id=567, participant_id=777)
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

    # create_appointment_group()
    def test_create_appointment_group(self, m):
        register_uris({'appointment_group': ['create_appointment_group']}, m)

        evnt = self.canvas.create_appointment_group({
            "context_codes": ["course_123"],
            "title": "Test Group"
        })

        self.assertIsInstance(evnt, AppointmentGroup)
        self.assertEqual(evnt.context_codes[0], "course_123")
        self.assertEqual(evnt.id, 234)

    def test_create_appointment_group_fail_on_context_codes(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.canvas.create_appointment_group({
                "title": "Test Group"
            })

    def test_create_appointment_group_fail_on_title(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.canvas.create_appointment_group({"context_codes": "course_123"})

    # list_user_participants()
    def test_list_user_participants(self, m):
        register_uris({'appointment_group': ['list_user_participants']}, m)

        users = self.canvas.list_user_participants(222)
        users_list = [user for user in users]
        self.assertEqual(len(users_list), 2)

    # list_group_participants()
    def test_list_group_participants(self, m):
        register_uris({'appointment_group': ['list_group_participants']}, m)

        groups = self.canvas.list_group_participants(222)
        groups_list = [group for group in groups]
        self.assertEqual(len(groups_list), 2)

    # search_recipients()
    def test_search_recipients(self, m):
        register_uris({'user': ['search_recipients']}, m)

        recipients = self.canvas.search_recipients()
        self.assertIsInstance(recipients, list)
        self.assertEqual(len(recipients), 2)

    # search_all_courses()
    def test_search_all_courses(self, m):
        register_uris({'course': ['search_all_courses']}, m)

        courses = self.canvas.search_all_courses()
        self.assertIsInstance(courses, list)
        self.assertEqual(len(courses), 2)
