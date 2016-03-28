from course import Course
from exceptions import RequiredFieldMissing
from paginated_list import PaginatedList
from requester import Requester
from user import User
from util import combine_kwargs


class Canvas(object):
    """
    The main class to be instantiated to provide access to Canvas's API.
    """

    def __init__(self, base_url, access_token):
        """
        :param base_url: string
        :param access_token: string
        """
        self.__requester = Requester(base_url, access_token)

    def create_course(self, account_id, **kwargs):
        """
        Create a course.

        :calls: `POST /api/v1/accounts/:account_id/courses
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.create>`
        :param account_id: int
        :rtype: :class:`pycanvas.course.Course`
        """
        response = self.__requester.request(
            'POST',
            'accounts/%s/courses' % (account_id),
            account_id=account_id,
            **combine_kwargs(**kwargs)
        )
        return Course(self.__requester, response.json())

    def create_user(self, account_id, pseudonym, **kwargs):
        """
        Create and return a new user and pseudonym for an account.

        :calls: `POST /api/v1/accounts/:account_id/users
        <https://canvas.instructure.com/doc/api/users.html#method.users.create>`
        :param account_id: int
        :param pseudonym: dict
        :rtype: :class: `User`
        """
        if isinstance(pseudonym, dict) and pseudonym.get('unique_id'):
            kwargs['pseudonym'] = pseudonym
        else:
            raise RequiredFieldMissing("Dictionary with key 'unique_id' is required.")

        response = self.__requester.request(
            'POST',
            'accounts/%s/users' % (account_id),
            **combine_kwargs(**kwargs)
        )
        return User(self.__requester, response.json())

    def get_course(self, course_id):
        """
        Retrieve a course by its ID.

        :calls: `GET /courses/:id
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.show>`
        :param course_id: int
        :rtype: :class:`pycanvas.course.Course`
        """
        response = self.__requester.request(
            'GET',
            'courses/%s' % (course_id)
        )
        return Course(self.__requester, response.json())

    def get_user(self, user_id, id_type=None):
        """
        Retrieve a user by their ID. `id_type` denotes which endpoint to try as there are
        several different ids that can pull the same user record from Canvas.

        :calls: `GET /users/:id
        <https://canvas.instructure.com/doc/api/users.html#method.users.api_show>`
        :param: user_id str
        :param: id_type str
        :rtype: :class: `pycanvas.user.User`
        """
        if id_type:
            uri = 'users/%s:%s' % (id_type, user_id)
        else:
            uri = 'users/%s' % (user_id)

        response = self.__requester.request(
            'GET',
            uri
        )
        return User(self.__requester, response.json())

    def get_courses(self):
        """
        Returns the list of active courses for the current user.

        :calls: `GET /api/v1/courses
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.index>`
        :rtype: :class:`PaginatedList` of :class:`Course`
        """
        return PaginatedList(
            Course,
            self.__requester,
            'GET',
            'courses'
        )

    def get_users(self, account_id, **kwargs):
        """
        Retrieve the list of users associated with this account.

        :calls: `GET /api/v1/accounts/:account_id/users
        <https://canvas.instructure.com/doc/api/users.html#method.users.index>`
        :param account_id: int
        :rtype: :class:`PaginatedList` of :class:`User`
        """
        return PaginatedList(
            User,
            self.__requester,
            'GET',
            'accounts/%s/users' % (account_id),
            **kwargs
        )

    def get_activity_stream_summary(self):
        """
        Returns a summary of the current user's global activity stream.

        :calls: `GET /api/v1/users/self/activity_stream/summary
        <https://canvas.instructure.com/doc/api/users.html#method.users.activity_stream_summary>`
        :rtype: dict
        """
        response = self.__requester.request(
            'GET',
            'users/self/activity_stream/summary'
        )
        return response.json()

    def get_todo_items(self):
        """
        Returns the current user's list of todo items, as seen on the user dashboard.

        :calls: `GET /api/v1/users/self/todo
        <https://canvas.instructure.com/doc/api/users.html#method.users.todo_items>`
        :rtype: dict
        """
        response = self.__requester.request(
            'GET',
            'users/self/todo'
        )
        return response.json()

    def get_upcoming_events(self):
        """
        Returns the current user's upcoming events, i.e. the same
        things shown in the dashboard 'Coming Up' sidebar.

        :calls: `GET /api/v1/users/self/upcoming_events
        <https://canvas.instructure.com/doc/api/users.html#method.users.upcoming_events>`
        :rtype: dict
        """
        response = self.__requester.request(
            'GET',
            'users/self/upcoming_events'
        )
        return response.json()

    def get_course_nicknames(self):
        """
        Returns all course nicknames you have set.

        :calls: `GET /api/v1/users/self/course_nicknames
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.index>`
        :rtype: :class:`PaginatedList` of :class:`CourseNickname`
        """
        from course_nickname import CourseNickname

        return PaginatedList(
            CourseNickname,
            self.__requester,
            'GET',
            'users/self/course_nicknames'
        )

    def get_course_nickname(self, course_id):
        """
        Returns all course nicknames you have set.

        :calls: `GET /api/v1/users/self/course_nicknames/:course_id
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.show>`
        :param course_id: int
        :rtype: :class:`CourseNickname`
        """
        from course_nickname import CourseNickname

        response = self.__requester.request(
            'GET',
            'users/self/course_nicknames/%s' % (course_id)
        )
        return CourseNickname(self.__requester, response.json())

    def set_course_nickname(self, course_id, nickname):
        """
        Set a nickname for the given course. This will replace the
        course's name in output of API calls you make subsequently, as
        well as in selected places in the Canvas web user interface.

        :calls: `PUT /api/v1/users/self/course_nicknames/:course_id
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.update>`
        :param course_id: int
        :param nickname: str
        :rtype: :class:`CourseNickname`
        """
        from course_nickname import CourseNickname

        response = self.__requester.request(
            'PUT',
            'users/self/course_nicknames/%s' % (course_id),
            nickname=nickname
        )
        return CourseNickname(self.__requester, response.json())

    def clear_course_nicknames(self):
        """
        Remove all stored course nicknames.

        :calls: `DELETE /api/v1/users/self/course_nicknames
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.delete>`
        :rtype: dict
        """

        response = self.__requester.request(
            'DELETE',
            'users/self/course_nicknames'
        )
        return response.json()
