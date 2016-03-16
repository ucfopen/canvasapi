from course import Course
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

    def get_course(self, course_id):
        """
        Retrieve a course by its ID.

        :calls: `GET /courses/:id <https://canvas.instructure.com/doc/api/courses.html#method.courses.show>`
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
