from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import CanvasException, RequiredFieldMissing
from canvasapi.paginated_list import PaginatedList
from canvasapi.peer_review import PeerReview
from canvasapi.progress import Progress
from canvasapi.submission import Submission
from canvasapi.upload import Uploader
from canvasapi.user import User
from canvasapi.user import UserDisplay
from canvasapi.util import combine_kwargs, obj_or_id


@python_2_unicode_compatible
class Assignment(CanvasObject):
    def __init__(self, requester, attributes):
        super(Assignment, self).__init__(requester, attributes)

        if "overrides" in attributes:
            self.overrides = [
                AssignmentOverride(requester, override)
                for override in attributes["overrides"]
            ]

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def create_override(self, **kwargs):
        """
        Create an override for this assignment.

        :calls: `POST /api/v1/courses/:course_id/assignments/:assignment_id/overrides \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.create>`_

        :rtype: :class:`canvasapi.assignment.AssignmentOverride`
        """
        response = self._requester.request(
            "POST",
            "courses/{}/assignments/{}/overrides".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update(course_id=self.course_id)
        return AssignmentOverride(self._requester, response_json)

    def delete(self, **kwargs):
        """
        Delete this assignment.

        :calls: `DELETE /api/v1/courses/:course_id/assignments/:id \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments.destroy>`_

        :rtype: :class:`canvasapi.assignment.Assignment`
        """
        response = self._requester.request(
            "DELETE",
            "courses/{}/assignments/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
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
            "PUT",
            "courses/{}/assignments/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        if "name" in response.json():
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
            "GET",
            "courses/{}/assignments/{}/gradeable_students".format(
                self.course_id, self.id
            ),
            {"course_id": self.course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_override(self, override, **kwargs):
        """
        Get a single assignment override with the given override id.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/overrides/:id \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.show>`_

        :param override: The object or ID of the override to get
        :type override: :class:`canvasapi.assignment.AssignmentOverride` or int

        :rtype: :class:`canvasapi.assignment.AssignmentOverride`
        """
        override_id = obj_or_id(override, "override", (AssignmentOverride,))

        response = self._requester.request(
            "GET",
            "courses/{}/assignments/{}/overrides/{}".format(
                self.course_id, self.id, override_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update(course_id=self.course_id)
        return AssignmentOverride(self._requester, response_json)

    def get_overrides(self, **kwargs):
        """
        Get a paginated list of overrides for this assignment that target
        sections/groups/students visible to the current user.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/overrides \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.AssignmentOverride`
        """
        return PaginatedList(
            AssignmentOverride,
            self._requester,
            "GET",
            "courses/{}/assignments/{}/overrides".format(self.course_id, self.id),
            {"course_id": self.course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_peer_reviews(self, **kwargs):
        """
        Get a list of all Peer Reviews for this assignment.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/peer_reviews \
        <https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.peer_review.PeerReview`
        """
        return PaginatedList(
            PeerReview,
            self._requester,
            "GET",
            "courses/{}/assignments/{}/peer_reviews".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
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
        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            "GET",
            "courses/{}/assignments/{}/submissions/{}".format(
                self.course_id, self.id, user_id
            ),
            _kwargs=combine_kwargs(**kwargs),
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
            "GET",
            "courses/{}/assignments/{}/submissions".format(self.course_id, self.id),
            {"course_id": self.course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def set_extensions(self, assignment_extensions, **kwargs):
        """
        Set extensions for student assignment submissions

        :calls: `POST /api/v1/courses/:course_id/assignments/:assignment_id/extensions \
        <https://canvas.instructure.com/doc/api/assignment_extensions.html#method.assignment_extensions.create>`_

        :param assignment_extensions: list of dictionaries representing extensions
        :type assignment_extensions: list

        :rtype: list of :class:`canvasapi.assignment.AssignmentExtension`

        Example Usage:

        >>> assignment.set_extensions([
        ...     {
        ...         'user_id': 3,
        ...         'extra_attempts: 2
        ...     },
        ...     {
        ...         'user_id': 2,
        ...         'extra_attempts: 2
        ...     }
        ... ])
        """
        if not isinstance(assignment_extensions, list) or not assignment_extensions:
            raise ValueError("Param `assignment_extensions` must be a non-empty list.")

        if any(not isinstance(extension, dict) for extension in assignment_extensions):
            raise ValueError(
                "Param `assignment_extensions` must only contain dictionaries"
            )

        if any("user_id" not in extension for extension in assignment_extensions):
            raise RequiredFieldMissing(
                "Dictionaries in `assignment_extensions` must contain key `user_id`"
            )
        kwargs["assignment_extensions"] = assignment_extensions
        response = self._requester.request(
            "POST",
            "courses/{}/assignments/{}/extensions".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        extension_list = response.json()["assignment_extensions"]
        return [
            AssignmentExtension(self._requester, extension)
            for extension in extension_list
        ]

    def submissions_bulk_update(self, **kwargs):
        """
        Update the grading and comments on multiple student's assignment
        submissions in an asynchronous job.

        :calls: `POST /api/v1/courses/:course_id/assignments/:assignment_id/ \
            submissions/update_grades \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.bulk_update>`_

        :rtype: :class:`canvasapi.progress.Progress`
        """
        response = self._requester.request(
            "POST",
            "courses/{}/assignments/{}/submissions/update_grades".format(
                self.course_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Progress(self._requester, response.json())

    def submit(self, submission, file=None, **kwargs):
        """
        Makes a submission for an assignment.

        :calls: `POST /api/v1/courses/:course_id/assignments/:assignment_id/submissions \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions.create>`_

        :param submission: The attributes of the submission.
        :type submission: dict
        :param file: A file to upload with the submission. (Optional,
            defaults to `None`. Submission type must be `online_upload`)
        :type file: file or str

        :rtype: :class:`canvasapi.submission.Submission`
        """
        if isinstance(submission, dict) and "submission_type" in submission:
            kwargs["submission"] = submission
        else:
            raise RequiredFieldMissing(
                "Dictionary with key 'submission_type' is required."
            )

        if file:
            if submission.get("submission_type") != "online_upload":
                raise ValueError(
                    "To upload a file, `submission['submission_type']` must be `online_upload`."
                )

            upload_response = self.upload_to_submission(file, **kwargs)
            if upload_response[0]:
                kwargs["submission"]["file_ids"] = [upload_response[1]["id"]]
            else:
                raise CanvasException("File upload failed. Not submitting.")

        response = self._requester.request(
            "POST",
            "courses/{}/assignments/{}/submissions".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update(course_id=self.course_id)

        return Submission(self._requester, response_json)

    def upload_to_submission(self, file, user="self", **kwargs):
        """
        Upload a file to a submission.

        :calls: `POST /api/v1/courses/:course_id/assignments/:assignment_id/ \
            submissions/:user_id/files \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.create_file>`_

        :param file: The file or path of the file to upload.
        :type file: file or str
        :param user: The object or ID of the related user, or 'self' for the
            current user. Defaults to 'self'.
        :type user: :class:`canvasapi.user.User`, int, or str

        :returns: True if the file uploaded successfully, False otherwise, \
                    and the JSON response from the API.
        :rtype: tuple
        """
        user_id = obj_or_id(user, "user", (User,))

        return Uploader(
            self._requester,
            "courses/{}/assignments/{}/submissions/{}/files".format(
                self.course_id, self.id, user_id
            ),
            file,
            **kwargs
        ).start()


@python_2_unicode_compatible
class AssignmentExtension(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.assignment_id, self.user_id)


@python_2_unicode_compatible
class AssignmentGroup(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def delete(self, **kwargs):
        """
        Delete this assignment.

        :calls: `DELETE /api/v1/courses/:course_id/assignment_groups/:assignment_group_id \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.destroy>`_

        :rtype: :class:`canvasapi.assignment.AssignmentGroup`
        """
        response = self._requester.request(
            "DELETE",
            "courses/{}/assignment_groups/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return AssignmentGroup(self._requester, response.json())

    def edit(self, **kwargs):
        """
        Modify this assignment group.

        :calls: `PUT /api/v1/courses/:course_id/assignment_groups/:assignment_group_id \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.update>`_

        :rtype: :class:`canvasapi.assignment.AssignmentGroup`
        """
        response = self._requester.request(
            "PUT",
            "courses/{}/assignment_groups/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        if "name" in response.json():
            super(AssignmentGroup, self).set_attributes(response.json())

        return AssignmentGroup(self._requester, response.json())


@python_2_unicode_compatible
class AssignmentOverride(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)

    def delete(self, **kwargs):
        """
        Delete this assignment override.

        :calls: `DELETE /api/v1/courses/:course_id/assignments/:assignment_id/overrides/:id
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.destroy>`_

        :returns: The previous content of the now-deleted assignment override.
        :rtype: :class:`canvasapi.assignment.AssignmentGroup`
        """
        response = self._requester.request(
            "DELETE",
            "courses/{}/assignments/{}/overrides/{}".format(
                self.course_id, self.assignment_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update(course_id=self.course_id)

        return AssignmentOverride(self._requester, response_json)

    def edit(self, **kwargs):
        """
        Update this assignment override.

        Note: All current overridden values must be supplied if they are to be retained.

        :calls: `PUT /api/v1/courses/:course_id/assignments/:assignment_id/overrides/:id
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.update>`_

        :rtype: :class:`canvasapi.assignment.AssignmentOverride`
        """
        response = self._requester.request(
            "PUT",
            "courses/{}/assignments/{}/overrides/{}".format(
                self.course_id, self.assignment_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update(course_id=self.course_id)
        if "title" in response_json:
            super(AssignmentOverride, self).set_attributes(response_json)

        return self
