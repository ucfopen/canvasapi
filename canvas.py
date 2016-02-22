from pycanvas import Requester
from pycanvas import Course
from pycanvas import util


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

        :calls: `POST /api/v1/accounts/:account_id/courses <https://canvas.instructure.com/doc/api/courses.html#method.courses.create>`
        :param account_id: int
        :rtype: :class:`pycanvas.course.Course`
        """
        kwargs['account_id'] = account_id
        data = util.combine_kwargs(**kwargs)

        response = self.__requester.request(
            'POST',
            'accounts/%s/courses' % (account_id),
            **data
        )
        return Course(self.__requester, response.json())

    def get_course(self, id):
        """
        Retrieve a course by its ID.

        :calls: `GET /courses/:id <https://canvas.instructure.com/doc/api/courses.html#method.courses.show>`
        :param id: int
        :rtype: :class:`pycanvas.course.Course`
        """
        response = self.__requester.request(
            'GET',
            'courses/%s' % (id)
        )
        return Course(self.__requester, response.json())
