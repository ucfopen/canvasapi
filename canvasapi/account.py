from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs, obj_or_id


class Account(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def close_notification_for_user(self, user, notification):
        """
        If the user no long wants to see a notification, it can be
        excused with this call.

        :calls: `DELETE /api/v1/accounts/:account_id/users/:user_id/account_notifications/:id \
        <https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.user_close_notification>`_

        :param user: The user object or ID to close the notificaton for.
        :type user: :class:`canvasapi.user.User` or int
        :param notification: The notification object or ID to close.
        :type notification: :class:`canvasapi.account.AccountNotification` or int
        :rtype: :class:`canvasapi.account.AccountNotification`
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))
        notif_id = obj_or_id(notification, "notif", (AccountNotification,))

        response = self._requester.request(
            'DELETE',
            'accounts/%s/users/%s/account_notifications/%s' % (self.id, user_id, notif_id)
        )
        return AccountNotification(self._requester, response.json())

    def create_account(self, **kwargs):
        """
        Create a new root account.

        :calls: `POST /api/v1/accounts/:account_id/root_accounts \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.create>`_

        :rtype: :class:`canvasapi.account.Account`
        """
        response = self._requester.request(
            'POST',
            'accounts/%s/root_accounts' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return Account(self._requester, response.json())

    def create_course(self, **kwargs):
        """
        Create a course.

        :calls: `POST /api/v1/accounts/:account_id/courses \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.create>`_

        :rtype: :class:`canvasapi.course.Course`
        """
        from canvasapi.course import Course
        response = self._requester.request(
            'POST',
            'accounts/%s/courses' % (self.id),
            account_id=self.id,
            **combine_kwargs(**kwargs)
        )
        return Course(self._requester, response.json())

    def create_subaccount(self, account, **kwargs):
        """
        Add a new sub-account to a given account.

        :calls: `POST /api/v1/accounts/:account_id/sub_accounts \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.create>`_

        :rtype: :class:`canvasapi.account.Account`
        """
        if isinstance(account, dict) and 'name' in account:
            kwargs['account'] = account
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")

        response = self._requester.request(
            'POST',
            'accounts/%s/sub_accounts' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return Account(self._requester, response.json())

    def create_user(self, pseudonym, **kwargs):
        """
        Create and return a new user and pseudonym for an account.

        :calls: `POST /api/v1/accounts/:account_id/users \
        <https://canvas.instructure.com/doc/api/users.html#method.users.create>`_

        :param pseudonym: The pseudonym of the account.
        :type pseudonym: dict
        :rtype: :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

        if isinstance(pseudonym, dict) and 'unique_id' in pseudonym:
            kwargs['pseudonym'] = pseudonym
        else:
            raise RequiredFieldMissing("Dictionary with key 'unique_id' is required.")

        response = self._requester.request(
            'POST',
            'accounts/%s/users' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return User(self._requester, response.json())

    def create_notification(self, account_notification, **kwargs):
        """
        Create and return a new global notification for an account.

        :calls: `POST /api/v1/accounts/:account_id/account_notifications \
        <https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.create>`_

        :param account_notification: The notification to create.
        :type account_notification: dict
        :rtype: :class:`canvasapi.account.AccountNotification`
        """
        required_key_list = ['subject', 'message', 'start_at', 'end_at']
        required_keys_present = all((x in account_notification for x in required_key_list))

        if isinstance(account_notification, dict) and required_keys_present:
            kwargs['account_notification'] = account_notification
        else:
            raise RequiredFieldMissing((
                "account_notification must be a dictionary with keys "
                "'subject', 'message', 'start_at', and 'end_at'."
            ))

        response = self._requester.request(
            'POST',
            'accounts/%s/account_notifications' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return AccountNotification(self._requester, response.json())

    def delete_user(self, user):
        """
        Delete a user record from a Canvas root account.

        If a user is associated with multiple root accounts (in a
        multi-tenant instance of Canvas), this action will NOT remove
        them from the other accounts.

        WARNING: This API will allow a user to remove themselves from
        the account. If they do this, they won't be able to make API
        calls or log into Canvas at that account.

        :calls: `DELETE /api/v1/accounts/:account_id/users/:user_id \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.remove_user>`_

        :param user: The user object or ID to delete.
        :type user: :class:`canvasapi.user.User` or int
        :rtype: :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            'DELETE',
            'accounts/%s/users/%s' % (self.id, user_id)
        )
        return User(self._requester, response.json())

    def get_courses(self, **kwargs):
        """
        Retrieve the list of courses in this account.

        :calls: `GET /api/v1/accounts/:account_id/courses \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.courses_api>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.Course`
        """
        from canvasapi.course import Course

        return PaginatedList(
            Course,
            self._requester,
            'GET',
            'accounts/%s/courses' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def get_external_tool(self, tool_id):
        """
        :calls: `GET /api/v1/accounts/:account_id/external_tools/:external_tool_id \
        <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.show>`_

        :rtype: :class:`canvasapi.external_tool.ExternalTool`
        """
        from canvasapi.external_tool import ExternalTool

        response = self._requester.request(
            'GET',
            'accounts/%s/external_tools/%s' % (self.id, tool_id),
        )
        tool_json = response.json()
        tool_json.update({'account_id': self.id})

        return ExternalTool(self._requester, tool_json)

    def get_external_tools(self, **kwargs):
        """
        :calls: `GET /api/v1/accounts/:account_id/external_tools \
        <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.external_tool.ExternalTool`
        """
        from canvasapi.external_tool import ExternalTool

        return PaginatedList(
            ExternalTool,
            self._requester,
            'GET',
            'accounts/%s/external_tools' % (self.id),
            {'account_id': self.id},
            **combine_kwargs(**kwargs)
        )

    def get_index_of_reports(self, report_type):
        """
        Retrieve all reports that have been run for the account of a specific type.

        :calls: `GET /api/v1/accounts/:account_id/reports/:report \
        <https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.index>`_

        :param report_type: The type of report.
        :type report_type: str
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.account.AccountReport`
        """
        return PaginatedList(
            AccountReport,
            self._requester,
            'GET',
            'accounts/%s/reports/%s' % (self.id, report_type)
        )

    def get_reports(self):
        """
        Return a list of reports for the current context.

        :calls: `GET /api/v1/accounts/:account_id/reports \
        <https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.available_reports>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.account.AccountReport`
        """
        return PaginatedList(
            AccountReport,
            self._requester,
            'GET',
            'accounts/%s/reports' % (self.id)
        )

    def get_subaccounts(self, recursive=False):
        """
        List accounts that are sub-accounts of the given account.

        :calls: `GET /api/v1/accounts/:account_id/sub_accounts \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.sub_accounts>`_

        :param recursive: If true, the entire account tree underneath this account will \
        be returned. If false, only direct sub-accounts of this  account will be returned.
        :type recursive: bool
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.account.Account`
        """
        return PaginatedList(
            Account,
            self._requester,
            'GET',
            'accounts/%s/sub_accounts' % (self.id),
            recursive=recursive
        )

    def get_users(self, **kwargs):
        """
        Retrieve a list of users associated with this account.

        :calls: `GET /api/v1/accounts/:account_id/users \
        <https://canvas.instructure.com/doc/api/users.html#method.users.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

        return PaginatedList(
            User,
            self._requester,
            'GET',
            'accounts/%s/users' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def get_user_notifications(self, user):
        """
        Return a list of all global notifications in the account for
        this user. Any notifications that have been closed by the user
        will not be returned.

        :calls: `GET /api/v1/accounts/:account_id/users/:user_id/account_notifications \
        <https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.user_index>`_

        :param user: The user object or ID to retrieve notifications for.
        :type user: :class:`canvasapi.user.User` or int
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.account.AccountNotification`
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))

        return PaginatedList(
            AccountNotification,
            self._requester,
            'GET',
            'accounts/%s/users/%s/account_notifications' % (self.id, user_id)
        )

    def update(self, **kwargs):
        """
        Update an existing account.

        :calls: `PUT /api/v1/accounts/:id \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.update>`_

        :returns: True if the account was updated, False otherwise.
        :rtype: bool
        """
        response = self._requester.request(
            'PUT',
            'accounts/%s' % (self.id),
            **combine_kwargs(**kwargs)
        )

        if 'name' in response.json():
            super(Account, self).set_attributes(response.json())
            return True
        else:
            return False

    def list_roles(self, **kwargs):
        """
        List the roles available to an account.

        :calls: `GET /api/v1/accounts/:account_id/roles \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.api_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.account.Role`
        """

        return PaginatedList(
            Role,
            self._requester,
            'GET',
            'accounts/%s/roles' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def get_role(self, role_id):
        """
        Retrieve a role by ID.

        :calls: `GET /api/v1/accounts/:account_id/roles/:id \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.show>`_

        :param role_id: The ID of the role.
        :type role_id: int
        :rtype: :class:`canvasapi.account.Role`
        """

        response = self._requester.request(
            'GET',
            'accounts/%s/roles/%s' % (self.id, role_id)
        )
        return Role(self._requester, response.json())

    def create_role(self, label, **kwargs):
        """
        Create a new course-level or account-level role.

        :calls: `POST /api/v1/accounts/:account_id/roles \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.add_role>`_

        :param label: The label for the role.
        :type label: str
        :rtype: :class:`canvasapi.account.Role`
        """

        response = self._requester.request(
            'POST',
            'accounts/%s/roles' % (self.id),
            label=label,
            **combine_kwargs(**kwargs)
        )
        return Role(self._requester, response.json())

    def deactivate_role(self, role_id, **kwargs):
        """
        Deactivate a custom role.

        :calls: `DELETE /api/v1/accounts/:account_id/roles/:id \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.remove_role>`_

        :param role_id: The ID of the role.
        :type role_id: int
        :rtype: :class:`canvasapi.account.Role`
        """

        response = self._requester.request(
            'DELETE',
            'accounts/%s/roles/%s' % (self.id, role_id),
            **combine_kwargs(**kwargs)
        )
        return Role(self._requester, response.json())

    def activate_role(self, role_id, **kwargs):
        """
        Reactivate an inactive role.

        :calls: `POST /api/v1/accounts/:account_id/roles/:id/activate \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.activate_role>`_

        :param role_id: The ID of the role.
        :type role_id: int
        :rtype: :class:`canvasapi.account.Role`
        """

        response = self._requester.request(
            'POST',
            'accounts/%s/roles/%s/activate' % (self.id, role_id),
            **combine_kwargs(**kwargs)
        )
        return Role(self._requester, response.json())

    def update_role(self, role_id, **kwargs):
        """
        Update permissions for an existing role.

        :calls: `PUT /api/v1/accounts/:account_id/roles/:id \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.update>`_

        :param role_id: The ID of the role.
        :type role_id: int
        :rtype: :class:`canvasapi.account.Role`
        """

        response = self._requester.request(
            'PUT',
            'accounts/%s/roles/%s' % (self.id, role_id),
            **combine_kwargs(**kwargs)
        )
        return Role(self._requester, response.json())

    def get_enrollment(self, enrollment_id, **kwargs):
        """
        Get an enrollment object by ID.

        :calls: `GET /api/v1/accounts/:account_id/enrollments/:id \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.show>`_

        :param enrollment_id: The ID of the enrollment to retrieve.
        :type enrollment_id: int
        :rtype: :class:`canvasapi.enrollment.Enrollment`
        """
        from canvasapi.enrollment import Enrollment

        response = self._requester.request(
            'GET',
            'accounts/%s/enrollments/%s' % (self.id, enrollment_id),
            **combine_kwargs(**kwargs)
        )
        return Enrollment(self._requester, response.json())

    def list_groups(self, **kwargs):
        """
        Return a list of active groups for the specified account.

        :calls: `GET /api/v1/accounts/:account_id/groups \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.context_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of :class:`canvasapi.group.Group`
        """
        from group import Group
        return PaginatedList(
            Group,
            self._requester,
            'GET',
            'accounts/%s/groups' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def create_group_category(self, name, **kwargs):
        """
        Create a Group Category

        :calls: `POST /api/v1/accounts/:account_id/group_categories \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.create>`_

        :param name: Name of group category.
        :type name: str
        :rtype: :class:`canvasapi.group.GroupCategory`
        """
        from group import GroupCategory

        response = self._requester.request(
            'POST',
            'accounts/%s/group_categories' % (self.id),
            name=name,
            **combine_kwargs(**kwargs)
        )
        return GroupCategory(self._requester, response.json())

    def list_group_categories(self):
        """
        List group categories for a context

        :calls: `GET /api/v1/accounts/:account_id/group_categories \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.group.GroupCategory`
        """
        from group import GroupCategory

        return PaginatedList(
            GroupCategory,
            self._requester,
            'GET',
            'accounts/%s/group_categories' % (self.id)
        )

    def create_external_tool(self, name, privacy_level, consumer_key, shared_secret, **kwargs):
        """
        Create an external tool in the current account.

        :calls: `POST /api/v1/accounts/:account_id/external_tools \
        <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.create>`_

        :param name: The name of the tool
        :type name: str
        :param privacy_level: What information to send to the external
            tool. Options are "anonymous", "name_only", "public"
        :type privacy_level: str
        :param consumer_key: The consumer key for the external tool
        :type consumer_key: str
        :param shared_secret: The shared secret with the external tool
        :type shared_secret: str
        :rtype: :class:`canvasapi.external_tool.ExternalTool`
        """
        from canvasapi.external_tool import ExternalTool

        response = self._requester.request(
            'POST',
            'accounts/%s/external_tools' % (self.id),
            **combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update({'account_id': self.id})

        return ExternalTool(self._requester, response_json)

    def create_enrollment_term(self, **kwargs):
        """
        Create an enrollment term.

        :calls: `POST /api/v1/accounts/:account_id/terms \
        <https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms.create>`_

        :rtype: :class:`canvasapi.enrollment_term.EnrollmentTerm`
        """
        from canvasapi.enrollment_term import EnrollmentTerm

        response = self._requester.request(
            'POST',
            'accounts/%s/terms' % (self.id),
            **combine_kwargs(**kwargs)
        )
        enrollment_term_json = response.json()
        enrollment_term_json.update({'account_id': self.id})

        return EnrollmentTerm(self._requester, enrollment_term_json)

    def list_enrollment_terms(self, **kwargs):
        """
        List enrollment terms for a context

        :calls: `GET /api/v1/accounts/:account_id/terms \
        <https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.enrollment_term.EnrollmentTerm`
        """
        from enrollment_term import EnrollmentTerm

        return PaginatedList(
            EnrollmentTerm,
            self._requester,
            'GET',
            'accounts/%s/terms' % (self.id),
            {'account_id': self.id},
            **combine_kwargs(**kwargs)
        )

    def list_user_logins(self, **kwargs):
        """
        Given a user ID, return that user's logins for the given account.

        :calls: `GET /api/v1/accounts/:account_id/logins \
        <https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.login.Login`
        """
        from login import Login

        return PaginatedList(
            Login,
            self._requester,
            'GET',
            'accounts/%s/logins' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def create_user_login(self, user, login, **kwargs):
        """
        Create a new login for an existing user in the given account

        :calls: `POST /api/v1/accounts/:account_id/logins \
        <https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.create>`_

        :param user: The attributes of the user to create a login for
        :type user: `dict`
        :param login: The attributes of the login to create
        :type login: `dict`
        :rtype: :class:`canvasapi.login.Login`
        """
        from login import Login

        if isinstance(user, dict) and 'id' in user:
            kwargs['user'] = user
        else:
            raise RequiredFieldMissing((
                "user must be a dictionary with keys "
                "'id'."
            ))

        if isinstance(login, dict) and 'unique_id' in login:
            kwargs['login'] = login
        else:
            raise RequiredFieldMissing((
                "login must be a dictionary with keys "
                "'unique_id'."
            ))

        response = self._requester.request(
            'POST',
            'accounts/%s/logins' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return Login(self._requester, response.json())

    def get_department_level_participation_data_with_given_term(self, term_id):
        """
        Return page view hits all available or concluded courses in the given term

        :calls: `GET /api/v1/accounts/:account_id/analytics/terms/:term_id/activity \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_participation>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'accounts/%s/analytics/terms/%s/activity' % (self.id, term_id)
        )
        return response.json()

    def get_department_level_participation_data_current(self):
        """
        Return page view hits all available courses in the default term

        :calls: `GET /api/v1/accounts/:account_id/analytics/current/activity \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_participation>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'accounts/%s/analytics/current/activity' % (self.id)
        )
        return response.json()

    def get_department_level_participation_data_completed(self):
        """
        Return page view hits all concluded courses in the default term

        :calls: `GET /api/v1/accounts/:account_id/analytics/completed/activity \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_participation>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'accounts/%s/analytics/completed/activity' % (self.id)
        )
        return response.json()

    def get_department_level_grade_data_with_given_term(self, term_id):
        """
        Return the distribution of all available or concluded grades with the given term

        :calls: `GET /api/v1/accounts/:account_id/analytics/terms/:term_id/grades \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_grades>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'accounts/%s/analytics/terms/%s/grades' % (self.id, term_id)
        )
        return response.json()

    def get_department_level_grade_data_current(self):
        """
        Return the distribution of all available grades in the default term

        :calls: `GET /api/v1/accounts/:account_id/analytics/current/grades \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_grades>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'accounts/%s/analytics/current/grades' % (self.id)
        )
        return response.json()

    def get_department_level_grade_data_completed(self):
        """
        Return the distribution of all concluded grades in the default term

        :calls: `GET /api/v1/accounts/:account_id/analytics/completed/grades \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_grades>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'accounts/%s/analytics/completed/grades' % (self.id)
        )
        return response.json()

    def get_department_level_statistics_with_given_term(self, term_id):
        """
        Return numeric statistics about the department with the given term

        :calls: `GET /api/v1/accounts/:account_id/analytics/terms/:term_id/statistics \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_statistics>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'accounts/%s/analytics/terms/%s/statistics' % (self.id, term_id)
        )
        return response.json()

    def get_department_level_statistics_current(self):
        """
        Return all available numeric statistics about the department in the default term

        :calls: `GET /api/v1/accounts/:account_id/analytics/current/statistics \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_statistics>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'accounts/%s/analytics/current/statistics' % (self.id)
        )
        return response.json()

    def get_department_level_statistics_completed(self):
        """
        Return all available numeric statistics about the department in the default term

        :calls: `GET /api/v1/accounts/:account_id/analytics/current/statistics \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_statistics>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'accounts/%s/analytics/completed/statistics' % (self.id)
        )
        return response.json()

    def add_authentication_providers(self, **kwargs):
        """
        Add external authentication providers for the account

        :calls: `POST /api/v1/accounts/:account_id/authentication_providers \
        <https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.create>`_

        :rtype: :class:`canvasapi.authentication_provider.AuthenticationProvider`
        """
        from canvasapi.authentication_provider import AuthenticationProvider

        response = self._requester.request(
            'POST',
            'accounts/%s/authentication_providers' % (self.id),
            **combine_kwargs(**kwargs)
        )
        authentication_providers_json = response.json()
        authentication_providers_json.update({'account_id': self.id})

        return AuthenticationProvider(self._requester, authentication_providers_json)

    def list_authentication_providers(self, **kwargs):
        """
        Return the list of authentication providers

        :calls: `GET /api/v1/accounts/:account_id/authentication_providers \
        <https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.authentication_provider.AuthenticationProvider`
        """
        from canvasapi.authentication_provider import AuthenticationProvider

        return PaginatedList(
            AuthenticationProvider,
            self._requester,
            'GET',
            'accounts/%s/authentication_providers' % (self.id),
            {'account_id': self.id},
            **combine_kwargs(**kwargs)
        )

    def get_authentication_providers(self, authentication_providers_id, **kwargs):
        """
        Get the specified authentication provider

        :calls: `GET /api/v1/accounts/:account_id/authentication_providers/:id \
        <https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.show>`_

        :rtype: :class:`canvasapi.authentication_provider.AuthenticationProvider`
        """
        from canvasapi.authentication_provider import AuthenticationProvider

        response = self._requester.request(
            'GET',
            'accounts/%s/authentication_providers/%s' % (self.id, authentication_providers_id),
            **combine_kwargs(**kwargs)
        )

        return AuthenticationProvider(self._requester, response.json())

    def show_account_auth_settings(self, **kwargs):
        """
        Return the current state of each account level setting

        :calls: `GET /api/v1/accounts/:account_id/sso_settings \
        <https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.show_sso_settings>`_

        :rtype: :class:`canvasapi.account.SSOSettings`
        """

        response = self._requester.request(
            'GET',
            'accounts/%s/sso_settings' % (self.id),
            **combine_kwargs(**kwargs)
        )

        return SSOSettings(self._requester, response.json())

    def update_account_auth_settings(self, **kwargs):
        """
        Return the current state of account level after updated

        :calls: `PUT /api/v1/accounts/:account_id/sso_settings \
        <https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.update_sso_settings>`_

        :rtype: :class:`canvasapi.account.SSOSettings`
        """

        response = self._requester.request(
            'PUT',
            'accounts/%s/sso_settings' % (self.id),
            **combine_kwargs(**kwargs)
        )

        return SSOSettings(self._requester, response.json())


class AccountNotification(CanvasObject):

    def __str__(self):  # pragma: no cover
        return str(self.subject)


class AccountReport(CanvasObject):

    def __str__(self):  # pragma: no cover
        return "{} ({})".format(self.report, self.id)


class Role(CanvasObject):

    def __str__(self):  # pragma: no cover
        return "{} ({})".format(self.label, self.base_role_type)


class SSOSettings(CanvasObject):

    def __str___(self):  # pragma: no cover
        return"{} ({})".format(self.login_handle_name, self.change_password_url)
