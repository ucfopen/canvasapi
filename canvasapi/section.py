from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.paginated_list import PaginatedList
from canvasapi.submission import Submission
from canvasapi.util import combine_kwargs


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
            'sections/%s/enrollments' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def cross_list_section(self, new_course_id):
        """
        Move the Section to another course.

        :calls: `POST /api/v1/sections/:id/crosslist/:new_course_id
        \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.crosslist>`_

        :rtype: :class:`canvasapi.section.Section`
        """
        response = self._requester.request(
            'POST',
            'sections/%s/crosslist/%s' % (self.id, new_course_id)
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
            "DELETE",
            "sections/%s/crosslist" % (self.id)
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
            "PUT",
            "sections/%s" % (self.id)
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
            "DELETE",
            "sections/%s" % (self.id)
        )
        return Section(self._requester, response.json())

    def submit_assignment(self, assignment_id, submission, **kwargs):
        """
        Makes a submission for an assignment.

        :calls: `POST /api/v1/sections/:section_id/assignments/:assignment_id/submissions \
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
            'sections/%s/assignments/%s/submissions' % (self.id, assignment_id),
            **combine_kwargs(**kwargs)
        )

        return Submission(self._requester, response.json())

    def list_submissions(self, assignment_id, **kwargs):
        """
        Makes a submission for an assignment.

        :calls: `GET /api/v1/sections/:section_id/assignments/:assignment_id/submissions  \
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
            'sections/%s/assignments/%s/submissions' % (self.id, assignment_id),
            **combine_kwargs(**kwargs)
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
        return PaginatedList(
            Submission,
            self._requester,
            'GET',
            'sections/%s/students/submissions' % (self.id),
            grouped=False,
            **combine_kwargs(**kwargs)
        )

    def get_submission(self, assignment_id, user_id, **kwargs):
        """
        Get a single submission, based on user id.

        :calls: `GET /api/v1/sections/:section_id/assignments/:assignment_id/submissions/:user_id \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.show>`_

        :param assignment_id: The ID of the assignment.
        :type assignment_id: int
        :param user_id: The ID of the user.
        :type user_id: str
        :rtype: :class:`canvasapi.submission.Submission`
        """
        response = self._requester.request(
            'GET',
            'sections/%s/assignments/%s/submissions/%s' % (self.id, assignment_id, user_id),
            **combine_kwargs(**kwargs)
        )
        return Submission(self._requester, response.json())

    def update_submission(self, assignment_id, user_id, **kwargs):
        """
        Comment on and/or update the grading for a student's assignment submission.

        :calls: `PUT /api/v1/sections/:section_id/assignments/:assignment_id/submissions/:user_id \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.update>`_

        :param assignment_id: The ID of the assignment.
        :type assignment_id: int
        :param user_id: The ID of the user.
        :type user_id: str
        :rtype: :class:`canvasapi.submission.Submission`
        """
        response = self._requester.request(
            'PUT',
            'sections/%s/assignments/%s/submissions/%s' % (self.id, assignment_id, user_id),
            **combine_kwargs(**kwargs)
        )

        submission = self.get_submission(assignment_id, user_id)

        if 'submission_type' in response.json():
            super(Submission, submission).set_attributes(response.json())

        return Submission(self._requester, response.json())

    def mark_submission_as_read(self, assignment_id, user_id):
        """
        Mark submission as read. No request fields are necessary.

        :calls: `PUT
            /api/v1/sections/:section_id/assignments/:assignment_id/submissions/:user_id/read \
            <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_read>`_

        :rtype: `bool`
        """
        response = self._requester.request(
            'PUT',
            'sections/%s/assignments/%s/submissions/%s/read' % (
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
            /api/v1/sections/:section_id/assignments/:assignment_id/submissions/:user_id/read \
            <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_unread>`_

        :rtype: `bool`
        """
        response = self._requester.request(
            'DELETE',
            'sections/%s/assignments/%s/submissions/%s/read' % (
                self.id,
                assignment_id,
                user_id,
            ),
        )
        return response.status_code == 204
