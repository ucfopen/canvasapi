from canvas_object import CanvasObject
from util import combine_kwargs
from paginated_list import PaginatedList


class Course(CanvasObject):

    def conclude(self):
        """
        Marks the course as concluded.

        :calls: `DELETE /api/v1/courses/:id
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.destroy>`
        :rtype: bool: True if the course was concluded, False otherwise.
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s' % (self.id),
            event="conclude"
        )
        response_json = response.json()
        return response_json.get('conclude', False)

    def delete(self):
        """
        Permanently deletes the course.

        :calls: `DELETE /api/v1/courses/:id
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.destroy>`
        :rtype: bool: True if the course was deleted, False otherwise.
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s' % (self.id),
            event="delete"
        )
        response_json = response.json()
        return response_json.get('delete', False)

    def update(self, **kwargs):
        """
        Updates the course.

        :calls: `PUT /api/v1/courses/:id
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.update>`
        :rtype: bool: True if the course was updated, False otherwise.
        """
        try:
            response = self._requester.request(
                'PUT',
                'courses/%s' % (self.id),
                **combine_kwargs(**kwargs)
            )

            super(Course, self).set_attributes(response.json())
            return True
        except Exception:
            return False

    def get_users(self, search_term=None, **kwargs):
        """
        Lists all users in a course.
        If a `search_term` is provided, only returns matching users

        :calls: `GET /api/v1/courses/:course_id/search_users
        https://canvas.instructure.com/doc/api/courses.html#method.courses.users`
        :rtype: :class:`PaginatedList` of :class:`User`

        """
        from user import User

        return PaginatedList(
            User,
            self._requester,
            'GET',
            'courses/%s/search_users' % (self.id),
            search_term=search_term,
            **combine_kwargs(**kwargs)
        )

    def __str__(self):
        return "%s %s %s" % (self.id, self.course_code, self.name)
