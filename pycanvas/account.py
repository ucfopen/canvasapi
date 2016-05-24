from canvas_object import CanvasObject
from exceptions import RequiredFieldMissing
from paginated_list import PaginatedList
from util import combine_kwargs, obj_or_id


class Account(CanvasObject):

    def __str__(self):
        return "id: %s, name: %s" % (
            self.id,
            self.name
        )

    def close_notification_for_user(self, user, notification):
        """
        If the user no long wants to see a notification, it can be
        excused with this call.

        :calls: `DELETE /api/v1/accounts/:account_id/users/:user_id/account_notifications/:id \
        <https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.user_close_notification>`_

        :param user: The user object or ID to close the notificaton for.
        :type user: :class:`pycanvas.user.User` or int
        :param notification: The notification object or ID to close.
        :type notification: :class:`pycanvas.account.AccountNotification` or int
        :rtype: :class:`pycanvas.account.AccountNotification`
        """
        from user import User

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

        :rtype: :class:`pycanvas.account.Account`
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

        :rtype: :class:`pycanvas.course.Course`
        """
        from course import Course
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

        :rtype: :class:`pycanvas.account.Account`
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
        :rtype: :class:`pycanvas.user.User`
        """
        from user import User

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
        :rtype: :class:`pycanvas.account.AccountNotification`
        """
        required_key_list = ['subject', 'message', 'start_at', 'end_at']
        required_keys_present = all((x in account_notification for x in required_key_list))

        if isinstance(account_notification, dict) and required_keys_present:
            kwargs['account_notification'] = account_notification
        else:
            raise RequiredFieldMissing("account_notification must be a dictionary with keys 'subject', 'message', 'start_at', and 'end_at'.")

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
        :type user: :class:`pycanvas.user.User` or int
        :rtype: :class:`pycanvas.user.User`
        """
        from user import User

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

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.course.Course`
        """
        from course import Course

        return PaginatedList(
            Course,
            self._requester,
            'GET',
            'accounts/%s/courses' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def get_index_of_reports(self, report_type):
        """
        Retrieve all reports that have been run for the account of a specific type.

        :calls: `GET /api/v1/accounts/:account_id/reports/:report \
        <https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.index>`_

        :param report_type: The type of report.
        :type report_type: str
        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.account.AccountReport`
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

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.account.AccountReport`
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
        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.account.Account`
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

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.user.User`
        """
        from user import User

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
        :type user: :class:`pycanvas.user.User` or int
        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.account.AccountNotification`
        """
        from user import User

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

    def get_roles(self, **kwargs):
        """
        List the roles available to an account.

        :calls: `GET /api/v1/accounts/:account_id/roles \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.api_index>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.role.Role`
        """
        from role import Role

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
        :rtype: :class:`pycanvas.role.Role`
        """
        from role import Role

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
        :rtype: :class:`pycanvas.role.Role`
        """
        from role import Role

        response = self._requester.request(
            'POST',
            'accounts/%s/roles' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return Role(self._requester, response.json())

    def deactivate_role(self, role_id):
        """
        Deactivate a custom role.

        :calls: `DELETE /api/v1/accounts/:account_id/roles/:id \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.remove_role>`_

        :param role_id: The ID of the role.
        :type role_id: int
        :rtype: :class:`pycanvas.role.Role`
        """
        from role import Role

        response = self._requester.request(
            'DELETE',
            'accounts/%s/roles/%s' % (self.id, role_id),
        )
        return Role(self._requester, response.json())

    def activate_role(self, role_id):
        """
        Reactivate an inactive role.

        :calls: `POST /api/v1/accounts/:account_id/roles/:id/activate \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.activate_role>`_

        :param role_id: The ID of the role.
        :type role_id: int
        :rtype: :class:`pycanvas.role.Role`
        """
        from role import Role

        response = self._requester.request(
            'POST',
            'accounts/%s/roles/%s/activate' % (self.id, role_id)
        )
        return Role(self._requester, response.json())

    def update_role(self, role_id, **kwargs):
        """
        Update permissions for an existing role.

        :calls: `PUT /api/v1/accounts/:account_id/roles/:id \
        <https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.update>`_

        :param role_id: The ID of the role.
        :type role_id: int
        :rtype: :class:`pycanvas.role.Role`
        """
        from role import Role

        response = self._requester.request(
            'PUT',
            'accounts/%s/roles/%s' % (self.id, role_id),
            **combine_kwargs(**kwargs)
        )
        return Role(self._requester, response.json())

    def enroll_by_id(self, enrollment_id, **kwargs):
        """
        Get an enrollment object by ID.

        :calls: `GET /api/v1/accounts/:account_id/enrollments/:id \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.show>`_

        :param enrollment_id: The ID of the enrollment to retrieve.
        :type enrollment_id: int
        :rtype: :class:`pycanvas.enrollment.Enrollment`
        """
        from enrollment import Enrollment

        response = self._requester.request(
            'GET',
            'accounts/%s/enrollments/%s' % (self.id, enrollment_id),
            **combine_kwargs(**kwargs)
        )
        return Enrollment(self._requester, response.json())


class AccountNotification(CanvasObject):
    def __str__(self):  # pragma: no cover
        return "subject: %s, message: %s" % (
            self.subject,
            self.message
        )


class AccountReport(CanvasObject):
    def __str__(self):  # pragma: no cover
        return "id: %s, report: %s" % (
            self.id,
            self.report
        )


class Role(CanvasObject):

    def __str__(self):
        return "id: %s" % (self.id)
