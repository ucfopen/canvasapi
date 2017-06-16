import datetime
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.account import Account, AccountNotification, AccountReport, Role, SSOSettings
from canvasapi.course import Course
from canvasapi.enrollment import Enrollment
from canvasapi.enrollment_term import EnrollmentTerm
from canvasapi.external_tool import ExternalTool
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.group import Group, GroupCategory
from canvasapi.user import User
from canvasapi.login import Login
from canvasapi.authentication_provider import AuthenticationProvider
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestAccount(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {'account': ['get_by_id'], 'user': ['get_by_id']}
            register_uris(requires, m)

            self.account = self.canvas.get_account(1)
            self.user = self.canvas.get_user(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.account)
        self.assertIsInstance(string, str)

    # close_notification_for_user()
    def test_close_notification_for_user_id(self, m):
        register_uris({'account': ['close_notification']}, m)

        user_id = self.user.id
        notif_id = 1
        closed_notif = self.account.close_notification_for_user(user_id, notif_id)

        self.assertIsInstance(closed_notif, AccountNotification)
        self.assertTrue(hasattr(closed_notif, 'subject'))

    def test_close_notification_for_user_obj(self, m):
        register_uris({'account': ['close_notification']}, m)

        notif_id = 1
        self.account.close_notification_for_user(self.user, notif_id)

    # create_account()
    def test_create_account(self, m):
        register_uris({'account': ['create_2']}, m)

        new_account = self.account.create_account()

        self.assertIsInstance(new_account, Account)
        self.assertTrue(hasattr(new_account, 'id'))

    # create_course()
    def test_create_course(self, m):
        register_uris({'account': ['create_course']}, m)

        course = self.account.create_course()

        self.assertIsInstance(course, Course)
        self.assertTrue(hasattr(course, 'name'))

    # create_subaccount()
    def test_create_subaccount(self, m):
        register_uris({'account': ['create_subaccount']}, m)

        subaccount_name = "New Subaccount"
        subaccount = self.account.create_subaccount({'name': subaccount_name})

        self.assertIsInstance(subaccount, Account)
        self.assertTrue(hasattr(subaccount, 'name'))
        self.assertEqual(subaccount.name, subaccount_name)
        self.assertTrue(hasattr(subaccount, 'root_account_id'))
        self.assertEqual(subaccount.root_account_id, self.account.id)

    def test_create_course_missing_field(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.account.create_subaccount({})

    # create_user()
    def test_create_user(self, m):
        register_uris({'account': ['create_user']}, m)

        unique_id = 123456
        user = self.account.create_user({'unique_id': unique_id})

        self.assertIsInstance(user, User)
        self.assertTrue(hasattr(user, 'unique_id'))
        self.assertEqual(user.unique_id, unique_id)

    def test_create_user_missing_field(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.account.create_user({})

    # create_notification()
    def test_create_notification(self, m):
        register_uris({'account': ['create_notification']}, m)

        subject = 'Subject'
        notif_dict = {
            'subject': subject,
            'message': 'Message',
            'start_at': '2015-04-01T00:00:00Z',
            'end_at': '2018-04-01T00:00:00Z'
        }
        notif = self.account.create_notification(notif_dict)

        self.assertIsInstance(notif, AccountNotification)
        self.assertTrue(hasattr(notif, 'subject'))
        self.assertEqual(notif.subject, subject)
        self.assertTrue(hasattr(notif, 'start_at_date'))
        self.assertIsInstance(notif.start_at_date, datetime.datetime)

    def test_create_notification_missing_field(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.account.create_notification({})

    # delete_user()
    def test_delete_user_id(self, m):
        register_uris({'account': ['delete_user']}, m)

        deleted_user = self.account.delete_user(self.user.id)

        self.assertIsInstance(deleted_user, User)
        self.assertTrue(hasattr(deleted_user, 'name'))

    def test_delete_user_obj(self, m):
        register_uris({'account': ['delete_user']}, m)

        deleted_user = self.account.delete_user(self.user)

        self.assertIsInstance(deleted_user, User)
        self.assertTrue(hasattr(deleted_user, 'name'))

    # get_courses()
    def test_get_courses(self, m):
        required = {'account': ['get_courses', 'get_courses_page_2']}
        register_uris(required, m)

        courses = self.account.get_courses()

        course_list = [course for course in courses]
        self.assertEqual(len(course_list), 4)
        self.assertIsInstance(course_list[0], Course)
        self.assertTrue(hasattr(course_list[0], 'name'))

    # get_external_tool()
    def test_get_external_tool(self, m):
        required = {'external_tool': ['get_by_id_account']}
        register_uris(required, m)

        tool = self.account.get_external_tool(1)

        self.assertIsInstance(tool, ExternalTool)
        self.assertTrue(hasattr(tool, 'name'))

    # get_external_tools()
    def test_get_external_tools(self, m):
        required = {'account': ['get_external_tools', 'get_external_tools_p2']}
        register_uris(required, m)

        tools = self.account.get_external_tools()
        tool_list = [tool for tool in tools]

        self.assertIsInstance(tool_list[0], ExternalTool)
        self.assertEqual(len(tool_list), 4)

    # get_index_of_reports()
    def test_get_index_of_reports(self, m):
        required = {'account': ['report_index', 'report_index_page_2']}
        register_uris(required, m)

        reports_index = self.account.get_index_of_reports("sis_export_csv")

        reports_index_list = [index for index in reports_index]
        self.assertEqual(len(reports_index_list), 4)
        self.assertIsInstance(reports_index_list[0], AccountReport)
        self.assertTrue(hasattr(reports_index_list[0], 'id'))

    # get_reports()
    def test_get_reports(self, m):
        required = {'account': ['reports', 'reports_page_2']}
        register_uris(required, m)

        reports = self.account.get_reports()

        reports_list = [report for report in reports]
        self.assertEqual(len(reports_list), 4)
        self.assertIsInstance(reports_list[0], AccountReport)
        self.assertTrue(hasattr(reports_list[0], 'id'))

    # get_subaccounts()
    def test_get_subaccounts(self, m):
        required = {'account': ['subaccounts', 'subaccounts_page_2']}
        register_uris(required, m)

        subaccounts = self.account.get_subaccounts()

        subaccounts_list = [account for account in subaccounts]
        self.assertEqual(len(subaccounts_list), 4)
        self.assertIsInstance(subaccounts_list[0], Account)
        self.assertTrue(hasattr(subaccounts_list[0], 'name'))

    # get_users()
    def test_get_users(self, m):
        required = {'account': ['users', 'users_page_2']}
        register_uris(required, m)

        users = self.account.get_users()

        user_list = [user for user in users]
        self.assertEqual(len(user_list), 4)
        self.assertIsInstance(user_list[0], User)
        self.assertTrue(hasattr(user_list[0], 'name'))

    # get_user_notifications()
    def test_get_user_notifications_id(self, m):
        required = {'account': ['user_notifs', 'user_notifs_page_2']}
        register_uris(required, m)

        user_notifs = self.account.get_user_notifications(self.user.id)

        notif_list = [notif for notif in user_notifs]
        self.assertEqual(len(notif_list), 4)
        self.assertIsInstance(user_notifs[0], AccountNotification)
        self.assertTrue(hasattr(user_notifs[0], 'subject'))

    def test_get_user_notifications_obj(self, m):
        required = {'account': ['user_notifs', 'user_notifs_page_2']}
        register_uris(required, m)

        user_notifs = self.account.get_user_notifications(self.user)

        notif_list = [notif for notif in user_notifs]
        self.assertEqual(len(notif_list), 4)
        self.assertIsInstance(user_notifs[0], AccountNotification)
        self.assertTrue(hasattr(user_notifs[0], 'subject'))

    # update()
    def test_update(self, m):
        register_uris({'account': ['update']}, m)

        self.assertEqual(self.account.name, 'Canvas Account')

        new_name = 'Updated Name'
        update_account_dict = {'name': new_name}

        self.assertTrue(self.account.update(account=update_account_dict))
        self.assertEqual(self.account.name, new_name)

    def test_update_fail(self, m):
        register_uris({'account': ['update_fail']}, m)

        self.assertEqual(self.account.name, 'Canvas Account')

        new_name = 'Updated Name'
        update_account_dict = {'name': new_name}

        self.assertFalse(self.account.update(account=update_account_dict))

    def test_list_roles(self, m):
        requires = {'account': ['list_roles', 'list_roles_2']}
        register_uris(requires, m)

        roles = self.account.list_roles()
        role_list = [role for role in roles]

        self.assertEqual(len(role_list), 4)
        self.assertIsInstance(role_list[0], Role)
        self.assertTrue(hasattr(role_list[0], 'role'))
        self.assertTrue(hasattr(role_list[0], 'label'))

    def test_get_role(self, m):
        register_uris({'account': ['get_role']}, m)

        target_role = self.account.get_role(2)

        self.assertIsInstance(target_role, Role)
        self.assertTrue(hasattr(target_role, 'role'))
        self.assertTrue(hasattr(target_role, 'label'))

    def test_create_role(self, m):
        register_uris({'account': ['create_role']}, m)

        new_role = self.account.create_role(1)

        self.assertIsInstance(new_role, Role)
        self.assertTrue(hasattr(new_role, 'role'))
        self.assertTrue(hasattr(new_role, 'label'))

    def test_deactivate_role(self, m):
        register_uris({'account': ['deactivate_role']}, m)

        old_role = self.account.deactivate_role(2)

        self.assertIsInstance(old_role, Role)
        self.assertTrue(hasattr(old_role, 'role'))
        self.assertTrue(hasattr(old_role, 'label'))

    def test_activate_role(self, m):
        register_uris({'account': ['activate_role']}, m)

        activated_role = self.account.activate_role(2)

        self.assertIsInstance(activated_role, Role)
        self.assertTrue(hasattr(activated_role, 'role'))
        self.assertTrue(hasattr(activated_role, 'label'))

    def test_update_role(self, m):
        register_uris({'account': ['update_role']}, m)

        updated_role = self.account.update_role(2)

        self.assertIsInstance(updated_role, Role)
        self.assertTrue(hasattr(updated_role, 'role'))
        self.assertTrue(hasattr(updated_role, 'label'))

    # get_enrollment()
    def test_get_enrollment(self, m):
        register_uris({'enrollment': ['get_by_id']}, m)

        target_enrollment = self.account.get_enrollment(1)

        self.assertIsInstance(target_enrollment, Enrollment)

    def test_list_groups(self, m):
        requires = {'account': ['list_groups_context', 'list_groups_context2']}
        register_uris(requires, m)

        groups = self.account.list_groups()
        group_list = [group for group in groups]

        self.assertIsInstance(group_list[0], Group)
        self.assertEqual(len(group_list), 4)

    # create_group_category()
    def test_create_group_category(self, m):
        register_uris({'account': ['create_group_category']}, m)

        name_str = "Test String"
        response = self.account.create_group_category(name=name_str)
        self.assertIsInstance(response, GroupCategory)

    # list_group_categories()
    def test_list_group_categories(self, m):
        register_uris({'account': ['list_group_categories']}, m)

        response = self.account.list_group_categories()
        category_list = [category for category in response]

        self.assertIsInstance(category_list[0], GroupCategory)

    # create_external_tool()
    def test_create_external_tool(self, m):
        register_uris({'external_tool': ['create_tool_account']}, m)

        response = self.account.create_external_tool(
            name="External Tool - Account",
            privacy_level="public",
            consumer_key="key",
            shared_secret="secret"
        )

        self.assertIsInstance(response, ExternalTool)
        self.assertTrue(hasattr(response, 'id'))
        self.assertEqual(response.id, 10)

    # create_enrollment_term()
    def test_create_enrollment_term(self, m):
        register_uris({'enrollment_term': ['create_enrollment_term']}, m)

        evnt = self.account.create_enrollment_term(
            name="Test Enrollment Term",
            id=45
        )

        self.assertIsInstance(evnt, EnrollmentTerm)
        self.assertEqual(evnt.name, "Test Enrollment Term")
        self.assertEqual(evnt.id, 45)

    # list_enrollment_terms()
    def test_list_enrollment_terms(self, m):
        register_uris({'account': ['list_enrollment_terms']}, m)

        response = self.account.list_enrollment_terms()
        enrollment_terms_list = [category for category in response]

        self.assertIsInstance(enrollment_terms_list[0], EnrollmentTerm)

    # list_user_logins()
    def test_list_user_logins(self, m):
        requires = {'account': ['list_user_logins', 'list_user_logins_2']}
        register_uris(requires, m)

        response = self.account.list_user_logins()
        login_list = [login for login in response]

        self.assertIsInstance(login_list[0], Login)
        self.assertEqual(len(login_list), 2)

    # create_user_login()
    def test_create_user_login(self, m):
        register_uris({'account': ['create_user_login']}, m)

        response = self.account.create_user_login(user={'id': 123}, login={'unique_id': 112233})

        self.assertIsInstance(response, Login)
        self.assertTrue(hasattr(response, 'id'))
        self.assertTrue(hasattr(response, 'unique_id'))
        self.assertEqual(response.id, 123)
        self.assertEqual(response.unique_id, 112233)

    def test_create_user_login_fail_on_user_id(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.account.create_user_login(user={}, login={})

    def test_create_user_login_fail_on_login_unique_id(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.account.create_user_login(user={'id': 123}, login={})

    # get_department_level_participation_data_with_given_term()
    def test_get_department_level_participation_data_with_given_term(self, m):
        register_uris({'account': ['get_department_level_participation_data_with_given_term']}, m)

        response = self.account.get_department_level_participation_data_with_given_term(1)

        self.assertIsInstance(response, list)

    # get_department_level_participation_data_current()
    def test_get_department_level_participation_data_current(self, m):
        register_uris({'account': ['get_department_level_participation_data_current']}, m)

        response = self.account.get_department_level_participation_data_current()

        self.assertIsInstance(response, list)

    # get_department_level_participation_data_completed()
    def test_get_department_level_participation_data_completed(self, m):
        register_uris({'account': ['get_department_level_participation_data_completed']}, m)

        response = self.account.get_department_level_participation_data_completed()

        self.assertIsInstance(response, list)

    # get_department_level_grade_data_with_given_term()
    def test_get_department_level_grade_data_with_given_term(self, m):
        register_uris({'account': ['get_department_level_grade_data_with_given_term']}, m)

        response = self.account.get_department_level_grade_data_with_given_term(1)

        self.assertIsInstance(response, list)

    # get_department_level_grade_data_current()
    def test_get_department_level_grade_data_current(self, m):
        register_uris({'account': ['get_department_level_grade_data_current']}, m)

        response = self.account.get_department_level_grade_data_current()

        self.assertIsInstance(response, list)

    # get_department_level_grade_data_completed()
    def test_get_department_level_grade_data_completed(self, m):
        register_uris({'account': ['get_department_level_grade_data_completed']}, m)

        response = self.account.get_department_level_grade_data_completed()

        self.assertIsInstance(response, list)

    # get_department_level_statistics_with_given_term()
    def test_get_department_level_statistics_with_given_term(self, m):
        register_uris({'account': ['get_department_level_statistics_with_given_term']}, m)

        response = self.account.get_department_level_statistics_with_given_term(1)

        self.assertIsInstance(response, list)

    # get_department_level_statistics_current()
    def test_get_department_level_statistics_current(self, m):
        register_uris({'account': ['get_department_level_statistics_current']}, m)

        response = self.account.get_department_level_statistics_current()

        self.assertIsInstance(response, list)

    # get_department_level_statistics_completed()
    def test_get_department_level_statistics_completed(self, m):
        register_uris({'account': ['get_department_level_statistics_completed']}, m)

        response = self.account.get_department_level_statistics_completed()

        self.assertIsInstance(response, list)

    # list_authentication_providers()
    def test_list_authentication_providers(self, m):
        requires = {'account': ['list_authentication_providers',
                                'list_authentication_providers_2']}
        register_uris(requires, m)

        authentication_providers = self.account.list_authentication_providers()
        authentication_providers_list = [
            authentication_provider for authentication_provider in authentication_providers
        ]

        self.assertEqual(len(authentication_providers_list), 4)
        self.assertIsInstance(authentication_providers_list[0], AuthenticationProvider)
        self.assertTrue(hasattr(authentication_providers_list[0], 'auth_type'))
        self.assertTrue(hasattr(authentication_providers_list[0], 'position'))

    # add_authentication_providers()
    def test_add_authentication_providers(self, m):
        register_uris({'account': ['add_authentication_providers']}, m)

        new_authentication_provider = self.account.add_authentication_providers()

        self.assertIsInstance(new_authentication_provider, AuthenticationProvider)
        self.assertTrue(hasattr(new_authentication_provider, 'auth_type'))
        self.assertTrue(hasattr(new_authentication_provider, 'position'))

    # get_authentication_providers()
    def test_get_authentication_providers(self, m):
        register_uris({'account': ['get_authentication_providers']}, m)

        response = self.account.get_authentication_providers(1)

        self.assertIsInstance(response, AuthenticationProvider)

    # show_account_auth_settings()
    def test_show_account_auth_settings(self, m):
        register_uris({'account': ['show_account_auth_settings']}, m)

        response = self.account.show_account_auth_settings()

        self.assertIsInstance(response, SSOSettings)

    # update_account_auth_settings()
    def test_update_account_auth_settings(self, m):
        register_uris({'account': ['update_account_auth_settings']}, m)

        response = self.account.update_account_auth_settings()

        self.assertIsInstance(response, SSOSettings)
