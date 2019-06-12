from __future__ import absolute_import, division, print_function, unicode_literals

import warnings

from six import python_2_unicode_compatible, text_type, string_types

from canvasapi.blueprint import BlueprintSubscription
from canvasapi.canvas_object import CanvasObject
from canvasapi.discussion_topic import DiscussionTopic
from canvasapi.grading_standard import GradingStandard
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.folder import Folder
from canvasapi.page import Page
from canvasapi.paginated_list import PaginatedList
from canvasapi.progress import Progress
from canvasapi.quiz import QuizExtension
from canvasapi.tab import Tab
from canvasapi.submission import Submission
from canvasapi.upload import Uploader
from canvasapi.util import combine_kwargs, is_multivalued, obj_or_id
from canvasapi.rubric import Rubric

warnings.simplefilter('always', DeprecationWarning)


@python_2_unicode_compatible
class Course(CanvasObject):

    def __str__(self):
        return '{} {} ({})'.format(self.course_code, self.name, self.id)

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
            'courses/{}'.format(self.id),
            event="conclude"
        )

        return response.json().get('conclude')

    def create_assignment_overrides(self, assignment_overrides, **kwargs):
        """
        Create the specified overrides for each assignment.

        :calls: `POST /api/v1/courses/:course_id/assignments/overrides \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.batch_create>`_

        :param assignment_overrides: Attributes for the new assignment overrides.
        :type assignment_overrides: list

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.AssignmentOverride`
        """
        from canvasapi.assignment import AssignmentOverride

        kwargs['assignment_overrides'] = assignment_overrides

        return PaginatedList(
            AssignmentOverride,
            self._requester,
            'POST',
            'courses/{}/assignments/overrides'.format(self.id),
            {'course_id': self.id},
            _kwargs=combine_kwargs(**kwargs)
        )

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
            'courses/{}'.format(self.id),
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
            'courses/{}'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        if response.json().get('name'):
            super(Course, self).set_attributes(response.json())

        return response.json().get('name')

    def update_assignment_overrides(self, assignment_overrides, **kwargs):
        """
        Update a list of specified overrides for each assignment.

        Note: All current overridden values must be supplied if they are to be retained.

        :calls: `PUT /api/v1/courses/:course_id/assignments/overrides \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.batch_update>`_

        :param assignment_overrides: Attributes for the updated assignment overrides.
        :type assignment_overrides: list

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.AssignmentOverride`
        """
        from canvasapi.assignment import AssignmentOverride

        kwargs['assignment_overrides'] = assignment_overrides

        return PaginatedList(
            AssignmentOverride,
            self._requester,
            'PUT',
            'courses/{}/assignments/overrides'.format(self.id),
            {'course_id': self.id},
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_user(self, user, user_id_type=None):
        """
        Retrieve a user by their ID. `user_id_type` denotes which endpoint to try as there are
        several different ids that can pull the same user record from Canvas.

        :calls: `GET /api/v1/courses/:course_id/users/:id \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.user>`_

        :param user: The object or ID of the user to retrieve.
        :type user: :class:`canvasapi.user.User` or int
        :param user_id_type: The type of the ID to search for.
        :type user_id_type: str

        :rtype: :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

        if user_id_type:
            uri = 'courses/{}/users/{}:{}'.format(self.id, user_id_type, user)
        else:
            user_id = obj_or_id(user, "user", (User,))
            uri = 'courses/{}/users/{}'.format(self.id, user_id)

        response = self._requester.request(
            'GET',
            uri
        )
        return User(self._requester, response.json())

    def get_users(self, **kwargs):
        """
        List all users in a course.

        :calls: `GET /api/v1/courses/:course_id/search_users \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.users>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

        return PaginatedList(
            User,
            self._requester,
            'GET',
            'courses/{}/search_users'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def enroll_user(self, user, enrollment_type, **kwargs):
        """
        Create a new user enrollment for a course or a section.

        :calls: `POST /api/v1/courses/:course_id/enrollments \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.create>`_

        :param user: The object or ID of the user to enroll in this course.
        :type user: :class:`canvasapi.user.User` or int
        :param enrollment_type: The type of enrollment.
        :type enrollment_type: str
        :rtype: :class:`canvasapi.enrollment.Enrollment`
        """
        from canvasapi.enrollment import Enrollment
        from canvasapi.user import User

        kwargs['enrollment[user_id]'] = obj_or_id(user, "user", (User,))
        kwargs['enrollment[type]'] = enrollment_type

        response = self._requester.request(
            'POST',
            'courses/{}/enrollments'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        return Enrollment(self._requester, response.json())

    def get_recent_students(self):
        """
        Return a list of students in the course ordered by how recently they
        have logged in.

        :calls: `GET /api/v1/courses/:course_id/recent_students \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.recent_students>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

        return PaginatedList(
            User,
            self._requester,
            'GET',
            'courses/{}/recent_students'.format(self.id)
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
            'courses/{}/preview_html'.format(self.id),
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
            'courses/{}/settings'.format(self.id)
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
            'courses/{}/settings'.format(self.id),
            **kwargs
        )
        return response.json()

    def upload(self, file, **kwargs):
        """
        Upload a file to this course.

        :calls: `POST /api/v1/courses/:course_id/files \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.create_file>`_

        :param file: The file or path of the file to upload.
        :type file: file or str
        :returns: True if the file uploaded successfully, False otherwise, \
                    and the JSON response from the API.
        :rtype: tuple
        """
        return Uploader(
            self._requester,
            'courses/{}/files'.format(self.id),
            file,
            **kwargs
        ).start()

    def reset(self):
        """
        Delete the current course and create a new equivalent course
        with no content, but all sections and users moved over.

        :calls: `POST /api/v1/courses/:course_id/reset_content \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.reset_content>`_

        :rtype: :class:`canvasapi.course.Course`
        """
        response = self._requester.request(
            'POST',
            'courses/{}/reset_content'.format(self.id),
        )
        return Course(self._requester, response.json())

    def get_enrollments(self, **kwargs):
        """
        List all of the enrollments in this course.

        :calls: `GET /api/v1/courses/:course_id/enrollments \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.enrollment.Enrollment`
        """
        from canvasapi.enrollment import Enrollment
        return PaginatedList(
            Enrollment,
            self._requester,
            'GET',
            'courses/{}/enrollments'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_assignment(self, assignment, **kwargs):
        """
        Return the assignment with the given ID.

        :calls: `GET /api/v1/courses/:course_id/assignments/:id \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.show>`_

        :param assignment: The object or ID of the assignment to retrieve.
        :type assignment: :class:`canvasapi.assignment.Assignment` or int

        :rtype: :class:`canvasapi.assignment.Assignment`
        """
        from canvasapi.assignment import Assignment

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))

        response = self._requester.request(
            'GET',
            'courses/{}/assignments/{}'.format(self.id, assignment_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return Assignment(self._requester, response.json())

    def get_assignment_overrides(self, assignment_overrides, **kwargs):
        """
        List the specified overrides in this course, providing they target
            sections/groups/students visible to the current user.

        :calls: `GET /api/v1/courses/:course_id/assignments/overrides \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.batch_retrieve>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.AssignmentOverride`
        """
        from canvasapi.assignment import AssignmentOverride

        kwargs['assignment_overrides'] = assignment_overrides

        return PaginatedList(
            AssignmentOverride,
            self._requester,
            'GET',
            'courses/{}/assignments/overrides'.format(self.id),
            {'course_id': self.id},
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_assignments(self, **kwargs):
        """
        List all of the assignments in this course.

        :calls: `GET /api/v1/courses/:course_id/assignments \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.Assignment`
        """
        from canvasapi.assignment import Assignment

        return PaginatedList(
            Assignment,
            self._requester,
            'GET',
            'courses/{}/assignments'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def create_assignment(self, assignment, **kwargs):
        """
        Create a new assignment for this course.

        Note: The assignment is created in the active state.

        :calls: `POST /api/v1/courses/:course_id/assignments \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.create>`_

        :param assignment: The attributes of the assignment
        :type assignment: dict
        :rtype: :class:`canvasapi.assignment.Assignment`
        """
        from canvasapi.assignment import Assignment

        if isinstance(assignment, dict) and 'name' in assignment:
            kwargs['assignment'] = assignment
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")

        response = self._requester.request(
            'POST',
            'courses/{}/assignments'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        return Assignment(self._requester, response.json())

    def get_quizzes(self, **kwargs):
        """
        Return a list of quizzes belonging to this course.

        :calls: `GET /api/v1/courses/:course_id/quizzes \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.quiz.Quiz`
        """
        from canvasapi.quiz import Quiz
        return PaginatedList(
            Quiz,
            self._requester,
            'GET',
            'courses/{}/quizzes'.format(self.id),
            {'course_id': self.id},
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_quiz(self, quiz):
        """
        Return the quiz with the given id.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:id \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.show>`_

        :param quiz: The object or ID of the quiz to retrieve.
        :type quiz: :class:`canvasapi.quiz.Quiz` or int

        :rtype: :class:`canvasapi.quiz.Quiz`
        """
        from canvasapi.quiz import Quiz

        quiz_id = obj_or_id(quiz, "quiz", (Quiz,))

        response = self._requester.request(
            'GET',
            'courses/{}/quizzes/{}'.format(self.id, quiz_id)
        )
        quiz_json = response.json()
        quiz_json.update({'course_id': self.id})

        return Quiz(self._requester, quiz_json)

    def create_quiz(self, quiz, **kwargs):
        """
        Create a new quiz in this course.

        :calls: `POST /api/v1/courses/:course_id/quizzes \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.create>`_

        :param quiz: The attributes for the quiz.
        :type quiz: dict
        :rtype: :class:`canvasapi.quiz.Quiz`
        """
        from canvasapi.quiz import Quiz

        if isinstance(quiz, dict) and 'title' in quiz:
            kwargs['quiz'] = quiz
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")

        response = self._requester.request(
            'POST',
            'courses/{}/quizzes'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        quiz_json = response.json()
        quiz_json.update({'course_id': self.id})

        return Quiz(self._requester, quiz_json)

    def get_modules(self, **kwargs):
        """
        Return a list of modules in this course.

        :calls: `GET /api/v1/courses/:course_id/modules \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.module.Module`
        """
        from canvasapi.module import Module

        return PaginatedList(
            Module,
            self._requester,
            'GET',
            'courses/{}/modules'.format(self.id),
            {'course_id': self.id},
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_module(self, module, **kwargs):
        """
        Retrieve a single module by ID.

        :calls: `GET /api/v1/courses/:course_id/modules/:id \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.show>`_

        :param module: The object or ID of the module to retrieve.
        :type module: :class:`canvasapi.module.Module` or int

        :rtype: :class:`canvasapi.module.Module`
        """
        from canvasapi.module import Module

        module_id = obj_or_id(module, "module", (Module,))

        response = self._requester.request(
            'GET',
            'courses/{}/modules/{}'.format(self.id, module_id),
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
        :rtype: :class:`canvasapi.module.Module`
        """
        from canvasapi.module import Module

        if isinstance(module, dict) and 'name' in module:
            kwargs['module'] = module
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")

        response = self._requester.request(
            'POST',
            'courses/{}/modules'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        module_json = response.json()
        module_json.update({'course_id': self.id})

        return Module(self._requester, module_json)

    def get_external_tool(self, tool):
        """
        :calls: `GET /api/v1/courses/:course_id/external_tools/:external_tool_id \
        <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.show>`_

        :param tool: The object or ID of the tool to retrieve.
        :type tool: :class:`canvasapi.external_tool.ExternalTool` or int

        :rtype: :class:`canvasapi.external_tool.ExternalTool`
        """
        from canvasapi.external_tool import ExternalTool

        tool_id = obj_or_id(tool, "tool", (ExternalTool,))

        response = self._requester.request(
            'GET',
            'courses/{}/external_tools/{}'.format(self.id, tool_id),
        )
        tool_json = response.json()
        tool_json.update({'course_id': self.id})

        return ExternalTool(self._requester, tool_json)

    def get_external_tools(self, **kwargs):
        """
        :calls: `GET /api/v1/courses/:course_id/external_tools \
        <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.external_tool.ExternalTool`
        """
        from canvasapi.external_tool import ExternalTool

        return PaginatedList(
            ExternalTool,
            self._requester,
            'GET',
            'courses/{}/external_tools'.format(self.id),
            {'course_id': self.id},
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_sections(self, **kwargs):
        """
        List all sections in a course.

        :calls: `GET /api/v1/courses/:course_id/sections \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.section.Section`
        """
        from canvasapi.section import Section

        return PaginatedList(
            Section,
            self._requester,
            'GET',
            'courses/{}/sections'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_section(self, section, **kwargs):
        """
        Retrieve a section.

        :calls: `GET /api/v1/courses/:course_id/sections/:id \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.show>`_

        :param section: The object or ID of the section to retrieve.
        :type section: :class:`canvasapi.section.Section` or int

        :rtype: :class:`canvasapi.section.Section`
        """
        from canvasapi.section import Section

        section_id = obj_or_id(section, "section", (Section,))

        response = self._requester.request(
            'GET',
            'courses/{}/sections/{}'.format(self.id, section_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return Section(self._requester, response.json())

    def show_front_page(self):
        """
        Retrieve the content of the front page.

        :calls: `GET /api/v1/courses/:course_id/front_page \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_front_page>`_

        :rtype: :class:`canvasapi.course.Course`
        """
        response = self._requester.request(
            'GET',
            'courses/{}/front_page'.format(self.id)
        )
        page_json = response.json()
        page_json.update({'course_id': self.id})

        return Page(self._requester, page_json)

    def edit_front_page(self, **kwargs):
        """
        Update the title or contents of the front page.

        :calls: `PUT /api/v1/courses/:course_id/front_page \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update_front_page>`_

        :rtype: :class:`canvasapi.course.Course`
        """
        response = self._requester.request(
            'PUT',
            'courses/{}/front_page'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        page_json = response.json()
        page_json.update({'course_id': self.id})

        return Page(self._requester, page_json)

    def get_pages(self, **kwargs):
        """
        List the wiki pages associated with a course.

        :calls: `GET /api/v1/courses/:course_id/pages \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.Course`
        """
        return PaginatedList(
            Page,
            self._requester,
            'GET',
            'courses/{}/pages'.format(self.id),
            {'course_id': self.id},
            _kwargs=combine_kwargs(**kwargs)
        )

    def create_page(self, wiki_page, **kwargs):
        """
        Create a new wiki page.

        :calls: `POST /api/v1/courses/:course_id/pages \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.create>`_

        :param title: The title for the page.
        :type title: dict
        :returns: The created page.
        :rtype: :class:`canvasapi.course.Course`
        """

        if isinstance(wiki_page, dict) and 'title' in wiki_page:
            kwargs['wiki_page'] = wiki_page
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")

        response = self._requester.request(
            'POST',
            'courses/{}/pages'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        page_json = response.json()
        page_json.update({'course_id': self.id})

        return Page(self._requester, page_json)

    def get_page(self, url):
        """
        Retrieve the contents of a wiki page.

        :calls: `GET /api/v1/courses/:course_id/pages/:url \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show>`_

        :param url: The url for the page.
        :type url: str
        :returns: The specified page.
        :rtype: :class:`canvasapi.course.Course`
        """

        response = self._requester.request(
            'GET',
            'courses/{}/pages/{}'.format(self.id, url)
        )
        page_json = response.json()
        page_json.update({'course_id': self.id})

        return Page(self._requester, page_json)

    def list_sections(self, **kwargs):
        """
        Returns the list of sections for this course.

        .. warning::
            .. deprecated:: 0.9.0
                Use :func:`canvasapi.course.Course.get_sections` instead.

        :calls: `GET /api/v1/courses/:course_id/sections \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.section.Section`
        """
        warnings.warn(
            "`list_sections` is being deprecated and will be removed in a future version."
            " Use `get_sections` instead",
            DeprecationWarning
        )
        return self.get_sections(**kwargs)

    def create_course_section(self, **kwargs):
        """
        Create a new section for this course.

        :calls: `POST /api/v1/courses/:course_id/sections \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.create>`_

        :rtype: :class:`canvasapi.course.Section`
        """

        from canvasapi.section import Section
        response = self._requester.request(
            'POST',
            'courses/{}/sections'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        return Section(self._requester, response.json())

    def list_groups(self, **kwargs):
        """
        Return list of active groups for the specified course.

        .. warning::
            .. deprecated:: 0.10.0
                Use :func:`canvasapi.course.Course.get_groups` instead.

        :calls: `GET /api/v1/courses/:course_id/groups \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.context_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.Course`
        """
        warnings.warn(
            "`list_groups` is being deprecated and will be removed in a future version."
            " Use `get_groups` instead",
            DeprecationWarning
        )

        return self.get_groups(**kwargs)

    def get_groups(self, **kwargs):
        """
        Return list of active groups for the specified course.

        :calls: `GET /api/v1/courses/:course_id/groups \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.context_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.Course`
        """
        from canvasapi.group import Group
        return PaginatedList(
            Group,
            self._requester,
            'GET',
            'courses/{}/groups'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def create_group_category(self, name, **kwargs):
        """
        Create a group category.

        :calls: `POST /api/v1/courses/:course_id/group_categories \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.create>`_

        :param name: Name of the category.
        :type name: str
        :rtype: :class:`canvasapi.group.GroupCategory`
        """
        from canvasapi.group import GroupCategory

        response = self._requester.request(
            'POST',
            'courses/{}/group_categories'.format(self.id),
            name=name,
            _kwargs=combine_kwargs(**kwargs)
        )
        return GroupCategory(self._requester, response.json())

    def list_group_categories(self, **kwargs):
        """
        List group categories for a context.

        .. warning::
            .. deprecated:: 0.10.0
                Use :func:`canvasapi.course.Course.get_group_categories` instead.

        :calls: `GET /api/v1/courses/:course_id/group_categories \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.group.GroupCategory`
        """
        warnings.warn(
            "`list_group_categories` is being deprecated and will be removed in a future version."
            " Use `get_group_categories` instead",
            DeprecationWarning
        )

        return self.get_group_categories(**kwargs)

    def get_group_categories(self, **kwargs):
        """
        List group categories for a context.

        :calls: `GET /api/v1/courses/:course_id/group_categories \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.group.GroupCategory`
        """
        from canvasapi.group import GroupCategory

        return PaginatedList(
            GroupCategory,
            self._requester,
            'GET',
            'courses/{}/group_categories'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_file(self, file, **kwargs):
        """
        Return the standard attachment json object for a file.

        :calls: `GET /api/v1/courses/:course_id/files/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_show>`_

        :param file: The object or ID of the file to retrieve.
        :type file: :class:`canvasapi.file.File` or int

        :rtype: :class:`canvasapi.file.File`
        """
        from canvasapi.file import File

        file_id = obj_or_id(file, "file", (File,))

        response = self._requester.request(
            'GET',
            'courses/{}/files/{}'.format(self.id, file_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return File(self._requester, response.json())

    def get_discussion_topic(self, topic):
        """
        Return data on an individual discussion topic.

        :calls: `GET /api/v1/courses/:course_id/discussion_topics/:topic_id \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.show>`_

        :param topic: The object or ID of the discussion topic.
        :type topic: :class:`canvasapi.discussion_topic.DiscussionTopic` or int

        :rtype: :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        topic_id = obj_or_id(topic, "topic", (DiscussionTopic,))

        response = self._requester.request(
            'GET',
            'courses/{}/discussion_topics/{}'.format(self.id, topic_id)
        )

        response_json = response.json()
        response_json.update({'course_id': self.id})

        return DiscussionTopic(self._requester, response_json)

    def get_full_discussion_topic(self, topic):
        """
        Return a cached structure of the discussion topic.

        :calls: `GET /api/v1/courses/:course_id/discussion_topics/:topic_id/view \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.view>`_

        :param topic: The object or ID of the discussion topic.
        :type topic: :class:`canvasapi.discussion_topic.DiscussionTopic` or int

        :rtype: dict
        """
        topic_id = obj_or_id(topic, "topic", (DiscussionTopic,))

        response = self._requester.request(
            'GET',
            'courses/{}/discussion_topics/{}/view'.format(self.id, topic_id),
        )
        return response.json()

    def get_discussion_topics(self, **kwargs):
        """
        Returns the paginated list of discussion topics for this course or group.

        :calls: `GET /api/v1/courses/:course_id/discussion_topics \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        return PaginatedList(
            DiscussionTopic,
            self._requester,
            'GET',
            'courses/{}/discussion_topics'.format(self.id),
            {'course_id': self.id},
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_assignment_group(self, assignment_group, **kwargs):
        """
        Retrieve specified assignment group for the specified course.

        :calls: `GET /api/v1/courses/:course_id/assignment_groups/:assignment_group_id \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.show>`_

        :param assignment_group: object or ID of assignment group.
        :type assignment_group: :class:`canvasapi.assignment.AssignmentGroup` or int

        :rtype: :class:`canvasapi.assignment.AssignmentGroup`
        """
        from canvasapi.assignment import AssignmentGroup

        assignment_group_id = obj_or_id(assignment_group, "assignment_group", (AssignmentGroup,))

        response = self._requester.request(
            'GET',
            'courses/{}/assignment_groups/{}'.format(self.id, assignment_group_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update({'course_id': self.id})

        return AssignmentGroup(self._requester, response_json)

    def list_assignment_groups(self, **kwargs):
        """
        List assignment groups for the specified course.

        .. warning::
            .. deprecated:: 0.10.0
                Use :func:`canvasapi.course.Course.get_assignment_groups` instead.

        :calls: `GET /api/v1/courses/:course_id/assignment_groups \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.AssignmentGroup`
        """
        warnings.warn(
            "`list_assignment_groups` is being deprecated and will be removed "
            "in a future version. Use `get_assignment_groups` instead",
            DeprecationWarning
        )

        return self.get_assignment_groups(**kwargs)

    def get_assignment_groups(self, **kwargs):
        """
        List assignment groups for the specified course.

        :calls: `GET /api/v1/courses/:course_id/assignment_groups \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.AssignmentGroup`
        """
        from canvasapi.assignment import AssignmentGroup

        return PaginatedList(
            AssignmentGroup,
            self._requester,
            'GET',
            'courses/{}/assignment_groups'.format(self.id),
            {'course_id': self.id},
            _kwargs=combine_kwargs(**kwargs)
        )

    def create_discussion_topic(self, **kwargs):
        """
        Creates a new discussion topic for the course or group.

        :calls: `POST /api/v1/courses/:course_id/discussion_topics \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.create>`_

        :rtype: :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        response = self._requester.request(
            'POST',
            'courses/{}/discussion_topics'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        response_json = response.json()
        response_json.update({'course_id': self.id})

        return DiscussionTopic(self._requester, response_json)

    def reorder_pinned_topics(self, order):
        """
        Puts the pinned discussion topics in the specified order.
        All pinned topics should be included.

        :calls: `POST /api/v1/courses/:course_id/discussion_topics/reorder \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.reorder>`_

        :param order: The ids of the pinned discussion topics in the desired order.
            e.g. [104, 102, 103], (104, 102, 103), or "104,102,103"
        :type order: string or iterable sequence of values

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        # Convert iterable sequence to comma-separated string
        if is_multivalued(order):
            order = ",".join([text_type(topic_id) for topic_id in order])

        # Check if is a string with commas
        if not isinstance(order, text_type) or "," not in order:
            raise ValueError("Param `order` must be a list, tuple, or string.")

        response = self._requester.request(
            'POST',
            'courses/{}/discussion_topics/reorder'.format(self.id),
            order=order
        )

        return response.json().get('reorder')

    def create_assignment_group(self, **kwargs):
        """
        Create a new assignment group for this course.

        :calls: `POST /api/v1/courses/:course_id/assignment_groups \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.create>`_

        :rtype: :class:`canvasapi.assignment.AssignmentGroup`
        """
        from canvasapi.assignment import AssignmentGroup

        response = self._requester.request(
            'POST',
            'courses/{}/assignment_groups'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update({'course_id': self.id})

        return AssignmentGroup(self._requester, response_json)

    def create_external_tool(self, name, privacy_level, consumer_key, shared_secret, **kwargs):
        """
        Create an external tool in the current course.

        :calls: `POST /api/v1/courses/:course_id/external_tools \
        <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.create>`_

        :param name: The name of the tool
        :type name: str
        :param privacy_level: What information to send to the external
            tool. Options are "anonymous", "name_only", "public"
        :type privacy_level: str
        :param consumer_key: The consumer key for the external tool
        :type consumer_key: str
        :param shared_secret: The shared secret with the external tool
        :type shared_secret: str
        :rtype: :class:`canvasapi.external_tool.ExternalTool`
        """
        from canvasapi.external_tool import ExternalTool

        response = self._requester.request(
            'POST',
            'courses/{}/external_tools'.format(self.id),
            name=name,
            privacy_level=privacy_level,
            consumer_key=consumer_key,
            shared_secret=shared_secret,
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update({'course_id': self.id})

        return ExternalTool(self._requester, response_json)

    def get_course_level_participation_data(self):
        """
        Return page view hits and participation numbers grouped by day through the course's history

        :calls: `GET /api/v1/courses/:course_id/analytics/activity \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_participation>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'courses/{}/analytics/activity'.format(self.id)
        )

        return response.json()

    def get_course_level_assignment_data(self, **kwargs):
        """
        Return a list of assignments for the course sorted by due date

        :calls: `GET /api/v1/courses/:course_id/analytics/assignments \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_assignments>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'courses/{}/analytics/assignments'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        return response.json()

    def get_course_level_student_summary_data(self, **kwargs):
        """
        Return a summary of per-user access information for all students in a course

        :calls: `GET /api/v1/courses/:course_id/analytics/student_summaries \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_student_summaries>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'courses/{}/analytics/student_summaries'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        return response.json()

    def get_user_in_a_course_level_participation_data(self, user):
        """
        Return page view hits grouped by hour and participation details through course's history

        :calls: `GET /api/v1/courses/:course_id/analytics/users/:student_id/activity \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_participation>`_

        :param user: The object or ID of the related user
        :type user: :class:`canvasapi.user.User` or int

        :rtype: dict
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            'GET',
            'courses/{}/analytics/users/{}/activity'.format(self.id, user_id)
        )

        return response.json()

    def get_user_in_a_course_level_assignment_data(self, user):
        """
        Return a list of assignments for the course sorted by due date

        :calls: `GET /api/v1/courses/:course_id/analytics/users/:student_id/assignments \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_assignments>`_

        :param user: The object or ID of the related user
        :type user: :class:`canvasapi.user.User` or int

        :rtype: dict
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            'GET',
            'courses/{}/analytics/users/{}/assignments'.format(self.id, user_id)
        )

        return response.json()

    def get_user_in_a_course_level_messaging_data(self, user):
        """
        Return messaging hits grouped by day through the entire history of the course

        :calls: `GET /api/v1/courses/:course_id/analytics/users/:student_id/communication \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_messaging>`_

        :param user: The object or ID of the related user
        :type user: :class:`canvasapi.user.User` or int

        :rtype: dict
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            'GET',
            'courses/{}/analytics/users/{}/communication'.format(self.id, user_id)
        )

        return response.json()

    def submit_assignment(self, assignment, submission, **kwargs):
        """
        Makes a submission for an assignment.

        .. warning::
            .. deprecated:: 0.9.0
                Use :func:`canvasapi.assignment.Assignment.submit` instead.

        :calls: `POST /api/v1/courses/:course_id/assignments/:assignment_id/submissions \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions.create>`_

        :param assignment: The object or ID of the related assignment
        :type assignment: :class:`canvasapi.assignment.Assignment` or int

        :param submission: The attributes of the submission.
        :type submission: dict

        :rtype: :class:`canvasapi.submission.Submission`
        """
        from canvasapi.assignment import Assignment

        warnings.warn(
            'Course.submit_assignment() is deprecated and will be removed in '
            'the future. Use Assignment.submit() instead.',
            DeprecationWarning
        )

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))

        assignment = Assignment(
            self._requester,
            {'course_id': self.id, 'id': assignment_id}
        )

        return assignment.submit(submission, **kwargs)

    def list_submissions(self, assignment, **kwargs):
        """
        Get all existing submissions for an assignment.

        .. warning::
            .. deprecated:: 0.9.0
                Use :func:`canvasapi.assignment.Assignment.get_submissions` instead.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions  \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.index>`_

        :param assignment: The object or ID of the related assignment
        :type assignment: :class:`canvasapi.assignment.Assignment` or int

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.submission.Submission`
        """
        from canvasapi.assignment import Assignment

        warnings.warn(
            'Course.list_submissions() is deprecated and will be removed in '
            'the future. Use Assignment.get_submissions() instead.',
            DeprecationWarning
        )

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))

        assignment = Assignment(
            self._requester,
            {'course_id': self.id, 'id': assignment_id}
        )

        return assignment.get_submissions(**kwargs)

    def list_multiple_submissions(self, **kwargs):
        """
        List submissions for multiple assignments.
        Get all existing submissions for a given set of students and assignments.

        .. warning::
            .. deprecated:: 0.10.0
                Use :func:`canvasapi.course.Course.get_multiple_submissions` instead.

        :calls: `GET /api/v1/courses/:course_id/students/submissions \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.submission.Submission`
        """
        warnings.warn(
            "`list_multiple_submissions`"
            " is being deprecated and will be removed in a future version."
            " Use `get_multiple_submissions` instead",
            DeprecationWarning
        )

        return self.get_multiple_submissions(**kwargs)

    def get_multiple_submissions(self, **kwargs):
        """
        List submissions for multiple assignments.
        Get all existing submissions for a given set of students and assignments.

        :calls: `GET /api/v1/courses/:course_id/students/submissions \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.submission.Submission`
        """
        if 'grouped' in kwargs:
            warnings.warn('The `grouped` parameter must be empty. Removing kwarg `grouped`.')
            del kwargs['grouped']

        return PaginatedList(
            Submission,
            self._requester,
            'GET',
            'courses/{}/students/submissions'.format(self.id),
            {'course_id': self.id},
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_submission(self, assignment, user, **kwargs):
        """
        Get a single submission, based on user id.

        .. warning::
            .. deprecated:: 0.9.0
                Use :func:`canvasapi.assignment.Assignment.get_submission` instead.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.show>`_

        :param assignment: The object or ID of the related assignment
        :type assignment: :class:`canvasapi.assignment.Assignment` or int
        :param user: The object or ID of the related user
        :type user: :class:`canvasapi.user.User` or int

        :rtype: :class:`canvasapi.submission.Submission`
        """
        from canvasapi.assignment import Assignment

        warnings.warn(
            '`Course.get_submission()` is deprecated and will be removed in a '
            'future version. Use `Assignment.get_submission()` instead',
            DeprecationWarning
        )

        assignment_id = obj_or_id(assignment, 'assignment', (Assignment,))

        assignment = Assignment(
            self._requester,
            {'course_id': self.id, 'id': assignment_id}
        )

        return assignment.get_submission(user, **kwargs)

    def update_submission(self, assignment, user, **kwargs):
        """
        Comment on and/or update the grading for a student's assignment submission.

        .. warning::
            .. deprecated:: 0.9.0
                Use :func:`canvasapi.submission.Submission.edit` instead.

        :calls: `PUT /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.update>`_

        :param assignment: The object or ID of the related assignment
        :type assignment: :class:`canvasapi.assignment.Assignment` or int
        :param user: The object or ID of the related user
        :type user: :class:`canvasapi.user.User` or int

        :rtype: :class:`canvasapi.submission.Submission`
        """
        from canvasapi.assignment import Assignment
        from canvasapi.user import User

        warnings.warn(
            '`Course.update_submission()` is deprecated and will be removed in a '
            'future version. Use `Submission.edit()` instead',
            DeprecationWarning
        )

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))
        user_id = obj_or_id(user, "user", (User,))

        submission = Submission(self._requester, {
            'course_id': self.id,
            'assignment_id': assignment_id,
            'user_id': user_id,
        })

        return submission.edit(**kwargs)

    def list_gradeable_students(self, assignment, **kwargs):
        """
        List students eligible to submit the assignment.

        .. warning::
            .. deprecated:: 0.9.0
                Use :func:`canvasapi.assignment.Assignment.get_gradeable_students` instead.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/gradeable_students  \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.gradeable_students>`_

        :param assignment: The object or ID of the related assignment
        :type assignment: :class:`canvasapi.assignment.Assignment` or int

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.user.UserDisplay`
        """
        from canvasapi.assignment import Assignment

        warnings.warn(
            '`Course.list_gradeable_students()` is deprecated and will be '
            'removed in a future version. Use '
            '`Assignment.get_gradeable_students()` instead.',
            DeprecationWarning
        )

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))
        assignment = Assignment(
            self._requester,
            {'id': assignment_id, 'course_id': self.id}
        )

        return assignment.get_gradeable_students(**kwargs)

    def mark_submission_as_read(self, assignment, user, **kwargs):
        """
        Mark submission as read. No request fields are necessary.

        .. warning::
            .. deprecated:: 0.9.0
                Use :func:`canvasapi.submission.Submission.mark_read` instead.

        :calls: `PUT
            /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/read \
            <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_read>`_

        :param assignment: The object or ID of the related assignment
        :type assignment: :class:`canvasapi.assignment.Assignment` or int
        :param user: The object or ID of the related user
        :type user: :class:`canvasapi.user.User` or int

        :rtype: `bool`
        """
        from canvasapi.assignment import Assignment
        from canvasapi.user import User

        warnings.warn(
            '`Course.mark_submission_as_read()` is deprecated and will be '
            'removed in a future version. Use `Submission.mark_read()` instead.',
            DeprecationWarning
        )

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))
        user_id = obj_or_id(user, "user", (User,))

        submission = Submission(self._requester, {
            'course_id': self.id,
            'assignment_id': assignment_id,
            'user_id': user_id
        })
        return submission.mark_read(**kwargs)

    def mark_submission_as_unread(self, assignment, user, **kwargs):
        """
        Mark submission as unread. No request fields are necessary.

        .. warning::
            .. deprecated:: 0.9.0
                Use :func:`canvasapi.submission.Submission.mark_unread` instead.

        :calls: `DELETE
            /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/read \
            <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_unread>`_

        :param assignment: The object or ID of the related assignment
        :type assignment: :class:`canvasapi.assignment.Assignment` or int
        :param user: The object or ID of the related user
        :type user: :class:`canvasapi.user.User` or int

        :rtype: `bool`
        """
        from canvasapi.assignment import Assignment
        from canvasapi.user import User

        warnings.warn(
            '`Course.mark_submission_as_unread()` is deprecated and will be '
            'removed in a future version. Use `Submission.mark_unread()` instead.',
            DeprecationWarning
        )

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))
        user_id = obj_or_id(user, "user", (User,))

        submission = Submission(self._requester, {
            'course_id': self.id,
            'assignment_id': assignment_id,
            'user_id': user_id
        })
        return submission.mark_unread(**kwargs)

    def list_external_feeds(self, **kwargs):
        """
        Returns the list of External Feeds this course.

        .. warning::
            .. deprecated:: 0.10.0
                Use :func:`canvasapi.course.Course.get_external_feeds` instead.

        :calls: `GET /api/v1/courses/:course_id/external_feeds \
        <https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.external_feed.ExternalFeed`
        """
        warnings.warn(
            "`list_external_feeds` is being deprecated and will be removed in "
            "a future version. Use `get_external_feeds` instead",
            DeprecationWarning
        )

        return self.get_external_feeds(**kwargs)

    def get_external_feeds(self, **kwargs):
        """
        Returns the list of External Feeds this course.

        :calls: `GET /api/v1/courses/:course_id/external_feeds \
        <https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.external_feed.ExternalFeed`
        """
        from canvasapi.external_feed import ExternalFeed
        return PaginatedList(
            ExternalFeed,
            self._requester,
            'GET',
            'courses/{}/external_feeds'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def create_external_feed(self, url, **kwargs):
        """
        Create a new external feed for the course.

        :calls: `POST /api/v1/courses/:course_id/external_feeds \
        <https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.create>`_

        :param url: The url of the external rss or atom feed
        :type url: str
        :rtype: :class:`canvasapi.external_feed.ExternalFeed`
        """
        from canvasapi.external_feed import ExternalFeed
        response = self._requester.request(
            'POST',
            'courses/{}/external_feeds'.format(self.id),
            url=url,
            _kwargs=combine_kwargs(**kwargs)
        )
        return ExternalFeed(self._requester, response.json())

    def delete_external_feed(self, feed):
        """
        Deletes the external feed.

        :calls: `DELETE /api/v1/courses/:course_id/external_feeds/:external_feed_id \
        <https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.destroy>`_

        :param feed: The object or ID of the feed to be deleted.
        :type feed: :class:`canvasapi.external_feed.ExternalFeed` or int

        :rtype: :class:`canvasapi.external_feed.ExternalFeed`
        """
        from canvasapi.external_feed import ExternalFeed

        feed_id = obj_or_id(feed, "feed", (ExternalFeed,))

        response = self._requester.request(
            'DELETE',
            'courses/{}/external_feeds/{}'.format(self.id, feed_id)
        )
        return ExternalFeed(self._requester, response.json())

    def list_files(self, **kwargs):
        """
        Returns the paginated list of files for the course.

        .. warning::
            .. deprecated:: 0.10.0
                Use :func:`canvasapi.course.Course.get_files` instead.

        :calls: `GET /api/v1/courses/:course_id/files \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.file.File`
        """
        warnings.warn(
            "`list_files` is being deprecated and will be removed in a future "
            "version. Use `get_files` instead",
            DeprecationWarning
        )

        return self.get_files(**kwargs)

    def get_files(self, **kwargs):
        """
        Returns the paginated list of files for the course.

        :calls: `GET /api/v1/courses/:course_id/files \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.file.File`
        """
        from canvasapi.file import File

        return PaginatedList(
            File,
            self._requester,
            'GET',
            'courses/{}/files'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_folder(self, folder):
        """
        Returns the details for a course folder

        :calls: `GET /api/v1/courses/:course_id/folders/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.show>`_

        :param folder: The object or ID of the folder to retrieve.
        :type folder: :class:`canvasapi.folder.Folder` or int

        :rtype: :class:`canvasapi.folder.Folder`
        """
        folder_id = obj_or_id(folder, "folder", (Folder,))

        response = self._requester.request(
            'GET',
            'courses/{}/folders/{}'.format(self.id, folder_id)
        )
        return Folder(self._requester, response.json())

    def list_folders(self, **kwargs):
        """
        Returns the paginated list of all folders for the given course. This will be returned as a
        flat list containing all subfolders as well.

        .. warning::
            .. deprecated:: 0.10.0
                Use :func:`canvasapi.course.Course.get_folders` instead.

        :calls: `GET /api/v1/courses/:course_id/folders \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.list_all_folders>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.folder.Folder`
        """
        warnings.warn(
            "`list_folders` is being deprecated and will be removed in a "
            "future version. Use `get_folders` instead",
            DeprecationWarning
        )

        return self.get_folders(**kwargs)

    def get_folders(self, **kwargs):
        """
        Returns the paginated list of all folders for the given course. This will be returned as a
        flat list containing all subfolders as well.

        :calls: `GET /api/v1/courses/:course_id/folders \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.list_all_folders>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.folder.Folder`
        """
        return PaginatedList(
            Folder,
            self._requester,
            'GET',
            'courses/{}/folders'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def create_folder(self, name, **kwargs):
        """
        Creates a folder in this course.

        :calls: `POST /api/v1/courses/:course_id/folders \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.create>`_

        :param name: The name of the folder.
        :type name: str
        :rtype: :class:`canvasapi.folder.Folder`
        """
        response = self._requester.request(
            'POST',
            'courses/{}/folders'.format(self.id),
            name=name,
            _kwargs=combine_kwargs(**kwargs)
        )
        return Folder(self._requester, response.json())

    def list_tabs(self, **kwargs):
        """
        List available tabs for a course.
        Returns a list of navigation tabs available in the current context.

        .. warning::
            .. deprecated:: 0.10.0
                Use :func:`canvasapi.course.Course.get_tabs` instead.

        :calls: `GET /api/v1/courses/:course_id/tabs \
        <https://canvas.instructure.com/doc/api/tabs.html#method.tabs.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.tab.Tab`
        """
        warnings.warn(
            "`list_tabs` is being deprecated and will be removed in a future "
            "version. Use `get_tabs` instead",
            DeprecationWarning
        )

        return self.get_tabs(**kwargs)

    def get_tabs(self, **kwargs):
        """
        List available tabs for a course.
        Returns a list of navigation tabs available in the current context.

        :calls: `GET /api/v1/courses/:course_id/tabs \
        <https://canvas.instructure.com/doc/api/tabs.html#method.tabs.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.tab.Tab`
        """
        return PaginatedList(
            Tab,
            self._requester,
            'GET',
            'courses/{}/tabs'.format(self.id),
            {'course_id': self.id},
            _kwargs=combine_kwargs(**kwargs)
        )

    def update_tab(self, tab_id, **kwargs):
        """
        Update a tab for a course.

        .. warning::
            .. deprecated:: 0.10.0
                Use :func:`canvasapi.tab.Tab.update` instead.

        :calls: `PUT /api/v1/courses/:course_id/tabs/:tab_id \
        <https://canvas.instructure.com/doc/api/tabs.html#method.tabs.update>`_

        :param tab_id: The ID of the tab
        :type tab_id: str

        :rtype: :class:`canvasapi.tab.Tab`
        """
        warnings.warn(
            "`Course.update_tab()` is being deprecated and will be removed in "
            "a future version. Use `Tab.update()` instead",
            DeprecationWarning
        )

        tab = Tab(self._requester, {
            'course_id': self.id,
            'id': tab_id
        })
        return tab.update(**kwargs)

    def get_rubric(self, rubric_id, **kwargs):
        """
        Get a single rubric, based on rubric id.

        :calls: `GET /api/v1/courses/:course_id/rubrics/:id \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.show>`_

        :param rubric_id: The ID of the rubric.
        :type rubric_id: int
        :rtype: :class:`canvasapi.rubric.Rubric`
        """
        response = self._requester.request(
            'GET',
            'courses/%s/rubrics/%s' % (self.id, rubric_id),
            _kwargs=combine_kwargs(**kwargs)
        )

        return Rubric(self._requester, response.json())

    def list_rubrics(self, **kwargs):
        """
        Get the paginated list of active rubrics for the current course.

        .. warning::
            .. deprecated:: 0.10.0
                Use :func:`canvasapi.course.Course.get_rubrics` instead.

        :calls: `GET /api/v1/courses/:course_id/rubrics \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.rubric.Rubric`
        """
        warnings.warn(
            "`list_rubrics` is being deprecated and will be removed in a "
            "future version. Use `get_rubrics` instead",
            DeprecationWarning
        )

        return self.get_rubrics(**kwargs)

    def get_rubrics(self, **kwargs):
        """
        Get the paginated list of active rubrics for the current course.

        :calls: `GET /api/v1/courses/:course_id/rubrics \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.rubric.Rubric`
        """
        return PaginatedList(
            Rubric,
            self._requester,
            'GET',
            'courses/%s/rubrics' % (self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_root_outcome_group(self):
        """
        Redirect to root outcome group for context

        :calls: `GET /api/v1/courses/:course_id/root_outcome_group \
        <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.redirect>`_

        :returns: The OutcomeGroup of the context.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        from canvasapi.outcome import OutcomeGroup

        response = self._requester.request(
            'GET',
            'courses/{}/root_outcome_group'.format(self.id)
        )
        return OutcomeGroup(self._requester, response.json())

    def get_outcome_group(self, group):
        """
        Returns the details of the Outcome Group with the given id.

        :calls: `GET /api/v1/courses/:course_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show>`_

        :param group: The outcome group object or ID to return.
        :type group: :class:`canvasapi.outcome.OutcomeGroup` or int

        :returns: An outcome group object.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        from canvasapi.outcome import OutcomeGroup

        outcome_group_id = obj_or_id(group, "group", (OutcomeGroup,))

        response = self._requester.request(
            'GET',
            'courses/{}/outcome_groups/{}'.format(self.id, outcome_group_id)
        )

        return OutcomeGroup(self._requester, response.json())

    def get_outcome_groups_in_context(self):
        """
        Get all outcome groups for context - BETA

        :calls: `GET /api/v1/courses/:course_id/outcome_groups \
        <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.index>`_

        :returns: Paginated List of OutcomesGroups in the context.
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.outcome.OutcomeGroups`
        """
        from canvasapi.outcome import OutcomeGroup

        return PaginatedList(
            OutcomeGroup,
            self._requester,
            'GET',
            'courses/{}/outcome_groups'.format(self.id)
        )

    def get_all_outcome_links_in_context(self):
        """
        Get all outcome links for context - BETA

        :calls: `GET /api/v1/courses/:course_id/outcome_group_links \
        <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link_index>`_

        :returns: Paginated List of OutcomesLinks in the context.
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.outcome.OutcomeLink`
        """
        from canvasapi.outcome import OutcomeLink

        return PaginatedList(
            OutcomeLink,
            self._requester,
            'GET',
            'courses/{}/outcome_group_links'.format(self.id)
        )

    def get_outcome_results(self, **kwargs):
        """
        Get all outcome results for context - BETA

        :calls: `GET /api/v1/courses/:course_id/outcome_results \
        <https://canvas.instructure.com/doc/api/outcome_results.html#method.outcome_results.index>`_

        :returns: List of potential related outcome result dicts.
        :rtype: dict
        """
        response = self._requester.request(
            'GET',
            'courses/{}/outcome_results'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        return response.json()

    def get_outcome_result_rollups(self, **kwargs):
        """
        Get all outcome result rollups for context - BETA

        :calls: `GET /api/v1/courses/:course_id/outcome_rollups \
        <https://canvas.instructure.com/doc/api/outcome_results.html#method.outcome_results.rollups>`_

        :returns: List of outcome result rollups in the context.
        :rtype: dict
        """
        response = self._requester.request(
            'GET',
            'courses/{}/outcome_rollups'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        return response.json()

    def add_grading_standards(self, title, grading_scheme_entry, **kwargs):
        """
        Create a new grading standard for the course.

        :calls: `POST /api/v1/courses/:course_id/grading_standards \
        <https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.create>`_

        :param title: The title for the Grading Standard
        :type title: str
        :param grading_scheme: A list of dictionaries containing keys for "name" and "value"
        :type grading_scheme: list[dict]
        :rtype: :class:`canvasapi.grading_standards.GradingStandard`
        """
        if not isinstance(grading_scheme_entry, list) or len(grading_scheme_entry) <= 0:
            raise ValueError("Param `grading_scheme_entry` must be a non-empty list.")

        for entry in grading_scheme_entry:
            if not isinstance(entry, dict):
                raise ValueError("grading_scheme_entry must consist of dictionaries.")
            if "name" not in entry or "value" not in entry:
                raise ValueError("Dictionaries with keys 'name' and 'value' are required.")
        kwargs["grading_scheme_entry"] = grading_scheme_entry

        response = self._requester.request(
            'POST',
            'courses/%s/grading_standards' % (self.id),
            title=title,
            _kwargs=combine_kwargs(**kwargs)
        )
        return GradingStandard(self._requester, response.json())

    def get_grading_standards(self, **kwargs):
        """
        Get a PaginatedList of the grading standards available for the course

        :calls: `GET /api/v1/courses/:course_id/grading_standards \
        <https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.grading_standards.GradingStandard`
        """
        return PaginatedList(
            GradingStandard,
            self._requester,
            'GET',
            'courses/%s/grading_standards' % (self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_single_grading_standard(self, grading_standard_id, **kwargs):
        """
        Get a single grading standard from the course.

        :calls: `GET /api/v1/courses/:course_id/grading_standards/:grading_standard_id \
        <https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_show>`_

        :param grading_standard_id: The grading standard id
        :type grading_standard_id: int
        :rtype: :class:`canvasapi.grading_standards.GradingStandard`
        """

        response = self._requester.request(
            'GET',
            'courses/%s/grading_standards/%d' % (self.id, grading_standard_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return GradingStandard(self._requester, response.json())

    def create_content_migration(self, migration_type, **kwargs):
        """
        Create a content migration.

        :calls: `POST /api/v1/courses/:course_id/content_migrations \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.create>`_

        :param migration_type: The migrator type to use in this migration
        :type migration_type: str or :class:`canvasapi.content_migration.Migrator`

        :rtype: :class:`canvasapi.content_migration.ContentMigration`
        """
        from canvasapi.content_migration import ContentMigration, Migrator

        if isinstance(migration_type, Migrator):
            kwargs['migration_type'] = migration_type.type
        elif isinstance(migration_type, string_types):
            kwargs['migration_type'] = migration_type
        else:
            raise TypeError('Parameter migration_type must be of type Migrator or str')

        response = self._requester.request(
            'POST',
            'courses/{}/content_migrations'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        response_json = response.json()
        response_json.update({'course_id': self.id})

        return ContentMigration(self._requester, response_json)

    def get_content_migration(self, content_migration, **kwargs):
        """
        Retrive a content migration by its ID

        :calls: `GET /api/v1/courses/:course_id/content_migrations/:id \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.show>`_

        :param content_migration: The object or ID of the content migration to retrieve.
        :type content_migration: int, str or :class:`canvasapi.content_migration.ContentMigration`

        :rtype: :class:`canvasapi.content_migration.ContentMigration`
        """
        from canvasapi.content_migration import ContentMigration

        migration_id = obj_or_id(content_migration, "content_migration", (ContentMigration,))

        response = self._requester.request(
            'GET',
            'courses/{}/content_migrations/{}'.format(self.id, migration_id),
            _kwargs=combine_kwargs(**kwargs)
        )

        response_json = response.json()
        response_json.update({'course_id': self.id})

        return ContentMigration(self._requester, response_json)

    def get_content_migrations(self, **kwargs):
        """
        List content migrations that the current account can view or manage.

        :calls: `GET /api/v1/courses/:course_id/content_migrations/ \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.content_migration.ContentMigration`
        """
        from canvasapi.content_migration import ContentMigration

        return PaginatedList(
            ContentMigration,
            self._requester,
            'GET',
            'courses/{}/content_migrations'.format(self.id),
            {'course_id': self.id},
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_migration_systems(self, **kwargs):
        """
        Return a list of migration systems.

        :calls: `GET /api/v1/courses/:course_id/content_migrations/migrators \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.available_migrators>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.content_migration.Migrator`
        """
        from canvasapi.content_migration import Migrator

        return PaginatedList(
            Migrator,
            self._requester,
            'GET',
            'courses/{}/content_migrations/migrators'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def set_quiz_extensions(self, quiz_extensions, **kwargs):
        """
        Set extensions for student all quiz submissions in a course.

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/extensions
            <https://canvas.instructure.com/doc/api/quiz_extensions.html#method.quizzes/quiz_extensions.create>`_

        :param quiz_extensions: List of dictionaries representing extensions.
        :type quiz_extensions: list

        :rtype: list of :class:`canvasapi.quiz.QuizExtension`

        Example Usage:

        >>> course.set_quiz_extensions([
        ...     {
        ...         'user_id': 1,
        ...         'extra_time': 60,
        ...         'extra_attempts': 1
        ...     },
        ...     {
        ...         'user_id': 2,
        ...         'extra_attempts': 3
        ...     },
        ...     {
        ...         'user_id': 3,
        ...         'extra_time': 20
        ...     }
        ... ])
        """

        if not isinstance(quiz_extensions, list) or not quiz_extensions:
            raise ValueError('Param `quiz_extensions` must be a non-empty list.')

        if any(not isinstance(extension, dict) for extension in quiz_extensions):
            raise ValueError('Param `quiz_extensions` must only contain dictionaries')

        if any('user_id' not in extension for extension in quiz_extensions):
            raise RequiredFieldMissing(
                'Dictionaries in `quiz_extensions` must contain key `user_id`'
            )

        kwargs['quiz_extensions'] = quiz_extensions

        response = self._requester.request(
            'POST',
            'courses/{}/quiz_extensions'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        extension_list = response.json()['quiz_extensions']
        return [QuizExtension(self._requester, extension) for extension in extension_list]

    def submissions_bulk_update(self, **kwargs):
        """
        Update the grading and comments on multiple student's assignment
        submissions in an asynchronous job.

        :calls: `POST /api/v1/courses/:course_id/submissions/update_grades \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.bulk_update>`_

        :rtype: :class:`canvasapi.progress.Progress`
        """
        response = self._requester.request(
            'POST',
            'courses/{}/submissions/update_grades'.format(
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        return Progress(self._requester, response.json())

    def get_blueprint(self, template='default', **kwargs):
        """
        Return the blueprint of a given ID.

        :calls: `GET /api/v1/courses/:course_id/blueprint_templates/:template_id \
        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.show>`_

        :param template: The object or ID of the blueprint template to get.
        :type template: int or :class:`canvasapi.blueprint.BlueprintTemplate`

        :rtype: :class:`canvasapi.blueprint.BlueprintTemplate`
        """
        from canvasapi.blueprint import BlueprintTemplate

        if template == 'default':
            template_id = template
        else:
            template_id = obj_or_id(template, 'template', (BlueprintTemplate,))

        response = self._requester.request(
            'GET',
            'courses/{}/blueprint_templates/{}'.format(
                self.id,
                template_id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        return BlueprintTemplate(self._requester, response.json())

    def list_blueprint_subscriptions(self, **kwargs):
        """
        Return a list of blueprint subscriptions for the given course.

        :calls: `GET /api/v1/courses/:course_id/blueprint_subscriptions\
        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.\
        master_courses/master_templates.subscriptions_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.blueprint.BlueprintSubscription`
        """

        return PaginatedList(
            BlueprintSubscription,
            self._requester,
            'GET',
            'courses/{}/blueprint_subscriptions'.format(
                self.id
            ),
            {'course_id': self.id},
            kwargs=combine_kwargs(**kwargs)
        )

    def list_content_exports(self, **kwargs):
        """
        Return a paginated list of the past and pending content export jobs for a course.

        :calls: `GET /api/v1/courses/:course_id/content_exports\
        <https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.content_export.ContentExport`
        """
        from canvasapi.content_export import ContentExport

        return PaginatedList(
            ContentExport,
            self._requester,
            'GET',
            'courses/{}/content_exports'.format(
                self.id
            ),
            kwargs=combine_kwargs(**kwargs)
        )

    def show_content_export(self, export_id, **kwargs):
        """
        Return information about a single content export.

        :calls: `GET /api/v1/courses/:course_id/content_exports/:id\
        <https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.show>`_

        :rtype: :class:`canvasapi.content_export.ContentExport`
        """
        from canvasapi.content_export import ContentExport

        response = self._requester.request(
            'GET',
            'courses/{}/content_exports/{}'.format(
                self.id,
                export_id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        return ContentExport(self._requester, response.json())

    def export_content(self, export_type, **kwargs):
        """
        Begin a content export job for a course.

        :calls: `POST /api/v1/courses/:course_id/content_exports\
        <https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.create>`_

        :rtype: :class:`canvasapi.content_export.ContentExport`
        """
        from canvasapi.content_export import ContentExport

        kwargs['export_type'] = export_type

        response = self._requester.request(
            'POST',
            'courses/{}/content_exports'.format(
                self.id,
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        return ContentExport(self._requester, response.json())


@python_2_unicode_compatible
class CourseNickname(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.nickname, self.course_id)

    def remove(self):
        """
        Remove the nickname for the given course. Subsequent course API
        calls will return the actual name for the course.

        :calls: `DELETE /api/v1/users/self/course_nicknames/:course_id \
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.delete>`_

        :rtype: :class:`canvasapi.course.CourseNickname`
        """
        response = self._requester.request(
            'DELETE',
            'users/self/course_nicknames/{}'.format(self.course_id)
        )
        return CourseNickname(self._requester, response.json())
