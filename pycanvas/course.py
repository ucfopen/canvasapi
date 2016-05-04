from canvas_object import CanvasObject
from util import combine_kwargs
from enrollment import Enrollment
from paginated_list import PaginatedList


class Course(CanvasObject):

    def __str__(self):  # pragma: no cover
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
            **combine_kwargs(**kwargs)
        )

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
        :rtype: :class:`PaginatedList` of :class:`User`
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

    def list_enrollments(self):
        """
        Lists all of the enrollments within a course.

        :calls: `GET /api/v1/courses/:course_id/enrollments`
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index>
        :rtype: :class:`PaginatedList` of :class:`Enrollment`
        """
        from enrollment import Enrollment
        return PaginatedList(
            Enrollment,
            self._requester,
            'GET',
            'courses/%s/enrollments' % (self.id)
        )

    def list_quizzes(self, **kwargs):
        """
        Returns the list of Quizzes in this course

        :calls: `GET /api/v1/courses/:course_id/quizzes`
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.index>
        :rtype: Quiz :class:`PaginatedList` of :class:`Quiz`
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
        Returns the quiz with the given id
        :calls: `GET /api/v1/courses/:course_id/quizzes/:id`
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.show>
        :rtype: Quiz
        """
        from quiz import Quiz
        response = self._requester.request(
            'GET',
            'courses/%s/quizzes/%s' % (self.id, quiz_id)
        )
        return Quiz(self._requester, response.json())

    def create_quiz(self, title, **kwargs):
        """
        Create a new quiz for a course
        :calls: `POST /api/v1/courses/:course_id/quizzes
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.create>
        :param title: string
        :rtype: Quiz
        """
        from quiz import Quiz
        response = self._requester.request(
            'POST',
            'courses/%s/quizzes' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return Quiz(self._requester, response.json())

    def deactivate_enrollment(self):
        """
        Delete, conclude or deactivate an enrollment
        :calls: `DELETE /api/v1/courses/:course_id/enrollments/:id`
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.destroy>
        :rtype: Enrollment
        """
        from enrollment import Enrollment

        response = self._requester(
            'DELETE',
            'courses/%s/enrollments/%s' % (self.id, enrollment.id)
        )
        return Enrollment(self._requester, response.json())

    def reactivate_enrollment(self):
        pass
