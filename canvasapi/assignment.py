from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.paginated_list import PaginatedList
from canvasapi.submission import Submission
from canvasapi.user import UserDisplay
from canvasapi.util import combine_kwargs, obj_or_id


@python_2_unicode_compatible
class Assignment(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def delete(self, **kwargs):
        """
        Delete this assignment.

        :calls: `DELETE /api/v1/courses/:course_id/assignments/:id \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments.destroy>`_

        :rtype: :class:`canvasapi.assignment.Assignment`
        """
        response = self._requester.request(
            'DELETE',
            'courses/{}/assignments/{}'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return Assignment(self._requester, response.json())

    def edit(self, **kwargs):
        """
        Modify this assignment.

        :calls: `PUT /api/v1/courses/:course_id/assignments/:id \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.update>`_

        :rtype: :class:`canvasapi.assignment.Assignment`
        """
        response = self._requester.request(
            'PUT',
            'courses/{}/assignments/{}'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        if 'name' in response.json():
            super(Assignment, self).set_attributes(response.json())

        return Assignment(self._requester, response.json())

    def get_gradeable_students(self, **kwargs):
        """
        List students eligible to submit the assignment.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/gradeable_students  \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.gradeable_students>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.user.UserDisplay`
        """
        return PaginatedList(
            UserDisplay,
            self._requester,
            'GET',
            'courses/{}/assignments/{}/gradeable_students'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_submission(self, user, **kwargs):
        """
        Get a single submission, based on user id.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.show>`_

        :param user: The object or ID of the related user
        :type user: :class:`canvasapi.user.User` or int

        :rtype: :class:`canvasapi.submission.Submission`
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            'GET',
            'courses/{}/assignments/{}/submissions/{}'.format(self.course_id, self.id, user_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update(course_id=self.course_id)

        return Submission(self._requester, response_json)

    def get_submissions(self, **kwargs):
        """
        Get all existing submissions for this assignment.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions  \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.submission.Submission`
        """
        return PaginatedList(
            Submission,
            self._requester,
            'GET',
            'courses/{}/assignments/{}/submissions'.format(self.course_id, self.id),
            {'course_id': self.course_id},
            _kwargs=combine_kwargs(**kwargs)
        )

    def submit(self, submission, **kwargs):
        """
        Makes a submission for an assignment.

        :calls: `POST /api/v1/courses/:course_id/assignments/:assignment_id/submissions \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions.create>`_

        :param submission: The attributes of the submission.
        :type submission: dict

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
            'courses/{}/assignments/{}/submissions'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update(course_id=self.course_id)

        return Submission(self._requester, response_json)


@python_2_unicode_compatible
class AssignmentGroup(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def edit(self, **kwargs):
        """
        Modify this assignment group.

        :calls: `PUT /api/v1/courses/:course_id/assignment_groups/:assignment_group_id \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.update>`_

        :rtype: :class:`canvasapi.assignment.AssignmentGroup`
        """
        response = self._requester.request(
            'PUT',
            'courses/{}/assignment_groups/{}'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        if 'name' in response.json():
            super(AssignmentGroup, self).set_attributes(response.json())

        return AssignmentGroup(self._requester, response.json())

    def delete(self, **kwargs):
        """
        Delete this assignment.

        :calls: `DELETE /api/v1/courses/:course_id/assignment_groups/:assignment_group_id \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.destroy>`_

        :rtype: :class:`canvasapi.assignment.AssignmentGroup`
        """
        response = self._requester.request(
            'DELETE',
            'courses/{}/assignment_groups/{}'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return AssignmentGroup(self._requester, response.json())
