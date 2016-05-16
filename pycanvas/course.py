from canvas_object import CanvasObject
from util import combine_kwargs
from paginated_list import PaginatedList


class Course(CanvasObject):

    def __str__(self):  # pragma: no cover
        return "%s %s %s" % (self.id, self.course_code, self.name)

    def conclude(self):
        """
        Mark this course as concluded.

        :calls: `DELETE /api/v1/courses/:id \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.destroy>`_

        :returns: True if the course was concluded, False otherwise.
        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s' % (self.id),
            event="conclude"
        )
        return response.json().get('conclude')

    def delete(self):
        """
        Permanently delete this course.

        :calls: `DELETE /api/v1/courses/:id \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.destroy>`_

        :returns: True if the course was deleted, False otherwise.
        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s' % (self.id),
            event="delete"
        )
        return response.json().get('delete')

    def update(self, **kwargs):
        """
        Update this course.

        :calls: `PUT /api/v1/courses/:id \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.update>`_

        :returns: True if the course was updated, False otherwise.
        :rtype: bool
        """
        response = self._requester.request(
            'PUT',
            'courses/%s' % (self.id),
            **combine_kwargs(**kwargs)
        )

        if response.json().get('name'):
            super(Course, self).set_attributes(response.json())

        return response.json().get('name')

    def get_user(self, user_id, user_id_type=None):
        """
        Retrieve a user by their ID. `user_id_type` denotes which endpoint to try as there are
        several different ids that can pull the same user record from Canvas.

        :calls: `GET /api/v1/courses/:course_id/users/:id \
        <https://canvas.instructure.com/doc/api/users.html#method.users.api_show>`_

        :param user_id: The ID of the user to retrieve.
        :type user: int
        :param: user_id_type: The type of the ID to search for.
        :type user_id_type: str
        :rtype: :class:`pycanvas.user.User`
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

    def get_users(self, search_term=None, **kwargs):
        """
        List all users in a course.

        If a `search_term` is provided, only matching users will be included
        in the returned list.

        :calls: `GET /api/v1/courses/:course_id/search_users \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.users>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.user.User`
        """
        from user import User

        return PaginatedList(
            User,
            self._requester,
            'GET',
            'courses/%s/search_users' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def enroll_user(self, user, enrollment_type, **kwargs):
        """
        Create a new user enrollment for a course or a section.

        :calls: `POST /api/v1/courses/:course_id/enrollments \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.create>`_

        :param user: The user to enroll in this course.
        :type user: :class:`pycanvas.user.User`
        :param enrollment_type: The type of enrollment.
        :type enrollment_type: str
        :rtype: :class:`pycanvas.enrollment.Enrollment`
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
        Return a list of students in the course ordered by how recently they
        have logged in.

        :calls: `GET /api/v1/courses/:course_id/recent_students \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.recent_students>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.user.User`
        """
        from user import User

        return PaginatedList(
            User,
            self._requester,
            'GET',
            'courses/%s/recent_students' % (self.id)
        )

    def preview_html(self, html):
        """
        Preview HTML content processed for this course.

        :calls: `POST /api/v1/courses/:course_id/preview_html \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.preview_html>`_

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
        Returns this course's settings.

        :calls: `GET /api/v1/courses/:course_id/settings \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.settings>`_

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

        :calls: `PUT /api/v1/courses/:course_id/settings \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.update_settings>`_

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
        Delete the current course and create a new equivalent course
        with no content, but all sections and users moved over.

        :calls: `POST /api/v1/courses/:course_id/reset_content \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.reset_content>`_

        :rtype: :class:`pycanvas.course.Course`
        """
        response = self._requester.request(
            'POST',
            'courses/%s/reset_content' % (self.id),
        )
        return Course(self._requester, response.json())

    def list_quizzes(self, **kwargs):
        """
        Return a list of quizzes belonging to this course.

        :calls: `GET /api/v1/courses/:course_id/quizzes \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.index>`_
        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.quiz.Quiz`
        """
        from quiz import Quiz
        return PaginatedList(
            Quiz,
            self._requester,
            'GET',
            'courses/%s/quizzes' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def get_quiz(self, quiz_id):
        """
        Return the quiz with the given id.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:id \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.show>`_

        :param quiz_id: The ID of the quiz to retrieve.
        :type quiz_id: int
        :rtype: :class:`pycanvas.quiz.Quiz`
        """
        from quiz import Quiz
        response = self._requester.request(
            'GET',
            'courses/%s/quizzes/%s' % (self.id, quiz_id)
        )
        return Quiz(self._requester, response.json())

    def create_quiz(self, title, **kwargs):
        """
        Create a new quiz in this course.

        :calls: `POST /api/v1/courses/:course_id/quizzes \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.create>`_

        :param title: The title of the quiz.
        :type title: str
        :rtype: :class:`pycanvas.quiz.Quiz`
        """
        from quiz import Quiz
        response = self._requester.request(
            'POST',
            'courses/%s/quizzes' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return Quiz(self._requester, response.json())
