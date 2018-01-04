from __future__ import absolute_import, division, print_function, unicode_literals
from warnings import warn

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.paginated_list import PaginatedList
from canvasapi.submission import Submission
from canvasapi.util import combine_kwargs, obj_or_id


@python_2_unicode_compatible
class Section(CanvasObject):

    def __str__(self):
        return '{} - {} ({})'.format(
            self.name,
            self.course_id,
            self.id,
        )

    def get_enrollments(self, **kwargs):
        """
        List all of the enrollments for the current user.

        :calls: `GET /api/v1/sections/:section_id/enrollments \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.enrollment.Enrollment`
        """
        from canvasapi.enrollment import Enrollment

        return PaginatedList(
            Enrollment,
            self._requester,
            'GET',
            'sections/{}/enrollments'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def cross_list_section(self, new_course):
        """
        Move the Section to another course.

        :calls: `POST /api/v1/sections/:id/crosslist/:new_course_id \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.crosslist>`_

        :param new_course: The object or ID of the new course.
        :type new_course: :class:`canvasapi.course.Course` or int

        :rtype: :class:`canvasapi.section.Section`
        """
        from canvasapi.course import Course

        new_course_id = obj_or_id(new_course, "new_course", (Course,))

        response = self._requester.request(
            'POST',
            'sections/{}/crosslist/{}'.format(self.id, new_course_id)
        )
        return Section(self._requester, response.json())

    def decross_list_section(self):
        """
        Undo cross-listing of a section.

        :calls: `DELETE /api/v1/sections/:id/crosslist \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.uncrosslist>`_

        :rtype: :class:`canvasapi.section.Section`
        """
        response = self._requester.request(
            'DELETE',
            'sections/{}/crosslist'.format(self.id)
        )
        return Section(self._requester, response.json())

    def edit(self):
        """
        Edit contents of a target section.

        :calls: `PUT /api/v1/sections/:id \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.update>`_

        :rtype: :class:`canvasapi.section.Section`
        """
        response = self._requester.request(
            'PUT',
            'sections/{}'.format(self.id)
        )
        return Section(self._requester, response.json())

    def delete(self):
        """
        Delete a target section.

        :calls: `DELETE /api/v1/sections/:id \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.destroy>`_

        :rtype: :class:`canvasapi.section.Section`
        """
        response = self._requester.request(
            'DELETE',
            'sections/{}'.format(self.id)
        )
        return Section(self._requester, response.json())

    def submit_assignment(self, assignment, submission, **kwargs):
        """
        Makes a submission for an assignment.

        :calls: `POST /api/v1/sections/:section_id/assignments/:assignment_id/submissions \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions.create>`_

        :param assignment: The object or ID of the assignment.
        :type assignment: :class:`canvasapi.assignment.Assignment` or int
        :param submission: The attributes of the submission.
        :type submission: dict

        :rtype: :class:`canvasapi.submission.Submission`
        """
        from canvasapi.assignment import Assignment

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))

        if isinstance(submission, dict) and 'submission_type' in submission:
            kwargs['submision'] = submission
        else:
            raise RequiredFieldMissing(
                "Dictionary with key 'submission_type' is required."
            )

        response = self._requester.request(
            'POST',
            'sections/{}/assignments/{}/submissions'.format(self.id, assignment_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update(section_id=self.id)

        return Submission(self._requester, response_json)

    def list_submissions(self, assignment, **kwargs):
        """
        Get all existing submissions for an assignment.

        :calls: `GET /api/v1/sections/:section_id/assignments/:assignment_id/submissions  \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.index>`_

        :param assignment: The object or ID of the assignment.
        :type assignment: :class:`canvasapi.assignment.Assignment` or int

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.submission.Submission`
        """
        from canvasapi.assignment import Assignment

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))

        return PaginatedList(
            Submission,
            self._requester,
            'GET',
            'sections/{}/assignments/{}/submissions'.format(self.id, assignment_id),
            {'section_id': self.id},
            _kwargs=combine_kwargs(**kwargs)
        )

    def list_multiple_submissions(self, **kwargs):
        """
        List submissions for multiple assignments.
        Get all existing submissions for a given set of students and assignments.

        :calls: `GET /api/v1/sections/:section_id/students/submissions \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.submission.Submission`
        """
        if 'grouped' in kwargs:
            warn('The `grouped` parameter must be empty. Removing kwarg `grouped`.')
            del kwargs['grouped']

        return PaginatedList(
            Submission,
            self._requester,
            'GET',
            'sections/{}/students/submissions'.format(self.id),
            {'section_id': self.id},
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_submission(self, assignment, user, **kwargs):
        """
        Get a single submission, based on user id.

        :calls: `GET /api/v1/sections/:section_id/assignments/:assignment_id/submissions/:user_id \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.show>`_

        :param assignment: The object or ID of the assignment.
        :type assignment: :class:`canvasapi.assignment.Assignment` or int
        :param user: The object or ID of the user.
        :type user: :class:`canvasapi.user.User` or int or str

        :rtype: :class:`canvasapi.submission.Submission`
        """
        from canvasapi.assignment import Assignment
        from canvasapi.user import User

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))
        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            'GET',
            'sections/{}/assignments/{}/submissions/{}'.format(self.id, assignment_id, user_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update(section_id=self.id)

        return Submission(self._requester, response_json)

    def update_submission(self, assignment, user, **kwargs):
        """
        Comment on and/or update the grading for a student's assignment submission.

        :calls: `PUT /api/v1/sections/:section_id/assignments/:assignment_id/submissions/:user_id \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.update>`_

        :param assignment: The object or ID of the assignment.
        :type assignment: :class:`canvasapi.assignment.Assignment` or int
        :param user: The object or ID of the user.
        :type user: :class:`canvasapi.user.User` or int or str

        :rtype: :class:`canvasapi.submission.Submission`
        """
        from canvasapi.assignment import Assignment
        from canvasapi.user import User

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))
        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            'PUT',
            'sections/{}/assignments/{}/submissions/{}'.format(self.id, assignment_id, user_id),
            _kwargs=combine_kwargs(**kwargs)
        )

        submission = self.get_submission(assignment_id, user_id)

        response_json = response.json()
        response_json.update(section_id=self.id)

        if 'submission_type' in response_json:
            super(Submission, submission).set_attributes(response_json)

        return Submission(self._requester, response_json)

    def mark_submission_as_read(self, assignment, user):
        """
        Mark submission as read. No request fields are necessary.

        :calls: `PUT
            /api/v1/sections/:section_id/assignments/:assignment_id/submissions/:user_id/read \
            <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_read>`_

        :param assignment: The object or ID of the assignment.
        :type assignment: :class:`canvasapi.assignment.Assignment` or int
        :param user: The object or ID of the user.
        :type user: :class:`canvasapi.user.User` or int or str

        :rtype: `bool`
        """
        from canvasapi.assignment import Assignment
        from canvasapi.user import User

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))
        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            'PUT',
            'sections/{}/assignments/{}/submissions/{}/read'.format(
                self.id,
                assignment_id,
                user_id,
            )
        )
        return response.status_code == 204

    def mark_submission_as_unread(self, assignment, user):
        """
        Mark submission as unread. No request fields are necessary.

        :calls: `DELETE
            /api/v1/sections/:section_id/assignments/:assignment_id/submissions/:user_id/read \
            <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_unread>`_

        :param assignment: The object or ID of the assignment.
        :type assignment: :class:`canvasapi.assignment.Assignment` or int
        :param user: The object or ID of the user.
        :type user: :class:`canvasapi.user.User` or int or str

        :rtype: `bool`
        """
        from canvasapi.assignment import Assignment
        from canvasapi.user import User

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))
        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            'DELETE',
            'sections/{}/assignments/{}/submissions/{}/read'.format(
                self.id,
                assignment_id,
                user_id,
            ),
        )
        return response.status_code == 204
