from canvas_object import CanvasObject
from util import combine_kwargs, list_objs


class Course(CanvasObject):

    def __str__(self):
        return "%s %s %s" % (self.id, self.course_code, self.name)

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
        response = self._requester.request(
            'PUT',
            'courses/%s' % (self.id),
            **combine_kwargs(**kwargs)
        )

        if 'name' in response.json():
            super(Course, self).set_attributes(response.json())

        return 'name' in response.json()

    def get_user(self, user_id, user_id_type=None):
        """
        Retrieve a user by their ID. id_type denotes which endpoint to try as there are
        several different ids that can pull the same user record from Canvas.

        :calls: `GET /api/v1/courses/:course_id/users/:id`
        <https://canvas.instructure.com/doc/api/users.html#method.users.api_show>
        :param: user_id str
        :param: user_id_type str
        :rtype: :class: `pycanvas.user.User`
        """
        from user import User

        if user_id_type:
            uri = 'courses/%s/users/%s:%s' % (self.id, user_id_type, user_id)
        else:
            uri = 'courses/%s/users/%s' % (self.id, user_id)

        response = self._requester.request(
            'GET',
            uri
        )
        return User(self._requester, response.json())

    def get_users(self, **kwargs):
        """
        Lists all users in a course. If a filter is provided (`search_term` or
        `enrollment_type`), list only the users that matches the filter.

        :calls: `GET /api/v1/courses/:course_id/users`
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.users>
        :rtype: list: The list of users
        """
        from user import User

        response = self._requester.request(
            'GET',
            'courses/%s/search_users' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return list_objs(User, self._requester, response.json())

    def enroll_user(self, user, enrollment_type, **kwargs):
        """
        Create a new user enrollment for a course or a section.

        :calls: `POST /api/v1/courses/:course_id/enrollments
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.create>`
        :param user: the user to enroll
        :type user: :class:`pycanvas.user.User`
        :param enrollment_type: the type of enrollment
        :type enrollment_type: str
        :rtype: Enrollment: object representing the enrollment
        """
        from enrollment import Enrollment

        kwargs['enrollment[user_id]'] = user.id
        kwargs['enrollment[type]'] = enrollment_type

        response = self._requester.request(
            'POST',
            'courses/%s/enrollments' % (self.id),
            **combine_kwargs(**kwargs)
        )

        return Enrollment(self._requester, response.json())

    def get_recent_students(self):
        """
        Returns a list of students in the course ordered by how
        recently they have logged in.

        :calls: `GET /api/v1/courses/:course_id/recent_students`
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.recent_students>
        :rtype: list: list of User objects
        """
        from user import User

        response = self._requester.request(
            'GET',
            'courses/%s/recent_students' % (self.id)
        )

        return list_objs(User, self._requester, response.json())

    def preview_html(self, html):
        """
        Preview HTML content processed for this course.

        :calls: `POST /api/v1/courses/:course_id/preview_html`
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.preview_html>
        :param html: The HTML code to preview.
        :type html: str
        :rtype: str
        """
        response = self._requester.request(
            'POST',
            'courses/%s/preview_html' % (self.id),
            html=html
        )
        return response.json().get('html', '')

    def get_settings(self):
        """
        Returns some of a course's settings.

        :calls: `GET /api/v1/courses/:course_id/settings`
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.settings>
        :rtype: dict
        """
        response = self._requester.request(
            'GET',
            'courses/%s/settings' % (self.id)
        )
        return response.json()

    def update_settings(self, **kwargs):
        """
        Update a course's settings.

        :calls: `PUT /api/v1/courses/:course_id/settings`
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.update_settings>
        :rtype: dict
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/settings' % (self.id),
            **kwargs
        )
        return response.json()

    def reset(self):
        """
        Deletes the current course, and creates a new equivalent course
        with no content, but all sections and users moved over.

        :calls: `POST /api/v1/courses/:course_id/reset_content`
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.reset_content>
        :rtype: Course
        """
        response = self._requester.request(
            'POST',
            'courses/%s/reset_content' % (self.id),
        )
        return Course(self._requester, response.json())
