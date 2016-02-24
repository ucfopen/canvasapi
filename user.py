from canvas_object import CanvasObject
from course import Course

class User(CanvasObject):

    def profile(self, **kwargs):
        """
        Get a user's profile.

        :calls: `GET /api/v1/user/:id <https://canvas.instructure.com/doc/api/users.html#method.profile.settings>`
        :rtype: :class: `pycanvas.user.User`
        """
        response = self._requester.request(
            'GET',
            'users/%s/profile' % (id)
        )
        return response.json()

    def page_views(self):
        """
        Get a user's pageviews.

        :calls: `GET /api/v1/users/:user_id/page_views <https://canvas.instructure.com/doc/api/users.html#method.page_views.index>`
        :rtype :class: `pycanvas.user.User`
        """
        response = self._requester.request(
            'GET',
            'users/%s/page_views' % (self.id)
        )
        return response.json()

    def get_courses(self):
        """
        Get a user's courses.

        :calls: `GET /api/v1/users/:user_id/courses`
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.user_index>
        :rtype: list
        """
        response = self._requester.request(
            'GET',
            'users/%s/courses' % (self.id)
        )
        return [Course(self._requester, course) for course in response.json()]

    def __str__(self):
        return "%s" % (self.name)
