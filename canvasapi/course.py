from canvasapi.canvas_object import CanvasObject
from canvasapi.discussion_topic import DiscussionTopic
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.folder import Folder
from canvasapi.page import Page
from canvasapi.paginated_list import PaginatedList
from canvasapi.tab import Tab
from canvasapi.submission import Submission
from canvasapi.upload import Uploader
from canvasapi.user import UserDisplay
from canvasapi.util import combine_kwargs


class Course(CanvasObject):

    def __str__(self):
        return "{} {} ({})".format(self.course_code, self.name, self.id)

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
        :rtype: :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

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

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

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
        :type user: :class:`canvasapi.user.User`
        :param enrollment_type: The type of enrollment.
        :type enrollment_type: str
        :rtype: :class:`canvasapi.enrollment.Enrollment`
        """
        from canvasapi.enrollment import Enrollment

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

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

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

    def upload(self, file, **kwargs):
        """
        Upload a file to this course.

        :calls: `POST /api/v1/courses/:course_id/files \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.create_file>`_

        :param path: The path of the file to upload.
        :type path: str
        :param file: The file or path of the file to upload.
        :type file: file or str
        :returns: True if the file uploaded successfully, False otherwise, \
                    and the JSON response from the API.
        :rtype: tuple
        """
        return Uploader(
            self._requester,
            'courses/%s/files' % (self.id),
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
            'courses/%s/reset_content' % (self.id),
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
            'courses/%s/enrollments' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def get_assignment(self, assignment_id, **kwargs):
        """
        Return the assignment with the given ID.

        :calls: `GET /api/v1/courses/:course_id/assignments/:id \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.show>`_

        :param assignment_id: The ID of the assignment to retrieve.
        :type assignment_id: int
        :rtype: :class:`canvasapi.assignment.Assignment`
        """
        from canvasapi.assignment import Assignment

        response = self._requester.request(
            'GET',
            'courses/%s/assignments/%s' % (self.id, assignment_id),
            **combine_kwargs(**kwargs)
        )
        return Assignment(self._requester, response.json())

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
            'courses/%s/assignments' % (self.id),
            **combine_kwargs(**kwargs)
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
            'courses/%s/assignments' % (self.id),
            **combine_kwargs(**kwargs)
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
        :rtype: :class:`canvasapi.quiz.Quiz`
        """
        from canvasapi.quiz import Quiz
        response = self._requester.request(
            'GET',
            'courses/%s/quizzes/%s' % (self.id, quiz_id)
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

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.module.Module`
        """
        from canvasapi.module import Module

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
        :rtype: :class:`canvasapi.module.Module`
        """
        from canvasapi.module import Module

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
        :rtype: :class:`canvasapi.module.Module`
        """
        from canvasapi.module import Module

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

    def get_external_tool(self, tool_id):
        """
        :calls: `GET /api/v1/courses/:course_id/external_tools/:external_tool_id \
        <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.show>`_

        :rtype: :class:`canvasapi.external_tool.ExternalTool`
        """
        from canvasapi.external_tool import ExternalTool

        response = self._requester.request(
            'GET',
            'courses/%s/external_tools/%s' % (self.id, tool_id),
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
            'courses/%s/external_tools' % (self.id),
            {'course_id': self.id},
            **combine_kwargs(**kwargs)
        )

    def get_section(self, section_id):
        """
        Retrieve a section.

        :calls: `GET /api/v1/courses/:course_id/sections/:id \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.index>`_

        :param section_id: The ID of the section to retrieve.
        :type section_id: int
        :rtype: :class:`canvasapi.section.Section`
        """
        from canvasapi.section import Section

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

        :rtype: :class:`canvasapi.course.Course`
        """
        response = self._requester.request(
            'GET',
            'courses/%s/front_page' % (self.id)
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
            'courses/%s/front_page' % (self.id),
            **combine_kwargs(**kwargs)
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
            'courses/%s/pages' % (self.id),
            {'course_id': self.id}
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
            'courses/%s/pages' % (self.id),
            **combine_kwargs(**kwargs)
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
            'courses/%s/pages/%s' % (self.id, url)
        )
        page_json = response.json()
        page_json.update({'course_id': self.id})

        return Page(self._requester, page_json)

    def list_sections(self, **kwargs):
        """
        Returns the list of sections for this course.

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
            'courses/%s/sections' % (self.id),
            **combine_kwargs(**kwargs)
        )

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
            'courses/%s/sections' % (self.id),
            **combine_kwargs(**kwargs)
        )

        return Section(self._requester, response.json())

    def list_groups(self, **kwargs):
        """
        Return list of active groups for the specified course.

        :calls: `GET /api/v1/courses/:course_id/groups \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.context_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.Course`
        """
        from group import Group
        return PaginatedList(
            Group,
            self._requester,
            'GET',
            'courses/%s/groups' % (self.id),
            **combine_kwargs(**kwargs)
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
            'courses/%s/group_categories' % (self.id),
            name=name,
            **combine_kwargs(**kwargs)
        )
        return GroupCategory(self._requester, response.json())

    def list_group_categories(self):
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
            'courses/%s/group_categories' % (self.id)
        )

    def get_discussion_topic(self, topic_id):
        """
        Return data on an individual discussion topic.

        :calls: `GET /api/v1/courses/:course_id/discussion_topics/:topic_id \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.show>`_

        :param topic_id: The ID of the discussion topic.
        :type topic_id: int

        :rtype: :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        response = self._requester.request(
            'GET',
            'courses/%s/discussion_topics/%s' % (self.id, topic_id)
        )

        response_json = response.json()
        response_json.update({'course_id': self.id})

        return DiscussionTopic(self._requester, response_json)

    def get_full_discussion_topic(self, topic_id):
        """
        Return a cached structure of the discussion topic.

        :calls: `GET /api/v1/courses/:course_id/discussion_topics/:topic_id/view \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.view>`_

        :param topic_id: The ID of the discussion topic.
        :type topic_id: int

        :rtype: :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        response = self._requester.request(
            'GET',
            'courses/%s/discussion_topics/%s/view' % (self.id, topic_id),
        )

        response_json = response.json()
        response_json.update({'course_id': self.id})

        return DiscussionTopic(self._requester, response_json)

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
            'courses/%s/discussion_topics' % (self.id),
            {'course_id': self.id},
            **combine_kwargs(**kwargs)
        )

    def get_assignment_group(self, assignment_group_id, **kwargs):
        """
        Retrieve specified assignment group for the specified course.

        :calls: `GET /api/v1/courses/:course_id/assignment_groups/:assignment_group_id \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.show>`_

        :param assignment_group_id: ID of assignment group.
        :type assignment_group_id: int
        :rtype: :class:`canvasapi.assignment.AssignmentGroup`
        """
        from canvasapi.assignment import AssignmentGroup

        response = self._requester.request(
            'GET',
            'courses/%s/assignment_groups/%s' % (self.id, assignment_group_id),
            **combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update({'course_id': self.id})

        return AssignmentGroup(self._requester, response_json)

    def list_assignment_groups(self, **kwargs):
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
            'courses/%s/assignment_groups' % (self.id),
            {'course_id': self.id},
            **combine_kwargs(**kwargs)
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
            'courses/%s/discussion_topics' % (self.id),
            **combine_kwargs(**kwargs)
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
            e.g. [104, 102, 103]
        :type order: list

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.discussion_topic.DiscussionTopic`
        """

        if not isinstance(order, list):
            raise ValueError("Param order needs to be string or a list.")

        response = self._requester.request(
            'POST',
            'courses/%s/discussion_topics/reorder' % (self.id),
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
            'courses/%s/assignment_groups' % (self.id),
            **combine_kwargs(**kwargs)
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
            'courses/%s/external_tools' % (self.id),
            **combine_kwargs(**kwargs)
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
            'courses/%s/analytics/activity' % (self.id)
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
            'courses/%s/analytics/assignments' % (self.id),
            **combine_kwargs(**kwargs)
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
            'courses/%s/analytics/student_summaries' % (self.id),
            **combine_kwargs(**kwargs)
        )

        return response.json()

    def get_user_in_a_course_level_participation_data(self, student_id):
        """
        Return page view hits grouped by hour and participation details through course's history

        :calls: `GET /api/v1/courses/:course_id/analytics/users/:student_id/activity \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_participation>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'courses/%s/analytics/users/%s/activity' % (self.id, student_id)
        )

        return response.json()

    def get_user_in_a_course_level_assignment_data(self, student_id):
        """
        Return a list of assignments for the course sorted by due date

        :calls: `GET /api/v1/courses/:course_id/analytics/users/:student_id/assignments \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_assignments>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'courses/%s/analytics/users/%s/assignments' % (self.id, student_id)
        )

        return response.json()

    def get_user_in_a_course_level_messaging_data(self, student_id):
        """
        Return messaging hits grouped by day through the entire history of the course

        :calls: `GET /api/v1/courses/:course_id/analytics/users/:student_id/communication \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_messaging>`_

        :rtype: dict
        """

        response = self._requester.request(
            'GET',
            'courses/%s/analytics/users/%s/communication' % (self.id, student_id)
        )

        return response.json()

    def submit_assignment(self, assignment_id, submission, **kwargs):
        """
        Makes a submission for an assignment.

        :calls: `POST /api/v1/courses/:course_id/assignments/:assignment_id/submissions \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions.create>`_

        :param submission: The attributes of the submission.
        :type submission: `dict`
        :rtype: :class:`canvasapi.submission.Submission`
        """
        if isinstance(submission, dict) and 'submission_type' in submission:
            kwargs['submision'] = submission
        else:
            raise RequiredFieldMissing(
                "Dictionary with key 'submission_type' is required."
            )

        response = self._requester.request(
            'POST',
            'courses/%s/assignments/%s/submissions' % (self.id, assignment_id),
            **combine_kwargs(**kwargs)
        )

        return Submission(self._requester, response.json())

    def list_submissions(self, assignment_id, **kwargs):
        """
        Makes a submission for an assignment.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions  \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.index>`_

        :param assignment_id: The ID of the assignment.
        :type assignment_id: `int`
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.submission.Submission`
        """
        return PaginatedList(
            Submission,
            self._requester,
            'GET',
            'courses/%s/assignments/%s/submissions' % (self.id, assignment_id),
            **combine_kwargs(**kwargs)
        )

    def list_multiple_submissions(self, **kwargs):
        """
        List submissions for multiple assignments.
        Get all existing submissions for a given set of students and assignments.

        :calls: `GET /api/v1/courses/:course_id/students/submissions \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.submission.Submission`
        """
        return PaginatedList(
            Submission,
            self._requester,
            'GET',
            'courses/%s/students/submissions' % (self.id),
            grouped=False,
            **combine_kwargs(**kwargs)
        )

    def get_submission(self, assignment_id, user_id, **kwargs):
        """
        Get a single submission, based on user id.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.show>`_

        :param assignment_id: The ID of the assignment.
        :type assignment_id: int
        :param user_id: The ID of the user.
        :type user_id: str
        :rtype: :class:`canvasapi.submission.Submission`
        """
        response = self._requester.request(
            'GET',
            'courses/%s/assignments/%s/submissions/%s' % (self.id, assignment_id, user_id),
            **combine_kwargs(**kwargs)
        )
        return Submission(self._requester, response.json())

    def update_submission(self, assignment_id, user_id, **kwargs):
        """
        Comment on and/or update the grading for a student's assignment submission.

        :calls: `PUT /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.update>`_

        :param assignment_id: The ID of the assignment.
        :type assignment_id: int
        :param user_id: The ID of the user.
        :type user_id: str
        :rtype: :class:`canvasapi.submission.Submission`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/assignments/%s/submissions/%s' % (self.id, assignment_id, user_id),
            **combine_kwargs(**kwargs)
        )

        submission = self.get_submission(assignment_id, user_id)

        if 'submission_type' in response.json():
            super(Submission, submission).set_attributes(response.json())

        return Submission(self._requester, response.json())

    def list_gradeable_students(self, assignment_id):
        """
        List students eligible to submit the assignment.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/gradeable_students  \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.gradeable_students>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.user.User`
        """
        return PaginatedList(
            UserDisplay,
            self._requester,
            'GET',
            'courses/%s/assignments/%s/gradeable_students' % (self.id, assignment_id)
        )

    def mark_submission_as_read(self, assignment_id, user_id):
        """
        Mark submission as read. No request fields are necessary.

        :calls: `PUT
            /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/read \
            <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_read>`_

        :rtype: `bool`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/assignments/%s/submissions/%s/read' % (
                self.id,
                assignment_id,
                user_id,
            )
        )
        return response.status_code == 204

    def mark_submission_as_unread(self, assignment_id, user_id):
        """
        Mark submission as unread. No request fields are necessary.

        :calls: `DELETE
            /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/read \
            <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_unread>`_

        :rtype: `bool`
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s/assignments/%s/submissions/%s/read' % (
                self.id,
                assignment_id,
                user_id,
            ),
        )
        return response.status_code == 204

    def list_external_feeds(self):
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
            'courses/%s/external_feeds' % (self.id)
        )

    def create_external_feed(self, url, **kwargs):
        """
        Create a new external feed for the course.

        :calls: `POST /api/v1/courses/:course_id/external_feeds \
        <https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.create>`_

        :param url: The urlof the external rss or atom feed
        :type url: str
        :rtype: :class:`canvasapi.external_feed.ExternalFeed`
        """
        from canvasapi.external_feed import ExternalFeed
        response = self._requester.request(
            'POST',
            'courses/%s/external_feeds' % self.id,
            url=url,
            **combine_kwargs(**kwargs)
        )
        return ExternalFeed(self._requester, response.json())

    def delete_external_feed(self, feed_id):
        """
        Deletes the external feed.

        :calls: `DELETE /api/v1/courses/:course_id/external_feeds/:external_feed_id \
        <https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.destroy>`_

        :param feed_id: The id of the feed to be deleted.
        :type feed_id: int
        :rtype: :class:`canvasapi.external_feed.ExternalFeed`
        """
        from canvasapi.external_feed import ExternalFeed
        response = self._requester.request(
            'DELETE',
            'courses/%s/external_feeds/%s' % (self.id, feed_id)
        )
        return ExternalFeed(self._requester, response.json())

    def list_files(self, **kwargs):
        """
        Returns the paginated list of files for the course.

        :calls: `GET api/v1/courses/:course_id/files \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.file.File`
        """
        from canvasapi.file import File

        return PaginatedList(
            File,
            self._requester,
            'GET',
            'courses/%s/files' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def get_folder(self, folder_id):
        """
        Returns the details for a course folder

        :calls: `GET /api/v1/courses/:course_id/folders/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.show>`_

        :param folder_id: The ID of the folder to retrieve.
        :type folder_id: int
        :rtype: :class:`canvasapi.folder.Folder`
        """
        response = self._requester.request(
            'GET',
            'courses/%s/folders/%s' % (self.id, folder_id)
        )
        return Folder(self._requester, response.json())

    def list_folders(self):
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
            'courses/%s/folders' % (self.id)
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
            'courses/%s/folders' % self.id,
            name=name,
            **combine_kwargs(**kwargs)
        )
        return Folder(self._requester, response.json())

    def list_tabs(self, **kwargs):
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
            'courses/%s/tabs' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def update_tab(self, tab_id, **kwargs):
        """
        Update a tab for a course.

        :calls: `PUT /api/v1/courses/:course_id/tabs/:tab_id \
        <https://canvas.instructure.com/doc/api/tabs.html#method.tabs.update>`_

        :rtype: :class:`canvasapi.tab.Tab`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/tabs/%s' % (self.id, tab_id),
            **combine_kwargs(**kwargs)
        )

        return Tab(self._requester, response.json())


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
            'users/self/course_nicknames/%s' % (self.course_id)
        )
        return CourseNickname(self._requester, response.json())
