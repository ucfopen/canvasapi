import datetime
import unittest

import requests_mock

import settings
from pycanvas import Canvas
from pycanvas.account import Account, AccountNotification, AccountReport
from pycanvas.course import Course
from pycanvas.enrollment import Enrollment
from pycanvas.external_tool import ExternalTool
from pycanvas.exceptions import RequiredFieldMissing
from pycanvas.group import Group, GroupCategories
from pycanvas.user import User
from util import register_uris


class TestAccount(unittest.TestCase):
    """
    Tests Account methods.
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'account': [
                'close_notification', 'create', 'create_2', 'create_course',
                'create_notification', 'create_subaccount', 'create_user',
                'delete_user', 'enroll_by_id', 'get_by_id', 'get_by_id_2',
                'get_by_id_3', 'get_courses', 'get_courses_page_2',
                'get_external_tools', 'get_external_tools_p2', 'list_groups_context',
                'list_groups_context2', 'reports', 'reports_page_2', 'report_index',
                'report_index_page_2', 'subaccounts', 'subaccounts_page_2', 'users',
                'users_page_2', 'user_notifs', 'user_notifs_page_2', 'update', 'update_fail',
                'create_group_category', 'list_group_categories'
            ],
            'external_tool': ['get_by_id_account'],
            'user': ['get_by_id'],
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, {'generic': ['not_found']}, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.account = self.canvas.get_account(1)
        self.user = self.canvas.get_user(1)

    # __str__()
    def test__str__(self):
        string = str(self.account)
        assert isinstance(string, str)

    # close_notification_for_user()
    def test_close_notification_for_user_id(self):
        user_id = self.user.id
        notif_id = 1
        closed_notif = self.account.close_notification_for_user(user_id, notif_id)

        assert isinstance(closed_notif, AccountNotification)
        assert hasattr(closed_notif, 'subject')

    def test_close_notification_for_user_obj(self):
        notif_id = 1
        self.account.close_notification_for_user(self.user, notif_id)

    # create_account()
    def test_create_account(self):
        new_account = self.account.create_account()

        assert isinstance(new_account, Account)
        assert hasattr(new_account, 'id')

    # create_course()
    def test_create_course(self):
        course = self.account.create_course()

        assert isinstance(course, Course)
        assert hasattr(course, 'name')

    # create_subaccount()
    def test_create_subaccount(self):
        subaccount_name = "New Subaccount"
        subaccount = self.account.create_subaccount({'name': subaccount_name})

        assert isinstance(subaccount, Account)
        assert hasattr(subaccount, 'name')
        assert subaccount.name == subaccount_name
        assert hasattr(subaccount, 'root_account_id')
        assert subaccount.root_account_id == self.account.id

    def test_create_course_missing_field(self):
        with self.assertRaises(RequiredFieldMissing):
            self.account.create_subaccount({})

    # create_user()
    def test_create_user(self):
        unique_id = 123456
        user = self.account.create_user({'unique_id': unique_id})

        assert isinstance(user, User)
        assert hasattr(user, 'unique_id')
        assert user.unique_id == unique_id

    def test_create_user_missing_field(self):
        with self.assertRaises(RequiredFieldMissing):
            self.account.create_user({})

    # create_notification()
    def test_create_notification(self):
        subject = 'Subject'
        notif_dict = {
            'subject': subject,
            'message': 'Message',
            'start_at': '2015-04-01T00:00:00Z',
            'end_at': '2018-04-01T00:00:00Z'
        }
        notif = self.account.create_notification(notif_dict)

        assert isinstance(notif, AccountNotification)
        assert hasattr(notif, 'subject')
        assert notif.subject == subject
        assert hasattr(notif, 'start_at_date')
        assert isinstance(notif.start_at_date, datetime.datetime)

    def test_create_notification_missing_field(self):
        with self.assertRaises(RequiredFieldMissing):
            self.account.create_notification({})

    # delete_user()
    def test_delete_user_id(self):
        deleted_user = self.account.delete_user(self.user.id)

        assert isinstance(deleted_user, User)
        assert hasattr(deleted_user, 'name')

    def test_delete_user_obj(self):
        deleted_user = self.account.delete_user(self.user)

        assert isinstance(deleted_user, User)
        assert hasattr(deleted_user, 'name')

    # get_courses()
    def test_get_courses(self):
        courses = self.account.get_courses()

        course_list = [course for course in courses]
        assert len(course_list) == 4
        assert isinstance(course_list[0], Course)
        assert hasattr(course_list[0], 'name')

    # get_external_tool()
    def test_get_external_tool(self):
        tool = self.account.get_external_tool(1)

        assert isinstance(tool, ExternalTool)
        assert hasattr(tool, 'name')

    # get_external_tools()
    def test_get_external_tools(self):
        tools = self.account.get_external_tools()
        tool_list = [tool for tool in tools]

        assert isinstance(tool_list[0], ExternalTool)
        assert len(tool_list) == 4

    # get_index_of_reports()
    def test_get_index_of_reports(self):
        reports_index = self.account.get_index_of_reports("sis_export_csv")

        reports_index_list = [index for index in reports_index]
        assert len(reports_index_list) == 4
        assert isinstance(reports_index_list[0], AccountReport)
        assert hasattr(reports_index_list[0], 'id')

    # get_reports()
    def test_get_reports(self):
        reports = self.account.get_reports()

        reports_list = [report for report in reports]
        assert len(reports_list) == 4
        assert isinstance(reports_list[0], AccountReport)
        assert hasattr(reports_list[0], 'id')

    # get_subaccounts()
    def test_get_subaccounts(self):
        subaccounts = self.account.get_subaccounts()

        subaccounts_list = [account for account in subaccounts]
        assert len(subaccounts_list) == 4
        assert isinstance(subaccounts_list[0], Account)
        assert hasattr(subaccounts_list[0], 'name')

    # get_users()
    def test_get_users(self):
        users = self.account.get_users()

        user_list = [user for user in users]
        assert len(user_list) == 4
        assert isinstance(user_list[0], User)
        assert hasattr(user_list[0], 'name')

    # get_user_notifications()
    def test_get_user_notifications_id(self):
        user_notifs = self.account.get_user_notifications(self.user.id)

        notif_list = [notif for notif in user_notifs]
        assert len(notif_list) == 4
        assert isinstance(user_notifs[0], AccountNotification)
        assert hasattr(user_notifs[0], 'subject')

    def test_get_user_notifications_obj(self):
        user_notifs = self.account.get_user_notifications(self.user)

        notif_list = [notif for notif in user_notifs]
        assert len(notif_list) == 4
        assert isinstance(user_notifs[0], AccountNotification)
        assert hasattr(user_notifs[0], 'subject')

    # update()
    def test_update(self):
        account = self.canvas.get_account(100)
        assert account.name == 'Old Name'

        new_name = 'Updated Name'
        update_account_dict = {'name': new_name}

        success = account.update(account=update_account_dict)

        assert success
        assert account.name == new_name

    def test_update_fail(self):
        account = self.canvas.get_account(101)
        assert account.name == 'Old Name'

        new_name = 'Updated Name'
        update_account_dict = {'name': new_name}

        success = account.update(account=update_account_dict)
        assert not success

    # enroll_by_id()
    def test_enroll_by_id(self):
        target_enrollment = self.account.enroll_by_id(1)

        assert isinstance(target_enrollment, Enrollment)

    def test_list_groups_in_context(self):
        groups = self.account.list_groups_in_context()
        group_list = [group for group in groups]

        assert isinstance(group_list[0], Group)
        assert len(group_list) == 4

    # create_group_category()
    def test_create_group_category(self):
        name_str = "Shia Laboef"
        response = self.account.create_group_category(name=name_str)
        assert isinstance(response, GroupCategories)

    # list_group_categories()
    def test_list_group_categories(self):
        response = self.account.list_group_categories()
        category_list = [category for category in response]
        assert isinstance(category_list[0], GroupCategories)
