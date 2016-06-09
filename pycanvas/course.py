from canvas_object import CanvasObject
from util import combine_kwargs
from paginated_list import PaginatedList
from exceptions import RequiredFieldMissing


class Course(CanvasObject):

    def __str__(self):
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
            event="conclude",
            var="blarg"
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
        :type user_id: int
        :param user_id_type: The type of the ID to search for.
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

    def list_enrollments(self):
        """
        List all of the enrollments in this course.

        :calls: `GET /api/v1/courses/:course_id/enrollments \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.enrollment.Enrollment`
        """
        from enrollment import Enrollment
        return PaginatedList(
            Enrollment,
            self._requester,
            'GET',
            'courses/%s/enrollments' % (self.id)
        )

    def get_assignment(self, assignment_id):
        """
        Return the assignment with the given ID.

        :calls: `GET /api/v1/courses/:course_id/assignments/:id \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.show>`_

        :param assignment_id: The ID of the assignment to retrieve.
        :type assignment_id: int
        :rtype: :class:`pycanvas.assignment.Assignment`
        """
        from assignment import Assignment

        response = self._requester.request(
            'GET',
            'courses/%s/assignments/%s' % (self.id, assignment_id),
        )
        return Assignment(self._requester, response.json())

    def get_assignments(self):
        """
        List all of the assignments in this course.

        :calls: `GET /api/v1/courses/:course_id/assignments \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.assignment.Assignment`
        """
        from assignment import Assignment

        return PaginatedList(
            Assignment,
            self._requester,
            'GET',
            'courses/%s/assignments' % (self.id)
        )

    def create_assignment(self, **kwargs):
        """
        Create a new assignment for this course.

        Note: The assignment is created in the active state.

        :calls: `POST /api/v1/courses/:course_id/assignments \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.create>`_

        :rtype: :class:`pycanvas.assignment.Assignment`
        """
        from assignment import Assignment

        response = self._requester.request(
            'POST',
            'courses/%s/assignments' % (self.id),
            **combine_kwargs(**kwargs)
        )

        return Assignment(self._requester, response.json())

    def get_quizzes(self, **kwargs):
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
            {'course_id': self.id},
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
        quiz_json = response.json()
        quiz_json.update({'course_id': self.id})

        return Quiz(self._requester, quiz_json)

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
        quiz_json = response.json()
        quiz_json.update({'course_id': self.id})

        return Quiz(self._requester, quiz_json)

    def get_modules(self, **kwargs):
        """
        Return a list of modules in this course.

        :calls: `GET /api/v1/courses/:course_id/modules \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.index>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.module.Module`
        """
        from module import Module

        return PaginatedList(
            Module,
            self._requester,
            'GET',
            'courses/%s/modules' % (self.id),
            {'course_id': self.id},
            **combine_kwargs(**kwargs)
        )

    def get_module(self, module_id, **kwargs):
        """
        Retrieve a single module by ID.

        :calls: `GET /api/v1/courses/:course_id/modules/:id \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.show>`_

        :param module_id: The ID of the module to retrieve.
        :type module_id: int
        :rtype: :class:`pycanvas.module.Module`
        """
        from module import Module

        response = self._requester.request(
            'GET',
            'courses/%s/modules/%s' % (self.id, module_id),
        )
        module_json = response.json()
        module_json.update({'course_id': self.id})

        return Module(self._requester, module_json)

    def create_module(self, module, **kwargs):
        """
        Create a new module.

        :calls: `POST /api/v1/courses/:course_id/modules \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.create>`_

        :param module: The attributes for the module.
        :type module: dict
        :returns: The created module.
        :rtype: :class:`pycanvas.module.Module`
        """
        from module import Module

        if isinstance(module, dict) and 'name' in module:
            kwargs['module'] = module
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")

        response = self._requester.request(
            'POST',
            'courses/%s/modules' % (self.id),
            **combine_kwargs(**kwargs)
        )
        module_json = response.json()
        module_json.update({'course_id': self.id})

        return Module(self._requester, module_json)

    def deactivate_enrollment(self, enrollment_id, action):
        """
        Delete, conclude, or deactivate an enrollment.

        The following actions can be performed on an enrollment: conclude, delete, \
        inactivate, deactivate.

        :calls: `DELETE /api/v1/courses/:course_id/enrollments/:id \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.destroy>`_

        :param enrollment_id: The ID of the enrollment to modify.
        :type enrollment_id: int
        :param action: The action to perform on the enrollment.
        :type action: str
        :rtype: :class:`pycanvas.enrollment.Enrollment`
        """
        from enrollment import Enrollment

        ALLOWED_ACTIONS = ['conclude', 'delete', 'inactivate', 'deactivate']

        if not action in ALLOWED_ACTIONS:
            raise ValueError('%s is not a valid action. Please use one of the following: %s' % (
                action,
                ','.join(ALLOWED_ACTIONS)
            ))

        response = self._requester.request(
            'DELETE',
            'courses/%s/enrollments/%s' % (self.id, enrollment_id)
        )
        return Enrollment(self._requester, response.json())

    def reactivate_enrollment(self, enrollment_id):
        """
        Activate an inactive enrollment.

        :calls: `PUT /api/v1/courses/:course_id/enrollments/:id/reactivate \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.reactivate>`_

        :param enrollment_id: The ID of the enrollment to reactivate.
        :type enrollment_id: int
        :rtype: :class:`pycanvas.enrollment.Enrollment`
        """
        from enrollment import Enrollment

        response = self._requester.request(
            'PUT',
            'courses/%s/enrollments/%s/reactivate' % (self.id, enrollment_id)
        )
        return Enrollment(self._requester, response.json())

    def get_section(self, section_id):
        """
        Retrieve a section.

        :calls: `GET /api/v1/courses/:course_id/sections/:id \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.index>`_

        :param section_id: The ID of the section to retrieve.
        :type section_id: int
        :rtype: :class:`pycanvas.section.Section`
        """
        from section import Section

        response = self._requester.request(
            'GET',
            'courses/%s/sections/%s' % (self.id, section_id)
        )
        return Section(self._requester, response.json())

    def show_front_page(self):
        """
        Retrieve the content of the front page.

        :calls: `GET /api/v1/courses/:course_id/front_page \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_front_page>`_

        :rtype: :class:`pycanvas.course.Course`
        """
        response = self._requester.request(
            'GET',
            'courses/%s/front_page' % (self.id)
        )
        return Page(self._requester, response.json())

    def create_front_page(self, **kwargs):
        """
        Update the title or contents of the front page.

        :calls: `PUT /api/v1/courses/:course_id/front_page \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update_front_page>`_

        :rtype: :class:`pycanvas.course.Course`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/front_page' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return Page(self._requester, response.json())


class CourseNickname(CanvasObject):

    def __str__(self):
        return "course_id: %s, name: %s, nickname: %s, " % (
            self.course_id,
            self.name,
            self.nickname
        )

    def remove(self):
        """
        Remove the nickname for the given course. Subsequent course API
        calls will return the actual name for the course.

        :calls: `DELETE /api/v1/users/self/course_nicknames/:course_id \
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.delete>`_

        :rtype: :class:`pycanvas.course.CourseNickname`
        """
        response = self._requester.request(
            'DELETE',
            'users/self/course_nicknames/%s' % (self.course_id)
        )
        return CourseNickname(self._requester, response.json())


class Page(CanvasObject):

    def __str__(self):
        return "url: %s, title: %s" % (
            self.url,
            self.title
        )
