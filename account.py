from canvas_object import CanvasObject
from exceptions import RequiredFieldMissing
from paginated_list import PaginatedList
from util import combine_kwargs


class Account(CanvasObject):

    def __str__(self):
        return "id: %s, name: %s" % (
            self.id,
            self.name
        )

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
