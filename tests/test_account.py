import datetime
import unittest

import pytz
import requests_mock

from canvasapi import Canvas
from canvasapi.account import (
    Account,
    AccountNotification,
    AccountReport,
    Admin,
    Role,
    SSOSettings,
)
from canvasapi.account_calendar import AccountCalendar
from canvasapi.authentication_event import AuthenticationEvent
from canvasapi.authentication_provider import AuthenticationProvider
from canvasapi.content_migration import ContentMigration, Migrator
from canvasapi.course import Course
from canvasapi.course_event import CourseEvent
from canvasapi.enrollment import Enrollment
from canvasapi.enrollment_term import EnrollmentTerm
from canvasapi.exceptions import CanvasException, RequiredFieldMissing
from canvasapi.external_tool import ExternalTool
from canvasapi.feature import Feature, FeatureFlag
from canvasapi.grading_period import GradingPeriod
from canvasapi.grading_standard import GradingStandard
from canvasapi.group import Group, GroupCategory
from canvasapi.login import Login
from canvasapi.outcome import OutcomeGroup, OutcomeLink
from canvasapi.outcome_import import OutcomeImport
from canvasapi.paginated_list import PaginatedList
from canvasapi.rubric import Rubric
from canvasapi.scope import Scope
from canvasapi.sis_import import SisImport
from canvasapi.user import User
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestAccount(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {"account": ["get_by_id", "get_role"], "user": ["get_by_id"]}
            register_uris(requires, m)

            self.account = self.canvas.get_account(1)
            self.user = self.canvas.get_user(1)
            self.role = self.account.get_role(2)

    # __str__()
    def test__str__(self, m):
        string = str(self.account)
        self.assertIsInstance(string, str)

    # get_global_notification()
    def test_get_global_notification(self, m):
        register_uris({"account": ["get_notification"]}, m)

        notif_id = 1
        notification = self.account.get_global_notification(notif_id)

        self.assertIsInstance(notification, AccountNotification)
        self.assertTrue(hasattr(notification, "subject"))
        self.assertEqual(notification.subject, "Attention Students")

    # create_account()
    def test_create_account(self, m):
        register_uris({"account": ["create_2"]}, m)

        new_account = self.account.create_account()

        self.assertIsInstance(new_account, Account)
        self.assertTrue(hasattr(new_account, "id"))

    # create_course()
    def test_create_course(self, m):
        register_uris({"account": ["create_course"]}, m)

        course = self.account.create_course()

        self.assertIsInstance(course, Course)
        self.assertTrue(hasattr(course, "name"))

    # create_subaccount()
    def test_create_subaccount(self, m):
        register_uris({"account": ["create_subaccount"]}, m)

        subaccount_name = "New Subaccount"
        subaccount = self.account.create_subaccount({"name": subaccount_name})

        self.assertIsInstance(subaccount, Account)
        self.assertTrue(hasattr(subaccount, "name"))
        self.assertEqual(subaccount.name, subaccount_name)
        self.assertTrue(hasattr(subaccount, "root_account_id"))
        self.assertEqual(subaccount.root_account_id, self.account.id)

    def test_create_course_missing_field(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.account.create_subaccount({})

    # create_user()
    def test_create_user(self, m):
        register_uris({"account": ["create_user"]}, m)

        unique_id = 123456
        user = self.account.create_user({"unique_id": unique_id})

        self.assertIsInstance(user, User)
        self.assertTrue(hasattr(user, "unique_id"))
        self.assertEqual(user.unique_id, unique_id)

    def test_create_user_missing_field(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.account.create_user({})

    # create_notification()
    def test_create_notification(self, m):
        register_uris({"account": ["create_notification"]}, m)

        subject = "Subject"
        notif_dict = {
            "subject": subject,
            "message": "Message",
            "start_at": "2015-04-01T00:00:00Z",
            "end_at": "2018-04-01T00:00:00Z",
        }
        notif = self.account.create_notification(notif_dict)

        self.assertIsInstance(notif, AccountNotification)
        self.assertTrue(hasattr(notif, "subject"))
        self.assertEqual(notif.subject, subject)
        self.assertTrue(hasattr(notif, "start_at_date"))
        self.assertIsInstance(notif.start_at_date, datetime.datetime)
        self.assertEqual(notif.start_at_date.tzinfo, pytz.utc)

    def test_create_notification_missing_field(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.account.create_notification({})

    # delete()
    def test_delete(self, m):
        register_uris({"account": ["create_subaccount", "delete_subaccount"]}, m)

        subaccount = self.account.create_subaccount({"name": "New Subaccount"})

        self.assertTrue(subaccount.delete())

    def test_delete_root_account(self, m):
        with self.assertRaises(CanvasException):
            self.account.delete()

    # delete_admin()
    def test_delete_admin(self, m):
        register_uris({"account": ["delete_admin"]}, m)

        user_id = 123
        deleted_admin = self.account.delete_admin(user=user_id)

        self.assertIsInstance(deleted_admin, Admin)
        self.assertTrue(hasattr(deleted_admin, "id"))
        self.assertTrue(hasattr(deleted_admin, "role"))
        self.assertTrue(hasattr(deleted_admin, "role_id"))
        self.assertTrue(hasattr(deleted_admin, "workflow_state"))
        self.assertEqual(deleted_admin.user["login_id"], "jdoe")
        self.assertEqual(deleted_admin.role, "AccountAdmin")
        self.assertEqual(deleted_admin.role_id, 1)
        self.assertEqual(deleted_admin.workflow_state, "deleted")

    # delete_user()
    def test_delete_user_id(self, m):
        register_uris({"account": ["delete_user"]}, m)

        deleted_user = self.account.delete_user(self.user.id)

        self.assertIsInstance(deleted_user, User)
        self.assertTrue(hasattr(deleted_user, "name"))

    def test_delete_user_obj(self, m):
        register_uris({"account": ["delete_user"]}, m)

        deleted_user = self.account.delete_user(self.user)

        self.assertIsInstance(deleted_user, User)
        self.assertTrue(hasattr(deleted_user, "name"))

    # get_courses()
    def test_get_courses(self, m):
        required = {"account": ["get_courses", "get_courses_page_2"]}
        register_uris(required, m)

        courses = self.account.get_courses()

        course_list = [course for course in courses]
        self.assertEqual(len(course_list), 4)
        self.assertIsInstance(course_list[0], Course)
        self.assertTrue(hasattr(course_list[0], "name"))

    # get_external_tool()
    def test_get_external_tool(self, m):
        required = {"external_tool": ["get_by_id_account"]}
        register_uris(required, m)

        tool_by_id = self.account.get_external_tool(1)
        self.assertIsInstance(tool_by_id, ExternalTool)
        self.assertTrue(hasattr(tool_by_id, "name"))

        tool_by_obj = self.account.get_external_tool(tool_by_id)
        self.assertIsInstance(tool_by_obj, ExternalTool)
        self.assertTrue(hasattr(tool_by_obj, "name"))

    # get_external_tools()
    def test_get_external_tools(self, m):
        required = {"account": ["get_external_tools", "get_external_tools_p2"]}
        register_uris(required, m)

        tools = self.account.get_external_tools()
        tool_list = [tool for tool in tools]

        self.assertIsInstance(tool_list[0], ExternalTool)
        self.assertEqual(len(tool_list), 4)

    # create_report
    def test_create_report(self, m):
        required = {"account": ["create_report"]}
        register_uris(required, m)

        report_template = {
            "title": "Zero Activity",
            "parameters": {
                "enrollment_term_id": {
                    "required": False,
                    "description": "The canvas id of the term to get grades from",
                },
                "start_at": {
                    "required": False,
                    "description": "The first date in the date range",
                },
                "course_id": {
                    "required": False,
                    "description": "The course to report on",
                },
            },
            "report": "zero_activity_csv",
            "last_run": "null",
        }

        report = self.account.create_report(
            "zero_activity_csv", parameters=report_template
        )

        self.assertIsInstance(report, AccountReport)
        self.assertTrue(hasattr(report, "title"))
        self.assertEqual(report.title, "Zero Activity")

    # delete_report
    def test_delete_report(self, m):
        required = {"account": ["delete_report"]}
        register_uris(required, m)

        self.account_report = AccountReport(
            self.canvas._Canvas__requester,
            {
                "title": "Zero Activity",
                "parameters": {
                    "enrollment_term_id": {
                        "required": False,
                        "description": "The canvas id of the term to get grades from",
                    },
                    "start_at": {
                        "required": False,
                        "description": "The first date in the date range",
                    },
                    "course_id": {
                        "required": False,
                        "description": "The course to report on",
                    },
                },
                "report": "zero_activity_csv",
                "last_run": "null",
                "account_id": 1,
                "id": 1,
            },
        )

        report = self.account_report.delete_report()

        self.assertIsInstance(report, AccountReport)
        self.assertTrue(hasattr(report, "status"))
        self.assertEqual(report.status, "deleted")

    # get account calendar
    def test_get_account_calendar(self, m):
        register_uris({"account": ["get_account_calendar"]}, m)

        # Check object is of type AccountCalendar
        account_calendar = self.account.get_account_calendar()
        self.assertIsInstance(account_calendar, AccountCalendar)

        # Verify contents of object
        self.assertEqual(account_calendar.id, 10)
        self.assertEqual(account_calendar.name, "Department of Computer Science")

    # get all account calendars
    def test_get_all_account_calendars(self, m):
        register_uris({"account": ["get_all_account_calendars"]}, m)

        # Get paginated list and convert to list
        account_calendars = self.account.get_all_account_calendars()
        account_calendars_list = list(account_calendars)

        # Check that list contains objects of type AccountCalendar
        self.assertEqual(len(account_calendars_list), 2)
        self.assertIsInstance(account_calendars_list[0], AccountCalendar)
        self.assertIsInstance(account_calendars_list[1], AccountCalendar)

        # Verify contents of first object
        self.assertEqual(account_calendars_list[0].id, 1)
        self.assertEqual(account_calendars_list[0].name, "FSU")

        # Verify contents of second object
        self.assertEqual(account_calendars_list[1].id, 2)
        self.assertEqual(account_calendars_list[1].name, "Full Sail")

    # get_report
    def test_get_report(self, m):
        required = {"account": ["get_report"]}
        register_uris(required, m)

        report = self.account.get_report("zero_activity_csv", 1)

        self.assertIsInstance(report, AccountReport)
        self.assertTrue(hasattr(report, "title"))
        self.assertEqual(report.title, "Zero Activity")
        self.assertIsInstance(str(report), str)

    # get_index_of_reports()
    def test_get_index_of_reports(self, m):
        required = {"account": ["report_index", "report_index_page_2"]}
        register_uris(required, m)

        reports_index = self.account.get_index_of_reports("sis_export_csv")

        reports_index_list = [index for index in reports_index]
        self.assertEqual(len(reports_index_list), 4)
        self.assertIsInstance(reports_index_list[0], AccountReport)
        self.assertTrue(hasattr(reports_index_list[0], "id"))

    # get_reports()
    def test_get_reports(self, m):
        required = {"account": ["reports", "reports_page_2"]}
        register_uris(required, m)

        reports = self.account.get_reports()

        reports_list = [report for report in reports]
        self.assertEqual(len(reports_list), 4)
        self.assertIsInstance(reports_list[0], AccountReport)
        self.assertTrue(hasattr(reports_list[0], "id"))
        self.assertIsInstance(str(reports_list[0]), str)

    # get query by account
    def test_query_audit_by_account(self, m):
        register_uris({"account": ["query_audit_by_account"]}, m)

        # Get paginated list and convert to list
        query = self.account.query_audit_by_account()
        query_list = list(query)

        # Check that list contains objects of type CourseEvent
        self.assertEqual(len(query_list), 2)
        self.assertIsInstance(query_list[0], CourseEvent)
        self.assertIsInstance(query_list[1], CourseEvent)

        # Verify contents of first object
        self.assertEqual(query_list[0].id, 1)
        self.assertEqual(query_list[0].name, "UCF")

        # Verify contents of second object
        self.assertEqual(query_list[1].id, 2)
        self.assertEqual(query_list[1].name, "FSU")

    # get_subaccounts()
    def test_get_subaccounts(self, m):
        required = {"account": ["subaccounts", "subaccounts_page_2"]}
        register_uris(required, m)

        subaccounts = self.account.get_subaccounts()

        subaccounts_list = [account for account in subaccounts]
        self.assertEqual(len(subaccounts_list), 4)
        self.assertIsInstance(subaccounts_list[0], Account)
        self.assertTrue(hasattr(subaccounts_list[0], "name"))

    # get_users()
    def test_get_users(self, m):
        required = {"account": ["users", "users_page_2"]}
        register_uris(required, m)

        users = self.account.get_users()

        user_list = [user for user in users]
        self.assertEqual(len(user_list), 4)
        self.assertIsInstance(user_list[0], User)
        self.assertTrue(hasattr(user_list[0], "name"))

    # get_user_notifications()
    def test_get_user_notifications_id(self, m):
        required = {"account": ["user_notifs", "user_notifs_page_2"]}
        register_uris(required, m)

        user_notifs = self.account.get_user_notifications(self.user.id)

        notif_list = [notif for notif in user_notifs]
        self.assertEqual(len(notif_list), 4)
        self.assertIsInstance(user_notifs[0], AccountNotification)
        self.assertTrue(hasattr(user_notifs[0], "subject"))

    def test_get_user_notifications_obj(self, m):
        required = {"account": ["user_notifs", "user_notifs_page_2"]}
        register_uris(required, m)

        user_notifs = self.account.get_user_notifications(self.user)

        notif_list = [notif for notif in user_notifs]
        self.assertEqual(len(notif_list), 4)
        self.assertIsInstance(user_notifs[0], AccountNotification)
        self.assertTrue(hasattr(user_notifs[0], "subject"))

    # update()
    def test_update(self, m):
        register_uris({"account": ["update"]}, m)

        self.assertEqual(self.account.name, "Canvas Account")

        new_name = "Updated Name"
        update_account_dict = {"name": new_name}

        self.assertTrue(self.account.update(account=update_account_dict))
        self.assertEqual(self.account.name, new_name)

    def test_update_fail(self, m):
        register_uris({"account": ["update_fail"]}, m)

        self.assertEqual(self.account.name, "Canvas Account")

        new_name = "Updated Name"
        update_account_dict = {"name": new_name}

        self.assertFalse(self.account.update(account=update_account_dict))

    # get_roles()
    def test_get_roles(self, m):
        requires = {"account": ["get_roles", "get_roles_2"]}
        register_uris(requires, m)

        roles = self.account.get_roles()
        role_list = [role for role in roles]

        self.assertEqual(len(role_list), 4)
        self.assertIsInstance(role_list[0], Role)
        self.assertTrue(hasattr(role_list[0], "role"))
        self.assertTrue(hasattr(role_list[0], "label"))

    def test_get_role(self, m):
        register_uris({"account": ["get_role"]}, m)

        target_role_by_id = self.account.get_role(2)
        self.assertIsInstance(target_role_by_id, Role)
        self.assertTrue(hasattr(target_role_by_id, "role"))
        self.assertTrue(hasattr(target_role_by_id, "label"))

        target_role_by_obj = self.account.get_role(self.role)
        self.assertIsInstance(target_role_by_obj, Role)
        self.assertTrue(hasattr(target_role_by_obj, "role"))
        self.assertTrue(hasattr(target_role_by_obj, "label"))

    def test_create_role(self, m):
        register_uris({"account": ["create_role"]}, m)

        new_role = self.account.create_role(1)
        self.assertIsInstance(new_role, Role)
        self.assertTrue(hasattr(new_role, "role"))
        self.assertTrue(hasattr(new_role, "label"))

    def test_deactivate_role(self, m):
        register_uris({"account": ["deactivate_role"]}, m)

        old_role_by_id = self.account.deactivate_role(2)
        self.assertIsInstance(old_role_by_id, Role)
        self.assertTrue(hasattr(old_role_by_id, "role"))
        self.assertTrue(hasattr(old_role_by_id, "label"))

        old_role_by_obj = self.account.deactivate_role(self.role)
        self.assertIsInstance(old_role_by_obj, Role)
        self.assertTrue(hasattr(old_role_by_obj, "role"))
        self.assertTrue(hasattr(old_role_by_obj, "label"))

    def test_activate_role(self, m):
        register_uris({"account": ["activate_role"]}, m)

        activated_role_by_id = self.account.activate_role(2)
        self.assertIsInstance(activated_role_by_id, Role)
        self.assertTrue(hasattr(activated_role_by_id, "role"))
        self.assertTrue(hasattr(activated_role_by_id, "label"))

        activated_role_by_obj = self.account.activate_role(self.role)
        self.assertIsInstance(activated_role_by_obj, Role)
        self.assertTrue(hasattr(activated_role_by_obj, "role"))
        self.assertTrue(hasattr(activated_role_by_obj, "label"))

    def test_update_role(self, m):
        register_uris({"account": ["update_role"]}, m)

        updated_role_by_id = self.account.update_role(2)
        self.assertIsInstance(updated_role_by_id, Role)
        self.assertTrue(hasattr(updated_role_by_id, "role"))
        self.assertTrue(hasattr(updated_role_by_id, "label"))

        updated_role_by_obj = self.account.update_role(self.role)
        self.assertIsInstance(updated_role_by_obj, Role)
        self.assertTrue(hasattr(updated_role_by_obj, "role"))
        self.assertTrue(hasattr(updated_role_by_obj, "label"))

    # get_enrollment()
    def test_get_enrollment(self, m):
        register_uris({"enrollment": ["get_by_id"]}, m)

        enrollment_by_id = self.account.get_enrollment(1)
        self.assertIsInstance(enrollment_by_id, Enrollment)

        enrollment_by_obj = self.account.get_enrollment(enrollment_by_id)
        self.assertIsInstance(enrollment_by_obj, Enrollment)

    # get_groups()
    def test_get_groups(self, m):
        requires = {"account": ["get_groups_context", "get_groups_context2"]}
        register_uris(requires, m)

        groups = self.account.get_groups()
        group_list = [group for group in groups]

        self.assertIsInstance(group_list[0], Group)
        self.assertEqual(len(group_list), 4)

    # create_group_category()
    def test_create_group_category(self, m):
        register_uris({"account": ["create_group_category"]}, m)

        name_str = "Test String"
        response = self.account.create_group_category(name=name_str)
        self.assertIsInstance(response, GroupCategory)

    # get_group_categories()
    def test_get_group_categories(self, m):
        register_uris({"account": ["get_group_categories"]}, m)

        response = self.account.get_group_categories()
        category_list = [category for category in response]

        self.assertIsInstance(category_list[0], GroupCategory)

    # create_external_tool()
    def test_create_external_tool(self, m):
        register_uris({"external_tool": ["create_tool_account"]}, m)

        response = self.account.create_external_tool(
            name="External Tool - Account",
            privacy_level="public",
            consumer_key="key",
            shared_secret="secret",
        )

        self.assertIsInstance(response, ExternalTool)
        self.assertTrue(hasattr(response, "id"))
        self.assertEqual(response.id, 10)

    # create_enrollment_term()
    def test_create_enrollment_term(self, m):
        register_uris({"enrollment_term": ["create_enrollment_term"]}, m)

        evnt = self.account.create_enrollment_term(name="Test Enrollment Term", id=45)

        self.assertIsInstance(evnt, EnrollmentTerm)
        self.assertEqual(evnt.name, "Test Enrollment Term")
        self.assertEqual(evnt.id, 45)

    # get_enrollment_term()
    def test_get_enrollment_term(self, m):
        register_uris({"account": ["get_enrollment_term"]}, m)

        enrollment_term = self.account.get_enrollment_term(1)

        self.assertIsInstance(enrollment_term, EnrollmentTerm)

        self.assertTrue(hasattr(enrollment_term, "id"))
        self.assertEqual(enrollment_term.id, 1)
        self.assertTrue(hasattr(enrollment_term, "name"))
        self.assertEqual(enrollment_term.name, "Enrollment Term 1")

    # get_enrollment_terms()
    def test_get_enrollment_terms(self, m):
        register_uris({"account": ["get_enrollment_terms"]}, m)

        response = self.account.get_enrollment_terms()
        enrollment_terms_list = [category for category in response]

        self.assertIsInstance(enrollment_terms_list[0], EnrollmentTerm)

    # get_user_logins()
    def test_get_user_logins(self, m):
        requires = {"account": ["get_user_logins", "get_user_logins_2"]}
        register_uris(requires, m)

        response = self.account.get_user_logins()
        login_list = [login for login in response]

        self.assertIsInstance(login_list[0], Login)
        self.assertEqual(len(login_list), 2)

    # create_user_login()
    def test_create_user_login(self, m):
        register_uris({"login": ["create_user_login"]}, m)

        unique_id = "belieber@example.com"

        response = self.account.create_user_login(
            user={"id": 1}, login={"unique_id": unique_id}
        )

        self.assertIsInstance(response, Login)
        self.assertTrue(hasattr(response, "id"))
        self.assertTrue(hasattr(response, "unique_id"))
        self.assertEqual(response.id, 101)
        self.assertEqual(response.unique_id, unique_id)

    def test_create_user_login_fail_on_user_id(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.account.create_user_login(user={}, login={})

    def test_create_user_login_fail_on_login_unique_id(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.account.create_user_login(user={"id": 1}, login={})

    # get_department_level_participation_data_with_given_term()
    def test_get_department_level_participation_data_with_given_term(self, m):
        register_uris(
            {"account": ["get_department_level_participation_data_with_given_term"]}, m
        )

        response = self.account.get_department_level_participation_data_with_given_term(
            1
        )

        self.assertIsInstance(response, list)

    # get_department_level_participation_data_current()
    def test_get_department_level_participation_data_current(self, m):
        register_uris(
            {"account": ["get_department_level_participation_data_current"]}, m
        )

        response = self.account.get_department_level_participation_data_current()

        self.assertIsInstance(response, list)

    # get_department_level_participation_data_completed()
    def test_get_department_level_participation_data_completed(self, m):
        register_uris(
            {"account": ["get_department_level_participation_data_completed"]}, m
        )

        response = self.account.get_department_level_participation_data_completed()

        self.assertIsInstance(response, list)

    # get_department_level_grade_data_with_given_term()
    def test_get_department_level_grade_data_with_given_term(self, m):
        register_uris(
            {"account": ["get_department_level_grade_data_with_given_term"]}, m
        )

        response = self.account.get_department_level_grade_data_with_given_term(1)

        self.assertIsInstance(response, list)

    # get_department_level_grade_data_current()
    def test_get_department_level_grade_data_current(self, m):
        register_uris({"account": ["get_department_level_grade_data_current"]}, m)

        response = self.account.get_department_level_grade_data_current()

        self.assertIsInstance(response, list)

    # get_department_level_grade_data_completed()
    def test_get_department_level_grade_data_completed(self, m):
        register_uris({"account": ["get_department_level_grade_data_completed"]}, m)

        response = self.account.get_department_level_grade_data_completed()

        self.assertIsInstance(response, list)

    # get_department_level_statistics_with_given_term()
    def test_get_department_level_statistics_with_given_term(self, m):
        register_uris(
            {"account": ["get_department_level_statistics_with_given_term"]}, m
        )

        response = self.account.get_department_level_statistics_with_given_term(1)

        self.assertIsInstance(response, list)

    # get_department_level_statistics_current()
    def test_get_department_level_statistics_current(self, m):
        register_uris({"account": ["get_department_level_statistics_current"]}, m)

        response = self.account.get_department_level_statistics_current()

        self.assertIsInstance(response, list)

    # get_department_level_statistics_completed()
    def test_get_department_level_statistics_completed(self, m):
        register_uris({"account": ["get_department_level_statistics_completed"]}, m)

        response = self.account.get_department_level_statistics_completed()

        self.assertIsInstance(response, list)

    # get_authentication_providers()
    def test_get_authentication_providers(self, m):
        requires = {
            "account": [
                "list_authentication_providers",
                "list_authentication_providers_2",
            ]
        }
        register_uris(requires, m)

        authentication_providers = self.account.get_authentication_providers()
        authentication_providers_list = [
            authentication_provider
            for authentication_provider in authentication_providers
        ]

        self.assertEqual(len(authentication_providers_list), 4)
        self.assertIsInstance(authentication_providers_list[0], AuthenticationProvider)
        self.assertTrue(hasattr(authentication_providers_list[0], "auth_type"))
        self.assertTrue(hasattr(authentication_providers_list[0], "position"))

    # add_authentication_providers()
    def test_add_authentication_providers(self, m):
        register_uris({"account": ["add_authentication_providers"]}, m)

        new_authentication_provider = self.account.add_authentication_providers()

        self.assertIsInstance(new_authentication_provider, AuthenticationProvider)
        self.assertTrue(hasattr(new_authentication_provider, "auth_type"))
        self.assertTrue(hasattr(new_authentication_provider, "position"))

    # get_authentication_provider()
    def test_get_authentication_provider(self, m):
        register_uris({"account": ["get_authentication_providers"]}, m)

        authentication_provider_by_id = self.account.get_authentication_provider(1)
        self.assertIsInstance(authentication_provider_by_id, AuthenticationProvider)

        authentication_provider_by_obj = self.account.get_authentication_provider(
            authentication_provider_by_id
        )
        self.assertIsInstance(authentication_provider_by_obj, AuthenticationProvider)

    # show_account_auth_settings()
    def test_show_account_auth_settings(self, m):
        register_uris({"account": ["show_account_auth_settings"]}, m)

        response = self.account.show_account_auth_settings()

        self.assertIsInstance(response, SSOSettings)

    # update_account_auth_settings()
    def test_update_account_auth_settings(self, m):
        register_uris({"account": ["update_account_auth_settings"]}, m)

        response = self.account.update_account_auth_settings()

        self.assertIsInstance(response, SSOSettings)

    # get_root_outcome_group()
    def test_get_root_outcome_group(self, m):
        register_uris({"outcome": ["account_root_outcome_group"]}, m)

        outcome_group = self.account.get_root_outcome_group()

        self.assertIsInstance(outcome_group, OutcomeGroup)
        self.assertEqual(outcome_group.id, 1)
        self.assertEqual(outcome_group.title, "ROOT")

    # get_outcome_group()
    def test_get_outcome_group(self, m):
        register_uris({"outcome": ["account_get_outcome_group"]}, m)

        outcome_group_by_id = self.account.get_outcome_group(1)
        self.assertIsInstance(outcome_group_by_id, OutcomeGroup)
        self.assertEqual(outcome_group_by_id.id, 1)
        self.assertEqual(outcome_group_by_id.title, "Account outcome group title")

        outcome_group_by_obj = self.account.get_outcome_group(outcome_group_by_id)
        self.assertIsInstance(outcome_group_by_obj, OutcomeGroup)
        self.assertEqual(outcome_group_by_obj.id, 1)
        self.assertEqual(outcome_group_by_obj.title, "Account outcome group title")

    # get_outcome_groups_in_context()
    def test_get_outcome_groups_in_context(self, m):
        register_uris({"outcome": ["account_outcome_groups_in_context"]}, m)

        outcome_group_list = self.account.get_outcome_groups_in_context()

        self.assertIsInstance(outcome_group_list[0], OutcomeGroup)
        self.assertEqual(outcome_group_list[0].id, 1)
        self.assertEqual(outcome_group_list[0].title, "ROOT")

    # get_all_outcome_links_in_context()
    def test_get_outcome_links_in_context(self, m):
        register_uris({"outcome": ["account_outcome_links_in_context"]}, m)

        outcome_link_list = self.account.get_all_outcome_links_in_context()

        self.assertIsInstance(outcome_link_list[0], OutcomeLink)
        self.assertEqual(outcome_link_list[0].outcome_group["id"], 2)
        self.assertEqual(outcome_link_list[0].outcome_group["title"], "test outcome")

    # add_grading_standards()
    def test_add_grading_standards(self, m):
        register_uris({"account": ["add_grading_standards"]}, m)

        title = "Grading Standard 1"
        grading_scheme = []
        grading_scheme.append({"name": "A", "value": 90})
        grading_scheme.append({"name": "B", "value": 80})
        grading_scheme.append({"name": "C", "value": 70})

        response = self.account.add_grading_standards(title, grading_scheme)

        self.assertIsInstance(response, GradingStandard)
        self.assertTrue(hasattr(response, "title"))
        self.assertEqual(title, response.title)
        self.assertTrue(hasattr(response, "grading_scheme"))
        self.assertEqual(response.grading_scheme[0].get("name"), "A")
        self.assertEqual(response.grading_scheme[0].get("value"), 0.9)

    # add_grading_standards()
    def test_add_grading_standards_empty_list(self, m):
        register_uris({"account": ["add_grading_standards"]}, m)
        with self.assertRaises(ValueError):
            self.account.add_grading_standards("title", [])

    def test_add_grading_standards_non_dict_list(self, m):
        register_uris({"account": ["add_grading_standards"]}, m)
        with self.assertRaises(ValueError):
            self.account.add_grading_standards("title", [1, 2, 3])

    def test_add_grading_standards_missing_value_key(self, m):
        register_uris({"account": ["add_grading_standards"]}, m)
        with self.assertRaises(ValueError):
            self.account.add_grading_standards("title", [{"name": "test"}])

    def test_add_grading_standards_missing_name_key(self, m):
        register_uris({"account": ["add_grading_standards"]}, m)
        with self.assertRaises(ValueError):
            self.account.add_grading_standards("title", [{"value": 2}])

    # get_grading_standards()
    def test_get_grading_standards(self, m):
        register_uris({"account": ["get_grading_standards"]}, m)

        standards = self.account.get_grading_standards()
        standard_list = [standard for standard in standards]
        self.assertEqual(len(standard_list), 2)
        self.assertIsInstance(standard_list[0], GradingStandard)
        self.assertIsInstance(standard_list[1], GradingStandard)

    # get_single_grading_standards()
    def test_get_single_grading_standard(self, m):
        register_uris({"account": ["get_single_grading_standard"]}, m)

        response = self.account.get_single_grading_standard(1)

        self.assertIsInstance(response, GradingStandard)
        self.assertTrue(hasattr(response, "id"))
        self.assertEqual(1, response.id)
        self.assertTrue(hasattr(response, "title"))
        self.assertEqual("Grading Standard 1", response.title)
        self.assertTrue(hasattr(response, "grading_scheme"))
        self.assertEqual(response.grading_scheme[0].get("name"), "A")
        self.assertEqual(response.grading_scheme[0].get("value"), 0.9)

    # get_rubric
    def test_get_rubric(self, m):
        register_uris({"account": ["get_rubric_single"]}, m)

        rubric_id = 1
        rubric = self.account.get_rubric(rubric_id)

        self.assertIsInstance(rubric, Rubric)
        self.assertEqual(rubric.id, rubric_id)
        self.assertEqual(rubric.title, "Account Rubric 1")

    # get_rubrics
    def test_get_rubrics(self, m):
        register_uris({"account": ["get_rubric_multiple"]}, m)

        rubrics = self.account.get_rubrics()

        self.assertEqual(len(list(rubrics)), 2)

        self.assertIsInstance(rubrics[0], Rubric)
        self.assertEqual(rubrics[0].id, 1)
        self.assertEqual(rubrics[0].title, "Account Rubric 1")
        self.assertIsInstance(rubrics[1], Rubric)
        self.assertEqual(rubrics[1].id, 2)
        self.assertEqual(rubrics[1].title, "Account Rubric 2")

    # create_content_migration
    def test_create_content_migration(self, m):
        register_uris({"account": ["create_content_migration"]}, m)

        content_migration = self.account.create_content_migration("dummy_importer")

        self.assertIsInstance(content_migration, ContentMigration)
        self.assertTrue(hasattr(content_migration, "migration_type"))

    def test_create_content_migration_migrator(self, m):
        register_uris(
            {"account": ["create_content_migration", "get_migration_systems_multiple"]},
            m,
        )

        migrators = self.account.get_migration_systems()
        content_migration = self.account.create_content_migration(migrators[0])

        self.assertIsInstance(content_migration, ContentMigration)
        self.assertTrue(hasattr(content_migration, "migration_type"))

    def test_create_content_migration_bad_migration_type(self, m):
        register_uris({"account": ["create_content_migration"]}, m)

        with self.assertRaises(TypeError):
            self.account.create_content_migration(1)

    # get_content_migration
    def test_get_content_migration(self, m):
        register_uris({"account": ["get_content_migration_single"]}, m)

        content_migration = self.account.get_content_migration(1)

        self.assertIsInstance(content_migration, ContentMigration)
        self.assertTrue(hasattr(content_migration, "migration_type"))

    # get_content_migrations
    def test_get_content_migrations(self, m):
        register_uris({"account": ["get_content_migration_multiple"]}, m)

        content_migrations = self.account.get_content_migrations()

        self.assertEqual(len(list(content_migrations)), 2)

        self.assertIsInstance(content_migrations[0], ContentMigration)
        self.assertEqual(content_migrations[0].id, 1)
        self.assertEqual(content_migrations[0].migration_type, "dummy_importer")
        self.assertIsInstance(content_migrations[1], ContentMigration)
        self.assertEqual(content_migrations[1].id, 2)
        self.assertEqual(content_migrations[1].migration_type, "dummy_importer")

    # get_migration_systems
    def test_get_migration_systems(self, m):
        register_uris({"account": ["get_migration_systems_multiple"]}, m)

        migration_systems = self.account.get_migration_systems()

        self.assertEqual(len(list(migration_systems)), 2)

        self.assertIsInstance(migration_systems[0], Migrator)
        self.assertEqual(migration_systems[0].type, "dummy_importer")
        self.assertEqual(migration_systems[0].requires_file_upload, True)
        self.assertEqual(migration_systems[0].name, "Dummy Importer 01")
        self.assertIsInstance(migration_systems[1], Migrator)
        self.assertEqual(migration_systems[1].type, "dummy_importer_02")
        self.assertEqual(migration_systems[1].requires_file_upload, False)
        self.assertEqual(migration_systems[1].name, "Dummy Importer 02")

    # get_admins()
    def test_get_admins(self, m):
        register_uris({"account": ["get_admins", "get_admins_page_2"]}, m)

        admins = self.account.get_admins()
        admin_list = [admin for admin in admins]

        self.assertEqual(len(list(admins)), 4)

        self.assertIsInstance(admin_list[0], Admin)
        self.assertIsInstance(admin_list[1], Admin)

        self.assertTrue(hasattr(admin_list[0], "id"))
        self.assertTrue(hasattr(admin_list[1], "role"))
        self.assertTrue(hasattr(admin_list[0], "role_id"))
        self.assertTrue(hasattr(admin_list[1], "workflow_state"))

        self.assertEqual(admin_list[1].user["login_id"], "jdoe")
        self.assertEqual(admin_list[1].role, "AccountAdmin")
        self.assertEqual(admin_list[0].role_id, 2)

    # create_sis_import()
    def test_create_sis_import(self, m):
        import os

        register_uris({"account": ["create_sis_import"]}, m)

        filepath = os.path.join("tests", "fixtures", "test_create_sis_import.csv")

        sis_import = self.account.create_sis_import(filepath)

        self.assertTrue(isinstance(sis_import, SisImport))
        self.assertTrue(hasattr(sis_import, "account_id"))
        self.assertTrue(hasattr(sis_import, "user"))

        self.assertEqual(sis_import.account_id, sis_import.user["id"])

    def test_create_sis_import_binary(self, m):
        import os

        register_uris({"account": ["create_sis_import"]}, m)

        filepath = os.path.join("tests", "fixtures", "test_create_sis_import.csv")

        with open(filepath, "rb") as f:
            sis_import = self.account.create_sis_import(f)

        self.assertIsInstance(sis_import, SisImport)

        self.assertTrue(hasattr(sis_import, "account_id"))
        self.assertTrue(hasattr(sis_import, "user"))

        self.assertEqual(sis_import.account_id, sis_import.user["id"])

    def test_create_sis_import_ioerror(self, m):
        f = "!@#$%^&*()_+QWERTYUIOP{}|"

        with self.assertRaises(IOError):
            self.account.create_sis_import(f)

    # get_sis_import()
    def test_get_sis_import(self, m):
        register_uris({"account": ["get_sis_import"]}, m)

        sis_import_id = 2
        sis_import = self.account.get_sis_import(sis_import_id)

        self.assertIsInstance(sis_import, SisImport)
        self.assertTrue(hasattr(sis_import, "account_id"))

        self.assertEqual(sis_import_id, sis_import.id)

    # get_sis_imports()
    def test_get_sis_imports(self, m):
        register_uris({"account": ["get_sis_imports"]}, m)

        sis_imports = self.account.get_sis_imports()

        self.assertIsInstance(sis_imports[0], SisImport)
        self.assertIsInstance(sis_imports[1], SisImport)

        self.assertTrue(hasattr(sis_imports[0], "account_id"))

        self.assertNotEqual(sis_imports[0].id, sis_imports[1].id)

    # get_sis_imports_running()
    def test_get_sis_imports_running(self, m):
        register_uris({"account": ["get_sis_imports_running"]}, m)

        sis_imports = self.account.get_sis_imports_running()

        self.assertIsInstance(sis_imports[0], SisImport)

        self.assertTrue(hasattr(sis_imports[0], "account_id"))

        for sis_import in sis_imports:
            self.assertEqual(sis_import.workflow_state, "importing")

    # abort_sis_imports_pending()
    def test_abort_sis_imports_pending(self, m):
        register_uris({"account": ["abort_sis_imports_pending"]}, m)

        aborted = self.account.abort_sis_imports_pending()

        self.assertTrue(aborted)

    def test_abort_sis_imports_pending_false(self, m):
        register_uris({"account": ["abort_sis_imports_pending_false"]}, m)

        aborted = self.account.abort_sis_imports_pending()

        self.assertFalse(aborted)

    def test_abort_sis_imports_pending_blank(self, m):
        register_uris({"account": ["abort_sis_imports_pending_blank"]}, m)

        aborted = self.account.abort_sis_imports_pending()

        self.assertFalse(aborted)

    # create_admins()
    def test_create_admin(self, m):
        register_uris({"account": ["create_admin"]}, m)

        user_id = 123
        admin = self.account.create_admin(user=user_id)
        self.assertIsInstance(admin, Admin)
        self.assertTrue(hasattr(admin, "id"))
        self.assertTrue(hasattr(admin, "role"))
        self.assertTrue(hasattr(admin, "role_id"))
        self.assertTrue(hasattr(admin, "workflow_state"))
        self.assertEqual(admin.user["login_id"], "jdoe")
        self.assertEqual(admin.role, "AccountAdmin")
        self.assertEqual(admin.role_id, 1)

    # get_outcome_import_status()
    def test_get_outcome_import_status(self, m):
        register_uris({"account": ["get_outcome_import_status"]}, m)
        outcome_import = self.account.get_outcome_import_status(1)

        self.assertIsInstance(outcome_import, OutcomeImport)
        self.assertEqual(outcome_import.id, 1)
        self.assertEqual(outcome_import.workflow_state, "succeeded")
        self.assertEqual(outcome_import.progress, "100")

    def test_get_outcome_import_status_latest(self, m):
        register_uris({"account": ["get_outcome_import_status_latest"]}, m)
        outcome_import = self.account.get_outcome_import_status("latest")

        self.assertIsInstance(outcome_import, OutcomeImport)
        self.assertEqual(outcome_import.id, 1)
        self.assertEqual(outcome_import.workflow_state, "succeeded")
        self.assertEqual(outcome_import.progress, "100")

    # import_outcome()
    def test_import_outcome_filepath(self, m):
        import os

        register_uris({"account": ["import_outcome"]}, m)

        filepath = os.path.join("tests", "fixtures", "test_import_outcome.csv")

        outcome_import = self.account.import_outcome(filepath)

        self.assertTrue(isinstance(outcome_import, OutcomeImport))
        self.assertTrue(hasattr(outcome_import, "account_id"))
        self.assertTrue(hasattr(outcome_import, "data"))
        self.assertEqual(outcome_import.id, 1)
        self.assertEqual(outcome_import.data["import_type"], "instructure_csv")

    def test_import_outcome_binary(self, m):
        import os

        register_uris({"account": ["import_outcome"]}, m)

        filepath = os.path.join("tests", "fixtures", "test_import_outcome.csv")

        with open(filepath, "rb") as f:
            outcome_import = self.account.import_outcome(f)

        self.assertTrue(isinstance(outcome_import, OutcomeImport))
        self.assertTrue(hasattr(outcome_import, "account_id"))
        self.assertTrue(hasattr(outcome_import, "data"))
        self.assertEqual(outcome_import.id, 1)
        self.assertEqual(outcome_import.data["import_type"], "instructure_csv")

    def test_import_outcome_id(self, m):
        register_uris({"account": ["import_outcome"]}, m)

        outcome_import = self.account.import_outcome(1)

        self.assertTrue(isinstance(outcome_import, OutcomeImport))
        self.assertTrue(hasattr(outcome_import, "account_id"))
        self.assertTrue(hasattr(outcome_import, "data"))
        self.assertEqual(outcome_import.id, 1)
        self.assertEqual(outcome_import.data["import_type"], "instructure_csv")

    def test_import_outcome_ioerror(self, m):
        f = "!@#$%^&*()_+QWERTYUIOP{}|"

        with self.assertRaises(IOError):
            self.account.import_outcome(f)

    # get_grading_periods()
    def test_get_grading_periods(self, m):
        register_uris({"account": ["get_grading_periods"]}, m)

        response = self.account.get_grading_periods()

        self.assertIsInstance(response, PaginatedList)
        self.assertIsInstance(response[0], GradingPeriod)
        self.assertIsInstance(response[1], GradingPeriod)
        self.assertEqual(response[0].id, 1)
        self.assertEqual(response[1].id, 2)
        self.assertEqual(response[0].title, "Grading period 1")
        self.assertEqual(response[1].title, "Grading period 2")

    # delete_grading_periods()
    def test_delete_grading_periods(self, m):
        register_uris({"account": ["delete_grading_period"]}, m)

        self.grading_period = GradingPeriod(
            self.canvas._Canvas__requester,
            {"title": "grading period 1", "id": 1, "course_id": 1},
        )
        self.assertTrue(self.account.delete_grading_period(1))
        self.assertTrue(self.account.delete_grading_period(self.grading_period))

    # get_scopes()
    def test_get_scopes(self, m):
        register_uris({"account": ["get_scopes"]}, m)

        scopes = self.account.get_scopes()
        scope_list = [scope for scope in scopes]

        self.assertEqual(len(list(scopes)), 2)
        self.assertTrue(isinstance(scopes, PaginatedList))
        self.assertTrue(isinstance(scope_list[0], Scope))

        self.assertEqual(scope_list[0].resource, "users")
        self.assertEqual(scope_list[1].resource, "users")

        self.assertEqual(scope_list[0].verb, "PUT")
        self.assertEqual(scope_list[1].verb, "GET")

    # close_notification
    def test_close_notification_for_user_id(self, m):
        register_uris({"account": ["close_notification"]}, m)

        user_id = self.user.id
        notif_id = 1
        closed_notif = self.account.close_notification_for_user(user_id, notif_id)

        self.assertIsInstance(closed_notif, AccountNotification)
        self.assertTrue(hasattr(closed_notif, "subject"))

    # update_global_notification()
    def test_update_global_notification(self, m):
        register_uris({"account": ["update_notification"]}, m)

        self.AccountNotification = AccountNotification(
            self.canvas._Canvas__requester,
            {
                "subject": "",
                "message": "",
                "start_at": "",
                "end_at": "",
                "id": 1,
                "account_id": 1,
            },
        )

        notif = {
            "subject": "subject",
            "message": "Message",
            "start_at": "2015-04-01T00:00:00Z",
            "end_at": "2018-04-01T00:00:00Z",
            "id": 1,
            "account_id": 1,
        }

        updated_notif = self.AccountNotification.update_global_notification(notif)

        self.assertIsInstance(updated_notif, AccountNotification)
        self.assertTrue(hasattr(updated_notif, "subject"))
        self.assertEqual(updated_notif.subject, "subject")

    # update account calendar visibility
    def test_update_account_calendar_visibility(self, m):
        register_uris({"account": ["update_account_calendar_visibility"]}, m)

        # verify object is of type AccountCalendar
        account_calendar = self.account.update_account_calendar_visibility()
        self.assertIsInstance(account_calendar, AccountCalendar)

        # verify contents of object
        self.assertEqual(account_calendar.id, 102)
        self.assertEqual(account_calendar.name, "Department of Aerospace Engineering")
        self.assertTrue(account_calendar.visible)

    # update many account calendars' visibility
    def test_update_many_account_calendars_visibility(self, m):
        register_uris({"account": ["update_many_account_calendars_visibility"]}, m)

        # verify the returned object is of type AccountCalendar
        account_calendar = self.account.update_many_account_calendars_visibility()
        self.assertIsInstance(account_calendar, AccountCalendar)

        # Verify contents of object
        self.assertEqual(account_calendar.id, 1)
        self.assertEqual(account_calendar.name, "Biology Department")
        self.assertTrue(account_calendar.visible)

    def test_update_global_notification_missing_field(self, m):
        register_uris({"account": ["update_notification"]}, m)

        self.AccountNotification = AccountNotification(
            self.canvas._Canvas__requester,
            {
                "subject": "",
                "message": "",
                "start_at": "",
                "end_at": "",
                "id": 1,
                "account_id": 1,
            },
        )

        notif = {}

        with self.assertRaises(RequiredFieldMissing):
            self.AccountNotification.update_global_notification(notif)

    # get_authentication_events()
    def test_get_authentication_events(self, m):
        register_uris({"account": ["get_authentication_events"]}, m)

        authentication_event = self.account.get_authentication_events()
        event_list = [event for event in authentication_event]

        self.assertEqual(len(event_list), 2)

        self.assertIsInstance(event_list[0], AuthenticationEvent)
        self.assertEqual(event_list[0].event_type, "login")
        self.assertEqual(event_list[0].pseudonym_id, 9478)

        self.assertIsInstance(event_list[1], AuthenticationEvent)
        self.assertEqual(event_list[1].created_at, "2012-07-20T15:00:00-06:00")
        self.assertEqual(event_list[1].event_type, "logout")


@requests_mock.Mocker()
class TestAccountNotification(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        self.AccountNotification = AccountNotification(
            self.canvas._Canvas__requester,
            {
                "subject": "subject",
                "message": "Message",
                "start_at": "2015-04-01T00:00:00Z",
                "end_at": "2018-04-01T00:00:00Z",
                "id": 1,
                "account_id": 1,
            },
        )

    # __str__()
    def test__str__(self, m):
        string = str(self.AccountNotification)
        self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestAccountReport(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)
        self.account = Account(self.canvas._Canvas__requester, {"id": 1})

        self.AccountReport = AccountReport(
            self.canvas._Canvas__requester,
            {
                "id": 1,
                "title": "Zero Activity",
                "parameters": {
                    "enrollment_term_id": {
                        "required": False,
                        "description": "The canvas id of the term to get grades from",
                    },
                    "start_at": {
                        "required": False,
                        "description": "The first date in the date range",
                    },
                    "course_id": {
                        "required": False,
                        "description": "The course to report on",
                    },
                },
                "report": "zero_activity_csv",
                "last_run": "null",
            },
        )

    # __str__()
    def test__str__(self, m):
        string = str(self.AccountReport)
        self.assertIsInstance(string, str)

    # get_features()
    def test_get_features(self, m):
        register_uris({"account": ["get_features"]}, m)

        features = self.account.get_features()

        self.assertIsInstance(features, PaginatedList)
        self.assertIsInstance(features[0], Feature)

    # get_enabled_features()
    def test_get_enabled_features(self, m):
        register_uris({"account": ["get_enabled_features"]}, m)

        features = self.account.get_enabled_features()

        self.assertIsInstance(features, list)
        self.assertIsInstance(features[0], str)

    # get_feature_flag()
    def test_get_feature_flag(self, m):
        register_uris({"account": ["get_features", "get_feature_flag"]}, m)

        feature = self.account.get_features()[0]

        feature_flag = self.account.get_feature_flag(feature)

        self.assertIsInstance(feature_flag, FeatureFlag)
        self.assertEqual(feature_flag.feature, "epub_export")
