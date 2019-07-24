from __future__ import absolute_import, division, print_function, unicode_literals
import warnings

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.progress import Progress
from canvasapi.submission import GroupedSubmission, Submission
from canvasapi.util import combine_kwargs, obj_or_id, normalize_bool


@python_2_unicode_compatible
class Section(CanvasObject):
    def __str__(self):
        return "{} - {} ({})".format(self.name, self.course_id, self.id)

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
            "POST", "sections/{}/crosslist/{}".format(self.id, new_course_id)
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
            "DELETE", "sections/{}/crosslist".format(self.id)
        )
        return Section(self._requester, response.json())

    def delete(self):
        """
        Delete a target section.

        :calls: `DELETE /api/v1/sections/:id \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.destroy>`_

        :rtype: :class:`canvasapi.section.Section`
        """
        response = self._requester.request("DELETE", "sections/{}".format(self.id))
        return Section(self._requester, response.json())

    def edit(self, **kwargs):
        """
        Edit contents of a target section.

        :calls: `PUT /api/v1/sections/:id \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.update>`_

        :rtype: :class:`canvasapi.section.Section`
        """
        response = self._requester.request(
            "PUT", "sections/{}".format(self.id), _kwargs=combine_kwargs(**kwargs)
        )

        if "name" in response.json():
            super(Section, self).set_attributes(response.json())

        return self

    def get_assignment_override(self, assignment, **kwargs):
        """
        Return override for the specified assignment for this section.

        :param assignment: The assignment to get an override for
        :type assignment: :class:`canvasapi.assignment.Assignment` or int

        :calls: `GET /api/v1/sections/:course_section_id/assignments/:assignment_id/override \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.section_alias>`_

        :rtype: :class:`canvasapi.assignment.AssignmentOverride`
        """
        from canvasapi.assignment import Assignment, AssignmentOverride

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))

        response = self._requester.request(
            "GET", "sections/{}/assignments/{}/override".format(self.id, assignment_id)
        )
        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return AssignmentOverride(self._requester, response_json)

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
            "GET",
            "sections/{}/enrollments".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_multiple_submissions(self, **kwargs):
        """
        List submissions for multiple assignments.
        Get all existing submissions for a given set of students and assignments.

        :calls: `GET /api/v1/sections/:section_id/students/submissions \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.submission.Submission`
        """
        is_grouped = kwargs.get("grouped", False)

        if normalize_bool(is_grouped, "grouped"):
            cls = GroupedSubmission
        else:
            cls = Submission

        return PaginatedList(
            cls,
            self._requester,
            "GET",
            "sections/{}/students/submissions".format(self.id),
            {"section_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_submission(self, assignment, user, **kwargs):
        """
        Get a single submission, based on user id.

        .. warning::
            .. deprecated:: 0.9.0
                Use :func:`canvasapi.assignment.Assignment.get_submission` instead.

        :calls: `GET /api/v1/sections/:section_id/assignments/:assignment_id/submissions/:user_id \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.show>`_

        :param assignment: The object or ID of the assignment.
        :type assignment: :class:`canvasapi.assignment.Assignment` or int
        :param user: The object or ID of the user.
        :type user: :class:`canvasapi.user.User` or int or str

        :rtype: :class:`canvasapi.submission.Submission`
        """
        from canvasapi.assignment import Assignment

        warnings.warn(
            "Section.get_submission() is deprecated and will be removed "
            "in the future. Use Assignment.get_submission() instead.",
            DeprecationWarning,
        )

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))

        assignment = Assignment(
            self._requester,
            {"course_id": self.course_id, "section_id": self.id, "id": assignment_id},
        )

        return assignment.get_submission(user, **kwargs)

    def list_multiple_submissions(self, **kwargs):
        """
        List submissions for multiple assignments.
        Get all existing submissions for a given set of students and assignments.

        .. warning::
            .. deprecated:: 0.10.0
                Use :func:`canvasapi.section.Section.get_multiple_submissions` instead.

        :calls: `GET /api/v1/sections/:section_id/students/submissions \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.submission.Submission`
        """
        warnings.warn(
            "`list_multiple_submissions`"
            " is being deprecated and will be removed in a future version."
            " Use `get_multiple_submissions` instead",
            DeprecationWarning,
        )

        return self.get_multiple_submissions(**kwargs)

    def list_submissions(self, assignment, **kwargs):
        """
        Get all existing submissions for an assignment.

        .. warning::
            .. deprecated:: 0.9.0
                Use :func:`canvasapi.assignment.Assignment.get_submissions` instead.

        :calls: `GET /api/v1/sections/:section_id/assignments/:assignment_id/submissions  \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.index>`_

        :param assignment: The object or ID of the assignment.
        :type assignment: :class:`canvasapi.assignment.Assignment` or int

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.submission.Submission`
        """
        from canvasapi.assignment import Assignment

        warnings.warn(
            "Section.list_submissions() is deprecated and will be removed "
            "in the future. Use Assignment.get_submissions() instead.",
            DeprecationWarning,
        )

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))
        assignment = Assignment(
            self._requester,
            {"course_id": self.course_id, "section_id": self.id, "id": assignment_id},
        )

        return assignment.get_submissions(**kwargs)

    def mark_submission_as_read(self, assignment, user, **kwargs):
        """
        Mark submission as read. No request fields are necessary.

        .. warning::
            .. deprecated:: 0.9.0
                Use :func:`canvasapi.submission.Submission.mark_read` instead.

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

        warnings.warn(
            "Section.mark_submission_as_read() is deprecated and will be "
            "removed in the future. Use Submission.mark_read() instead.",
            DeprecationWarning,
        )

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))
        user_id = obj_or_id(user, "user", (User,))

        submission = Submission(
            self._requester,
            {
                "course_id": self.course_id,
                "assignment_id": assignment_id,
                "user_id": user_id,
            },
        )
        return submission.mark_read(**kwargs)

    def mark_submission_as_unread(self, assignment, user, **kwargs):
        """
        Mark submission as unread. No request fields are necessary.

        .. warning::
            .. deprecated:: 0.9.0
                Use :func:`canvasapi.submission.Submission.mark_unread` instead.

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

        warnings.warn(
            "Section.mark_submission_as_unread() is deprecated and will be "
            "removed in the future. Use Submission.mark_unread() instead.",
            DeprecationWarning,
        )

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))
        user_id = obj_or_id(user, "user", (User,))

        submission = Submission(
            self._requester,
            {
                "course_id": self.course_id,
                "assignment_id": assignment_id,
                "user_id": user_id,
            },
        )
        return submission.mark_unread(**kwargs)

    def submissions_bulk_update(self, **kwargs):
        """
        Update the grading and comments on multiple student's assignment
        submissions in an asynchronous job.

        :calls: `POST /api/v1/sections/:section_id/submissions/update_grades \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.bulk_update>`_

        :rtype: :class:`canvasapi.progress.Progress`
        """
        response = self._requester.request(
            "POST",
            "sections/{}/submissions/update_grades".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Progress(self._requester, response.json())

    def submit_assignment(self, assignment, submission, **kwargs):
        """
        Makes a submission for an assignment.

        .. warning::
            .. deprecated:: 0.9.0
                Use :func:`canvasapi.assignment.Assignment.submit` instead.

        :calls: `POST /api/v1/sections/:section_id/assignments/:assignment_id/submissions \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions.create>`_

        :param assignment: The object or ID of the assignment.
        :type assignment: :class:`canvasapi.assignment.Assignment` or int
        :param submission: The attributes of the submission.
        :type submission: dict

        :rtype: :class:`canvasapi.submission.Submission`
        """
        from canvasapi.assignment import Assignment

        warnings.warn(
            "Section.submit_assignment() is deprecated and will be removed "
            "in the future. Use Assignment.submit() instead.",
            DeprecationWarning,
        )

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))
        assignment = Assignment(
            self._requester,
            {"course_id": self.course_id, "section_id": self.id, "id": assignment_id},
        )
        return assignment.submit(submission, **kwargs)

    def update_submission(self, assignment, user, **kwargs):
        """
        Comment on and/or update the grading for a student's assignment submission.

        .. warning::
            .. deprecated:: 0.9.0
                Use :func:`canvasapi.submission.Submission.edit` instead.

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

        warnings.warn(
            "Section.update_submission() is deprecated and will be removed "
            "in the future. Use Submission.edit() instead.",
            DeprecationWarning,
        )

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))
        user_id = obj_or_id(user, "user", (User,))

        submission = Submission(
            self._requester,
            {
                "course_id": self.course_id,
                "assignment_id": assignment_id,
                "user_id": user_id,
            },
        )

        return submission.edit(**kwargs)
