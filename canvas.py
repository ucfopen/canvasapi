from pycanvas import Requester
from pycanvas import Course


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

    def get_course(self, id):
        """
        Retrieve a course by its ID.

        :calls: `GET /courses/:id <https://canvas.instructure.com/doc/api/courses.html#method.courses.show>
        :param id: int
        :rtype: :class:`pycanvas.course.Course`
        """
        response = self.__requester.request(
            'GET',
            'courses/%s' % (id)
        )
        return Course(self.__requester, response.json())
