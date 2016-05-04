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

    def close_notification_for_user(self, user, notif):
        """
        If the user no long wants to see this notification it can be
        excused with this call.

        :calls: `DELETE /api/v1/accounts/:account_id/users/:user_id/account_notifications/:id
        <https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.user_close_notification>`
        :param user: :class:`User` or int
        :rtype: :class:`AccountNotification`
        """
        from user import User

        user_id = obj_or_id(user, "user", (User,))
        notif_id = obj_or_id(notif, "notif", (AccountNotification,))

        response = self._requester.request(
            'DELETE',
            'accounts/%s/users/%s/account_notifications/%s' % (self.id, user_id, notif_id)
        )
        return AccountNotification(self._requester, response.json())

    def create_account(self, **kwargs):
        """
        Creates a new root account.

        :calls: `POST /api/v1/accounts/:account_id/root_accounts
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.create>`
        :rtype: :class:`Account`
        """
        response = self._requester.request(
            'POST',
            '/accounts/%s/root_accounts' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return Account(self._requester, response.json())

    def create_course(self, **kwargs):
        """
        Create a course.

        :calls: `POST /api/v1/accounts/:account_id/courses
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.create>`
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

        :calls: `POST /api/v1/accounts/:account_id/sub_accounts
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.create>`
        :rtype: :class:`Account`
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

        :calls: `POST /api/v1/accounts/:account_id/users
        <https://canvas.instructure.com/doc/api/users.html#method.users.create>`
        :param pseudonym: dict
        :rtype: :class: `User`
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

        :calls: `POST /api/v1/accounts/:account_id/account_notifications
        <https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.create>`
        :param account_notification: dict
        :rtype: :class: `AccountNotification`
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

        :calls: `DELETE /api/v1/accounts/:account_id/users/:user_id
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.remove_user>`
        :param user: :class:`User` or int
        :rtype: :class:`User`
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

        :calls: `GET /api/v1/accounts/:account_id/courses
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.courses_api>`
        :rtype: :class:`PaginatedList` of :class:`Course`
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
        Shows all reports that have been run for the account of a specific type.

        :calls: `GET /api/v1/accounts/:account_id/reports/:report
        <https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.index>`
        :param report_type: str
        :rtype: :class:`PaginatedList` of :class:`AccountReport`
        """
        return PaginatedList(
            AccountReport,
            self._requester,
            'GET',
            'accounts/%s/reports/%s' % (self.id, report_type)
        )

    def get_reports(self):
        """
        Returns the list of reports for the current context.

        :calls: `GET /api/v1/accounts/:account_id/reports
        <https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.available_reports>`
        :rtpye: :class:`PaginatedList` of :class`AccountReport`
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

        :calls: `GET /api/v1/accounts/:account_id/sub_accounts
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.sub_accounts>`
        :param recursive: bool
        :rtype: :class:`PaginatedList` of :class:`Account`
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
        Retrieve the list of users associated with this account.

        :calls: `GET /api/v1/accounts/:account_id/users
        <https://canvas.instructure.com/doc/api/users.html#method.users.index>`
        :rtype: :class:`PaginatedList` of :class:`User`
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
        Returns a list of all global notifications in the account for
        this user. Any notifications that have been closed by the user
        will not be returned.

        :calls:`GET /api/v1/accounts/:account_id/users/:user_id/account_notifications
        <https://canvas.instructure.com/doc/api/account_notifications.html#method.account_notifications.user_index>`
        :param user: :class:`User` or int
        :rtype: :class:`PaginatedList` of :class:`AccountNotification`
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

        :calls: `PUT /api/v1/accounts/:id
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.update>`
        :rtype: bool: True if the course was updated, False otherwise.
        """

        response = self._requester(
            'PUT',
            'accounts/%s' % (self.id),
            **combine_kwargs(**kwargs)
        )

        if 'name' in response.json():
            super(Account, self).set_attributes(response.json())
            return True
        else:
            return False

    def enroll_by_id(self, enrollment_id):
        """
        Get an enrollment object by id
        :calls: `GET /api/v1/accounts/:account_id/enrollments/:id
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.show>
        :rtype: enrollment
        """
        from enrollment import Enrollment

        response = self._requester(
            'GET',
            'accounts/%s/enrollments/%s' % (self.id, enrollment.id),
        )
        return response.json()


class AccountNotification(CanvasObject):
    def __str__(self):
        return "subject: %s, message: %s" % (
            self.subject,
            self.message
        )


class AccountReport(CanvasObject):
    def __str__(self):
        return "id: %s, report: %s" % (
            self.id,
            self.report
        )
