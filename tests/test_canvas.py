import unittest
import warnings
from datetime import datetime

import pytz
import requests_mock

from canvasapi import Canvas
from canvasapi.account import Account
from canvasapi.account_calendar import AccountCalendar
from canvasapi.appointment_group import AppointmentGroup
from canvasapi.calendar_event import CalendarEvent
from canvasapi.comm_message import CommMessage
from canvasapi.conversation import Conversation
from canvasapi.course import Course, CourseNickname
from canvasapi.course_epub_export import CourseEpubExport
from canvasapi.discussion_topic import DiscussionTopic
from canvasapi.eportfolio import EPortfolio
from canvasapi.exceptions import RequiredFieldMissing, ResourceDoesNotExist
from canvasapi.file import File
from canvasapi.group import Group, GroupCategory
from canvasapi.jwt import JWT
from canvasapi.outcome import Outcome, OutcomeGroup
from canvasapi.paginated_list import PaginatedList
from canvasapi.poll import Poll
from canvasapi.progress import Progress
from canvasapi.section import Section
from canvasapi.todo import Todo
from canvasapi.user import User
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestCanvas(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

    # Canvas()
    def test_init_deprecate_url_contains_version(self, m):
        with self.assertRaises(
            ValueError,
            msg="`base_url` should not specify an API version. Remove trailing /api/v1/",
        ):
            Canvas(settings.BASE_URL_WITH_VERSION, settings.API_KEY)

    def test_init_warns_when_url_is_http(self, m):
        with warnings.catch_warnings(record=True):
            Canvas(settings.BASE_URL_AS_HTTP, settings.API_KEY)
            self.assertRaises(
                UserWarning,
                msg=(
                    "Canvas may respond unexpectedly when making requests to HTTP"
                    "URLs. If possible, please use HTTPS."
                ),
            )

    def test_init_warns_when_url_is_blank(self, m):
        with warnings.catch_warnings(record=True):
            Canvas(settings.BASE_URL_AS_BLANK, settings.API_KEY)
            self.assertRaises(
                UserWarning,
                msg="Canvas needs a valid URL, please provide a non-blank `base_url`.",
            )

    def test_init_warns_when_url_is_invalid(self, m):
        with warnings.catch_warnings(record=True):
            Canvas(settings.BASE_URL_AS_INVALID, settings.API_KEY)
            self.assertRaises(
                UserWarning,
                msg=(
                    "An invalid `base_url` for the Canvas API Instance was used."
                    "Please provide a valid HTTP or HTTPS URL if possible."
                ),
            )

    def test_init_strips_extra_spaces_in_api_key(self, m):
        client = Canvas(settings.BASE_URL, " 12345 ")
        self.assertEqual(client._Canvas__requester.access_token, "12345")

    def test_init_strips_extra_spaces_in_base_url(self, m):
        client = Canvas(settings.BASE_URL_WITH_EXTRA_SPACES, "12345")
        self.assertEqual(
            client._Canvas__requester.base_url, settings.BASE_URL_WITH_VERSION
        )

    # create_account()
    def test_create_account(self, m):
        register_uris({"account": ["create"]}, m)

        name = "Newly Created Account"

        account_dict = {"name": name}
        account = self.canvas.create_account(account=account_dict)

        self.assertIsInstance(account, Account)
        self.assertTrue(hasattr(account, "name"))
        self.assertEqual(account.name, name)

    # test token creation
    def test_create_jwt(self, m):
        register_uris({"jwt": ["create_jwt"]}, m)

        # verify returned object is of type JWT
        jwt = self.canvas.create_jwt()
        self.assertIsInstance(jwt, JWT)

        # check the token is correct and we received the right object
        self.assertEqual(jwt.token, "ZjM0UTZmLyVNSjdqb10wLV9jQSxeUiogXUlCWUs7Tg==")

    # refresh token
    def test_refresh_jwt_str(self, m):
        register_uris({"jwt": ["refresh_jwt"]}, m)

        old_token = "ZjM0UTZmLyVNSjdqb10wLV9jQSxeUiogXUlCWUs7Tg=="
        new_token = "O3MzNjpPKWc+fmFfMXRJJiEoR1VbSDVDT1IzUF1IJUpjJ3JSe0lrMHw8OUlX"

        # verify returned object is of type JWT
        jwt = self.canvas.refresh_jwt(jwt=old_token)
        self.assertIsInstance(jwt, JWT)

        # check the token is correct and we received the right object
        self.assertEqual(jwt.token, new_token)

    def test_refresh_jwt_obj(self, m):
        register_uris({"jwt": ["create_jwt", "refresh_jwt"]}, m)

        old_token = "ZjM0UTZmLyVNSjdqb10wLV9jQSxeUiogXUlCWUs7Tg=="
        new_token = "O3MzNjpPKWc+fmFfMXRJJiEoR1VbSDVDT1IzUF1IJUpjJ3JSe0lrMHw8OUlX"

        old_jwt = self.canvas.create_jwt()
        self.assertEqual(old_jwt.token, old_token)

        # verify returned object is of type JWT
        jwt = self.canvas.refresh_jwt(jwt=old_jwt)
        self.assertIsInstance(jwt, JWT)

        # check the token is correct and we received the right object
        self.assertEqual(jwt.token, new_token)

    # create_poll()
    def test_create_poll(self, m):
        register_uris({"poll": ["create_poll"]}, m)

        new_poll_q = self.canvas.create_poll([{"question": "Is this a question?"}])
        self.assertIsInstance(new_poll_q, Poll)
        self.assertTrue(hasattr(new_poll_q, "question"))

        new_poll_q_d = self.canvas.create_poll(
            [{"question": "Is this a question?"}, {"description": "This is a test."}]
        )
        self.assertIsInstance(new_poll_q_d, Poll)
        self.assertTrue(hasattr(new_poll_q_d, "question"))
        self.assertTrue(hasattr(new_poll_q_d, "description"))

    def test_create_poll_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.canvas.create_poll(polls={})

    # get_account()
    def test_get_account(self, m):
        register_uris({"account": ["get_by_id"]}, m)

        account_by_id = self.canvas.get_account(1)
        self.assertIsInstance(account_by_id, Account)

        account_by_obj = self.canvas.get_account(account_by_id)
        self.assertIsInstance(account_by_obj, Account)

    # get account calendars
    def test_get_account_calendars(self, m):
        register_uris({"account": ["get_account_calendars"]}, m)

        # Convert to list for further testing
        account_calendars = self.canvas.get_account_calendars()
        account_calendars_list = list(account_calendars)

        # Check that list contains objects of type AccountCalendar
        self.assertEqual(len(account_calendars_list), 2)
        self.assertIsInstance(account_calendars_list[0], AccountCalendar)

        # Verify contents of first object
        self.assertEqual(account_calendars_list[0].id, 1)
        self.assertEqual(account_calendars_list[0].name, "CDL")

        # Verify contents of second object
        self.assertEqual(account_calendars_list[1].id, 2)
        self.assertEqual(account_calendars_list[1].name, "DDL")

    def test_get_account_sis_id(self, m):
        register_uris({"account": ["get_by_sis_id"]}, m)

        account = self.canvas.get_account("test-sis-id", use_sis_id=True)

        self.assertIsInstance(account, Account)
        self.assertEqual(account.name, "Account From SIS")

    def test_get_account_fail(self, m):
        register_uris({"generic": ["not_found"]}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_account(settings.INVALID_ID)

    # get_accounts()
    def test_get_accounts(self, m):
        register_uris({"account": ["multiple"]}, m)

        accounts = self.canvas.get_accounts()
        account_list = [account for account in accounts]
        self.assertEqual(len(account_list), 2)

    # get_course_accounts()
    def test_get_course_accounts(self, m):
        register_uris({"account": ["multiple_course"]}, m)

        accounts = self.canvas.get_course_accounts()
        account_list = [account for account in accounts]
        self.assertEqual(len(account_list), 2)

    # get_brand_variables()
    def test_get_brand_variables(self, m):
        register_uris({"account": ["get_brand_variables"]}, m)

        variables = self.canvas.get_brand_variables()
        self.assertIsInstance(variables, dict)

    # get_course()
    def test_get_course(self, m):
        register_uris({"course": ["get_by_id"]}, m)

        course_by_id = self.canvas.get_course(1)
        self.assertIsInstance(course_by_id, Course)
        self.assertTrue(hasattr(course_by_id, "name"))

        course_by_obj = self.canvas.get_course(course_by_id)
        self.assertIsInstance(course_by_obj, Course)
        self.assertTrue(hasattr(course_by_obj, "name"))

    def test_get_course_sis_id(self, m):
        register_uris({"course": ["get_by_sis_id"]}, m)

        course = self.canvas.get_course("test-sis-id", use_sis_id=True)

        self.assertIsInstance(course, Course)
        self.assertEqual(course.name, "SIS Course")

    def test_get_course_with_start_date(self, m):
        register_uris({"course": ["start_at_date"]}, m)

        course = self.canvas.get_course(2)

        self.assertTrue(hasattr(course, "start_at"))
        self.assertIsInstance(course.start_at, str)
        self.assertTrue(hasattr(course, "start_at_date"))
        self.assertIsInstance(course.start_at_date, datetime)
        self.assertEqual(course.start_at_date.tzinfo, pytz.utc)

    def test_get_course_non_unicode_char(self, m):
        register_uris({"course": ["unicode_encode_error"]}, m)

        course = self.canvas.get_course(3)

        self.assertTrue(hasattr(course, "name"))

    def test_get_course_fail(self, m):
        register_uris({"generic": ["not_found"]}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_course(settings.INVALID_ID)

    # get_user()
    def test_get_user(self, m):
        register_uris({"user": ["get_by_id"]}, m)

        user_by_id = self.canvas.get_user(1)
        self.assertIsInstance(user_by_id, User)
        self.assertTrue(hasattr(user_by_id, "name"))

        user_by_obj = self.canvas.get_user(user_by_id)
        self.assertIsInstance(user_by_obj, User)
        self.assertTrue(hasattr(user_by_obj, "name"))

    def test_get_user_by_id_type(self, m):
        register_uris({"user": ["get_by_id_type"]}, m)

        user = self.canvas.get_user("jdoe", "sis_user_id")

        self.assertIsInstance(user, User)
        self.assertTrue(hasattr(user, "name"))

    def test_get_user_self(self, m):
        register_uris({"user": ["get_by_id_self"]}, m)

        user = self.canvas.get_user("self")

        self.assertIsInstance(user, User)
        self.assertTrue(hasattr(user, "name"))

    def test_get_user_fail(self, m):
        register_uris({"generic": ["not_found"]}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_user(settings.INVALID_ID)

    # get_courses()
    def test_get_courses(self, m):
        register_uris({"course": ["multiple", "multiple_page_2"]}, m)

        courses = self.canvas.get_courses(per_page=1)

        course_list = [course for course in courses]
        self.assertEqual(len(course_list), 4)
        self.assertIsInstance(course_list[0], Course)

    # get_activity_stream_summary()
    def test_get_activity_stream_summary(self, m):
        register_uris({"user": ["activity_stream_summary"]}, m)

        summary = self.canvas.get_activity_stream_summary()

        self.assertIsInstance(summary, list)

    # get_todo_items()
    def test_get_todo_items(self, m):
        register_uris({"user": ["todo_items"]}, m)

        todo_items = self.canvas.get_todo_items()
        todo_list = [todo for todo in todo_items]

        self.assertIsInstance(todo_list[0], Todo)

    # get_upcoming_events()
    def test_get_upcoming_events(self, m):
        register_uris({"user": ["upcoming_events"]}, m)

        events = self.canvas.get_upcoming_events()

        self.assertIsInstance(events, list)

    # get_course_nicknames()
    def test_get_course_nicknames(self, m):
        register_uris({"user": ["course_nicknames", "course_nicknames_page_2"]}, m)

        nicknames = self.canvas.get_course_nicknames()

        nickname_list = [name for name in nicknames]
        self.assertEqual(len(nickname_list), 4)
        self.assertIsInstance(nickname_list[0], CourseNickname)
        self.assertTrue(hasattr(nickname_list[0], "nickname"))

    # get_course_nickname()
    def test_get_course_nickname(self, m):
        register_uris({"course": ["get_by_id"], "user": ["course_nickname"]}, m)

        nickname_by_id = self.canvas.get_course_nickname(1)
        self.assertIsInstance(nickname_by_id, CourseNickname)
        self.assertTrue(hasattr(nickname_by_id, "nickname"))

        course_for_obj = self.canvas.get_course(1)
        nickname_by_obj = self.canvas.get_course_nickname(course_for_obj)
        self.assertIsInstance(nickname_by_obj, CourseNickname)
        self.assertTrue(hasattr(nickname_by_obj, "nickname"))

    def test_get_course_nickname_fail(self, m):
        register_uris({"generic": ["not_found"]}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.canvas.get_course_nickname(settings.INVALID_ID)

    # set_course_nickname()
    def test_set_course_nickname(self, m):
        register_uris({"course": ["get_by_id"], "user": ["course_nickname_set"]}, m)

        name = "New Course Nickname"
        nickname_by_id = self.canvas.set_course_nickname(1, name)
        self.assertIsInstance(nickname_by_id, CourseNickname)
        self.assertTrue(hasattr(nickname_by_id, "nickname"))
        self.assertEqual(nickname_by_id.nickname, name)

        course_for_obj = self.canvas.get_course(1)
        nickname_by_obj = self.canvas.set_course_nickname(course_for_obj, name)
        self.assertIsInstance(nickname_by_obj, CourseNickname)
        self.assertTrue(hasattr(nickname_by_obj, "nickname"))

    # clear_course_nicknames()
    def test_clear_course_nicknames(self, m):
        register_uris({"user": ["course_nicknames_delete"]}, m)

        success = self.canvas.clear_course_nicknames()
        self.assertTrue(success)

    # search_accounts()
    def test_search_accounts(self, m):
        register_uris({"account": ["domains"]}, m)

        domains = self.canvas.search_accounts()

        self.assertIsInstance(domains, list)
        self.assertEqual(len(domains), 1)
        self.assertIn("name", domains[0])

    # get_section()
    def test_get_section(self, m):
        register_uris({"section": ["get_by_id"]}, m)

        section_by_id = self.canvas.get_section(1)
        self.assertIsInstance(section_by_id, Section)

        section_by_obj = self.canvas.get_section(section_by_id)
        self.assertIsInstance(section_by_obj, Section)

    def test_get_section_sis_id(self, m):
        register_uris({"section": ["get_by_sis_id"]}, m)

        section = self.canvas.get_section("test-sis-id", use_sis_id=True)

        self.assertIsInstance(section, Section)
        self.assertEqual(section.name, "SIS Section")

    # create_group()
    def test_create_group(self, m):
        register_uris({"group": ["create"]}, m)

        group = self.canvas.create_group()

        self.assertIsInstance(group, Group)
        self.assertTrue(hasattr(group, "name"))
        self.assertTrue(hasattr(group, "description"))

    # get_group()
    def test_get_group(self, m):
        register_uris({"group": ["get_by_id"]}, m)

        group_by_id = self.canvas.get_group(1)
        self.assertIsInstance(group_by_id, Group)
        self.assertTrue(hasattr(group_by_id, "name"))
        self.assertTrue(hasattr(group_by_id, "description"))

        group_by_obj = self.canvas.get_group(group_by_id)
        self.assertIsInstance(group_by_obj, Group)
        self.assertTrue(hasattr(group_by_obj, "name"))
        self.assertTrue(hasattr(group_by_obj, "description"))

    def test_get_group_sis_id(self, m):
        register_uris({"group": ["get_by_sis_id"]}, m)

        group = self.canvas.get_group("test-sis-id", use_sis_id=True)

        self.assertIsInstance(group, Group)
        self.assertEqual(group.name, "SIS Group")

    # get_group_category()
    def test_get_group_category(self, m):
        register_uris({"group": ["get_category_by_id"]}, m)

        group_category_by_id = self.canvas.get_group_category(1)
        self.assertIsInstance(group_category_by_id, GroupCategory)

        group_category_by_obj = self.canvas.get_group_category(group_category_by_id)
        self.assertIsInstance(group_category_by_obj, GroupCategory)

    # create_conversation()
    def test_create_conversation(self, m):
        register_uris({"conversation": ["create_conversation"]}, m)

        recipients = ["2"]
        body = "Hello, World!"

        conversations = self.canvas.create_conversation(
            recipients=recipients, body=body
        )
        self.assertIsInstance(conversations, list)
        self.assertEqual(len(conversations), 1)
        self.assertIsInstance(conversations[0], Conversation)
        self.assertTrue(hasattr(conversations[0], "last_message"))
        self.assertEqual(conversations[0].last_message, body)

    def test_create_conversation_multiple_people(self, m):
        register_uris({"conversation": ["create_conversation_multiple"]}, m)

        recipients = ["2", "3"]
        body = "Hey guys!"

        conversations = self.canvas.create_conversation(
            recipients=recipients, body=body
        )
        self.assertIsInstance(conversations, list)
        self.assertEqual(len(conversations), 2)

        self.assertIsInstance(conversations[0], Conversation)
        self.assertTrue(hasattr(conversations[0], "last_message"))
        self.assertEqual(conversations[0].last_message, body)

        self.assertIsInstance(conversations[1], Conversation)
        self.assertTrue(hasattr(conversations[1], "last_message"))
        self.assertEqual(conversations[1].last_message, body)

    # get_conversation()
    def test_get_conversation(self, m):
        register_uris({"conversation": ["get_by_id"]}, m)

        conversation_by_id = self.canvas.get_conversation(1)
        self.assertIsInstance(conversation_by_id, Conversation)
        self.assertTrue(hasattr(conversation_by_id, "subject"))

        conversation_by_obj = self.canvas.get_conversation(conversation_by_id)
        self.assertIsInstance(conversation_by_obj, Conversation)
        self.assertTrue(hasattr(conversation_by_obj, "subject"))

    # get_conversations()
    def test_get_conversations(self, m):
        requires = {"conversation": ["get_conversations", "get_conversations_2"]}
        register_uris(requires, m)

        convos = self.canvas.get_conversations()
        conversation_list = [conversation for conversation in convos]

        self.assertEqual(len(conversation_list), 4)
        self.assertIsInstance(conversation_list[0], Conversation)

    # mark_all_as_read()
    def test_conversations_mark_all_as_read(self, m):
        register_uris({"conversation": ["mark_all_as_read"]}, m)

        result = self.canvas.conversations_mark_all_as_read()
        self.assertTrue(result)

    # unread_count()
    def test_conversations_unread_count(self, m):
        register_uris({"conversation": ["unread_count"]}, m)

        result = self.canvas.conversations_unread_count()
        self.assertEqual(result["unread_count"], "7")

    # get_running_batches()
    def test_conversations_get_running_batches(self, m):
        register_uris({"conversation": ["get_running_batches"]}, m)

        result = self.canvas.conversations_get_running_batches()
        self.assertEqual(len(result), 2)
        self.assertIn("body", result[0]["message"])
        self.assertEqual(result[1]["message"]["author_id"], 1)

    # batch_update()
    def test_conversations_batch_update(self, m):
        register_uris({"conversation": ["batch_update"]}, m)

        conversation_ids = [1, 2]
        this_event = "mark_as_read"
        result = self.canvas.conversations_batch_update(
            event=this_event, conversation_ids=conversation_ids
        )
        self.assertIsInstance(result, Progress)

    def test_conversations_batch_updated_fail_on_event(self, m):
        conversation_ids = [1, 2]
        this_event = "this doesn't work"
        with self.assertRaises(ValueError):
            self.canvas.conversations_batch_update(
                event=this_event, conversation_ids=conversation_ids
            )

    def test_conversations_batch_updated_fail_on_ids(self, m):
        conversation_ids = [None] * 501
        this_event = "mark_as_read"
        with self.assertRaises(ValueError):
            self.canvas.conversations_batch_update(
                event=this_event, conversation_ids=conversation_ids
            )

    # create_calendar_event()
    def test_create_calendar_event(self, m):
        register_uris({"calendar_event": ["create_calendar_event"]}, m)

        cal_event = {"context_code": "course_123"}
        evnt = self.canvas.create_calendar_event(calendar_event=cal_event)

        self.assertIsInstance(evnt, CalendarEvent)
        self.assertEqual(evnt.context_code, "course_123")
        self.assertEqual(evnt.id, 234)

    def test_create_calendar_event_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.canvas.create_calendar_event({})

    # get_calendar_events()
    def test_get_calendar_events(self, m):
        register_uris({"calendar_event": ["list_calendar_events"]}, m)

        cal_events = self.canvas.get_calendar_events()
        cal_event_list = [cal_event for cal_event in cal_events]
        self.assertEqual(len(cal_event_list), 2)

    # get_calendar_event()
    def test_get_calendar_event(self, m):
        register_uris({"calendar_event": ["get_calendar_event"]}, m)

        calendar_event_by_id = self.canvas.get_calendar_event(567)
        self.assertIsInstance(calendar_event_by_id, CalendarEvent)
        self.assertEqual(calendar_event_by_id.title, "Test Event 3")

        calendar_event_by_obj = self.canvas.get_calendar_event(calendar_event_by_id)
        self.assertIsInstance(calendar_event_by_obj, CalendarEvent)
        self.assertEqual(calendar_event_by_obj.title, "Test Event 3")

    # reserve_time_slot()
    def test_reserve_time_slot(self, m):
        register_uris({"calendar_event": ["reserve_time_slot"]}, m)

        calendar_event_by_id = self.canvas.reserve_time_slot(calendar_event=567)
        self.assertIsInstance(calendar_event_by_id, CalendarEvent)
        self.assertEqual(calendar_event_by_id.title, "Test Reservation")

        calendar_event_by_obj = self.canvas.reserve_time_slot(
            calendar_event=calendar_event_by_id
        )
        self.assertIsInstance(calendar_event_by_obj, CalendarEvent)
        self.assertEqual(calendar_event_by_obj.title, "Test Reservation")

    def test_reserve_time_slot_by_participant_id(self, m):
        register_uris({"calendar_event": ["reserve_time_slot_participant_id"]}, m)

        cal_event = self.canvas.reserve_time_slot(
            calendar_event=567, participant_id=777
        )
        self.assertIsInstance(cal_event, CalendarEvent)
        self.assertEqual(cal_event.title, "Test Reservation")
        self.assertEqual(cal_event.user, 777)

    # get_appointment_groups()
    def test_get_appointment_groups(self, m):
        register_uris({"appointment_group": ["list_appointment_groups"]}, m)

        appt_groups = self.canvas.get_appointment_groups()
        appt_groups_list = [appt_group for appt_group in appt_groups]
        self.assertEqual(len(appt_groups_list), 2)

    # get_appointment_group()
    def test_get_appointment_group(self, m):
        register_uris({"appointment_group": ["get_appointment_group"]}, m)

        appointment_group_by_id = self.canvas.get_appointment_group(567)
        self.assertIsInstance(appointment_group_by_id, AppointmentGroup)
        self.assertEqual(appointment_group_by_id.title, "Test Group 3")

        appointment_group_by_obj = self.canvas.get_appointment_group(
            appointment_group_by_id
        )
        self.assertIsInstance(appointment_group_by_obj, AppointmentGroup)
        self.assertEqual(appointment_group_by_obj.title, "Test Group 3")

    # create_appointment_group()
    def test_create_appointment_group(self, m):
        register_uris({"appointment_group": ["create_appointment_group"]}, m)

        evnt = self.canvas.create_appointment_group(
            {"context_codes": ["course_123"], "title": "Test Group"}
        )

        self.assertIsInstance(evnt, AppointmentGroup)
        self.assertEqual(evnt.context_codes[0], "course_123")
        self.assertEqual(evnt.id, 234)

    def test_create_appointment_group_fail_on_context_codes(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.canvas.create_appointment_group({"title": "Test Group"})

    def test_create_appointment_group_fail_on_title(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.canvas.create_appointment_group({"context_codes": "course_123"})

    # get_user_participants()
    def test_get_user_participants(self, m):
        register_uris(
            {
                "appointment_group": [
                    "get_appointment_group_222",
                    "list_user_participants",
                ]
            },
            m,
        )

        users_by_id = self.canvas.get_user_participants(222)
        users_get_by_id = [user for user in users_by_id]
        self.assertEqual(len(users_get_by_id), 2)

        appointment_group_for_obj = self.canvas.get_appointment_group(222)
        users_by_id = self.canvas.get_user_participants(appointment_group_for_obj)
        users_get_by_id = [user for user in users_by_id]
        self.assertEqual(len(users_get_by_id), 2)

    # get_group_participants()
    def test_get_group_participants(self, m):
        register_uris(
            {
                "appointment_group": [
                    "get_appointment_group_222",
                    "list_group_participants",
                ]
            },
            m,
        )

        groups_by_id = self.canvas.get_group_participants(222)
        groups_get_by_id = [group for group in groups_by_id]
        self.assertEqual(len(groups_get_by_id), 2)

        appointment_group_for_obj = self.canvas.get_appointment_group(222)
        groups_by_obj = self.canvas.get_group_participants(appointment_group_for_obj)
        groups_get_by_obj = [group for group in groups_by_obj]
        self.assertEqual(len(groups_get_by_obj), 2)

    # get_file()
    def test_get_file(self, m):
        register_uris({"file": ["get_by_id"]}, m)

        file_by_id = self.canvas.get_file(1)
        self.assertIsInstance(file_by_id, File)
        self.assertEqual(file_by_id.display_name, "File.docx")
        self.assertEqual(file_by_id.size, 6144)

        file_by_obj = self.canvas.get_file(file_by_id)
        self.assertIsInstance(file_by_obj, File)
        self.assertEqual(file_by_obj.display_name, "File.docx")
        self.assertEqual(file_by_obj.size, 6144)

    # search_recipients()
    def test_search_recipients(self, m):
        register_uris({"user": ["search_recipients"]}, m)

        recipients = self.canvas.search_recipients()
        self.assertIsInstance(recipients, list)
        self.assertEqual(len(recipients), 2)

    # search_all_courses()
    def test_search_all_courses(self, m):
        register_uris({"course": ["search_all_courses"]}, m)

        courses = self.canvas.search_all_courses()
        self.assertIsInstance(courses, list)
        self.assertEqual(len(courses), 2)

    # get_outcome()
    def test_get_outcome(self, m):
        register_uris({"outcome": ["canvas_get_outcome"]}, m)

        outcome_group_by_id = self.canvas.get_outcome(3)
        self.assertIsInstance(outcome_group_by_id, Outcome)
        self.assertEqual(outcome_group_by_id.id, 3)
        self.assertEqual(outcome_group_by_id.title, "Outcome Show Example")

        outcome_group_by_obj = self.canvas.get_outcome(outcome_group_by_id)
        self.assertIsInstance(outcome_group_by_obj, Outcome)
        self.assertEqual(outcome_group_by_obj.id, 3)
        self.assertEqual(outcome_group_by_obj.title, "Outcome Show Example")

    # get_root_outcome_group()
    def test_get_root_outcome_group(self, m):
        register_uris({"outcome": ["canvas_root_outcome_group"]}, m)

        outcome_group = self.canvas.get_root_outcome_group()
        self.assertIsInstance(outcome_group, OutcomeGroup)
        self.assertEqual(outcome_group.id, 1)
        self.assertEqual(outcome_group.title, "ROOT")

    # get_outcome_group()
    def test_get_outcome_group(self, m):
        register_uris({"outcome": ["canvas_get_outcome_group"]}, m)

        outcome_group_by_id = self.canvas.get_outcome_group(1)
        self.assertIsInstance(outcome_group_by_id, OutcomeGroup)
        self.assertEqual(outcome_group_by_id.id, 1)
        self.assertEqual(outcome_group_by_id.title, "Canvas outcome group title")

        outcome_group_by_obj = self.canvas.get_outcome_group(outcome_group_by_id)
        self.assertIsInstance(outcome_group_by_obj, OutcomeGroup)
        self.assertEqual(outcome_group_by_obj.id, 1)
        self.assertEqual(outcome_group_by_obj.title, "Canvas outcome group title")

    # get_progress()
    def test_get_progress(self, m):
        register_uris({"content_migration": ["get_progress"]}, m)

        progress = self.canvas.get_progress(1)
        self.assertIsInstance(progress, Progress)
        self.assertTrue(hasattr(progress, "id"))
        self.assertEqual(progress.id, 1)

    # get_announcements()
    def test_get_single_course_announcements(self, m):
        register_uris({"announcements": ["list_announcements"]}, m)
        announcements = self.canvas.get_announcements([1])
        announcement_list = [announcement for announcement in announcements]

        self.assertIsInstance(announcements, PaginatedList)
        self.assertIsInstance(announcement_list[0], DiscussionTopic)
        self.assertEqual(len(announcement_list), 4)

    def test_get_course_announcements_from_object(self, m):
        register_uris(
            {"course": ["get_by_id"], "announcements": ["list_announcements"]}, m
        )
        course = self.canvas.get_course(1)
        announcements = self.canvas.get_announcements([course])

        self.assertIsInstance(announcements, PaginatedList)

    def test_get_course_announcements_from_mixed_list(self, m):
        register_uris(
            {"course": ["get_by_id"], "announcements": ["list_announcements"]}, m
        )
        course = self.canvas.get_course(1)
        course_ids = [course, 2]
        announcements = self.canvas.get_announcements(course_ids)

        self.assertIsInstance(announcements, PaginatedList)

    def test_get_announcements_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.canvas.get_announcements([])
        with self.assertRaises(RequiredFieldMissing):
            self.canvas.get_announcements(1)

    def test_multiple_course_announcements(self, m):
        register_uris({"announcements": ["list_announcements"]}, m)
        announcements = self.canvas.get_announcements([1, 2])
        announcement_list = [announcement for announcement in announcements]

        self.assertEqual(announcement_list[1].context_code, "course_1")
        self.assertEqual(announcement_list[1]._parent_type, "course")
        self.assertEqual(announcement_list[1]._parent_id, "1")

        self.assertEqual(announcement_list[2].context_code, "group_1")
        self.assertEqual(announcement_list[2]._parent_type, "group")
        self.assertEqual(announcement_list[2]._parent_id, "1")

    def test_course_announcements_legacy(self, m):
        register_uris({"announcements": ["list_announcements"]}, m)
        announcements = self.canvas.get_announcements(context_codes=["course_1"])

        self.assertEqual(announcements[0].context_code, "course_1")
        self.assertEqual(announcements[0]._parent_type, "course")
        self.assertEqual(announcements[0]._parent_id, "1")

    # get_eportfolio()
    def test_get_eportfolio(self, m):
        register_uris({"eportfolio": ["get_eportfolio_by_id"]}, m)

        eportfolio = self.canvas.get_eportfolio(1)

        self.assertIsInstance(eportfolio, EPortfolio)
        self.assertEqual(eportfolio.name, "ePortfolio 1")

    # get_epub_exports()
    def test_get_epub_exports(self, m):
        register_uris({"course": ["get_epub_exports"]}, m)

        epub_export_list = self.canvas.get_epub_exports()

        self.assertIsInstance(epub_export_list, PaginatedList)
        self.assertIsInstance(epub_export_list[0], CourseEpubExport)
        self.assertIsInstance(epub_export_list[1], CourseEpubExport)
        self.assertEqual(epub_export_list[0].id, 1)
        self.assertEqual(epub_export_list[1].id, 2)
        self.assertEqual(epub_export_list[0].name, "course1")
        self.assertEqual(epub_export_list[1].name, "course2")

        self.assertTrue(hasattr(epub_export_list[0], "epub_export"))
        self.assertTrue(hasattr(epub_export_list[1], "epub_export"))

        epub1 = epub_export_list[0].epub_export
        epub2 = epub_export_list[1].epub_export
        self.assertEqual(epub1["id"], 1)
        self.assertEqual(epub2["id"], 2)
        self.assertEqual(epub1["workflow_state"], "exported")
        self.assertEqual(epub2["workflow_state"], "exported")

    # comm_messages()
    def test_get_comm_messages(self, m):
        register_uris({"comm_message": ["comm_messages"]}, m)

        comm_messages = self.canvas.get_comm_messages(2)

        self.assertIsInstance(comm_messages, PaginatedList)
        self.assertIsInstance(comm_messages[0], CommMessage)
        self.assertIsInstance(comm_messages[1], CommMessage)

        self.assertTrue(hasattr(comm_messages[0], "id"))
        self.assertTrue(hasattr(comm_messages[1], "body"))

        self.assertEqual(comm_messages[0].id, 42)
        self.assertEqual(comm_messages[0].subject, "example subject line")
        self.assertEqual(comm_messages[1].id, 2)
        self.assertEqual(comm_messages[1].subject, "My Subject")

    def test_graphql(self, m):
        register_uris({"graphql": ["graphql"]}, m, base_url=settings.BASE_URL_GRAPHQL)
        query = """
        query MyQuery($termid: ID!) {
            term(id: $termid) {
                coursesConnection {
                    nodes {
                        _id
                        assignmentsConnection {
                        nodes {
                            name
                            _id
                            expectsExternalSubmission
                        }
                        }
                    }
                    edges {
                        node {
                        id
                        }
                    }
                }
            }
        }
        """
        variables = {"termid": 125}

        graphql_response = self.canvas.graphql(query=query, variables=variables)
        # Just a super simple check right now that it gets back a dict respose
        self.assertIsInstance(graphql_response, dict)
