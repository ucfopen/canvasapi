from canvasapi.canvas_object import CanvasObject
from canvasapi.file import File
from canvasapi.paginated_list import PaginatedList
from canvasapi.peer_review import PeerReview
from canvasapi.upload import FileOrPathLike, Uploader
from canvasapi.user import UserDisplay
from canvasapi.util import combine_kwargs, obj_or_id


class Submission(CanvasObject):
    def __init__(self, requester, attributes):
        super(Submission, self).__init__(requester, attributes)

        self.submission_comments = [
            SubmissionComment(self._requester, submission_comment)
            for submission_comment in attributes.get("submission_comments", [])
        ]

        self.attachments = [
            File(self._requester, attachment)
            for attachment in attributes.get("attachments", [])
        ]

    def __str__(self):
        return "{}-{}".format(self.assignment_id, self.user_id)

    def create_submission_peer_review(self, user, **kwargs):
        """
        Create a peer review for this submission.

        :calls: `POST /api/v1/courses/:course_id/assignments/:assignment_id/ \
            submissions/:submission_id/peer_reviews \
        <https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index>`_

        :param user: The user object or ID to retrieve notifications for.
        :type user: :class:`canvasapi.user.User` or int

        :rtype: :class:`canvasapi.peer_review.PeerReview`
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))
        kwargs["user_id"] = user_id
        response = self._requester.request(
            "POST",
            "courses/{}/assignments/{}/submissions/{}/peer_reviews".format(
                self.course_id, self.assignment_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        return PeerReview(self._requester, response.json())

    def delete_comment(self, submission_comment, **kwargs):
        """
        Delete a submission comment

        :calls: `DELETE /api/v1/courses/:course_id/assignments/:assignment_id/ \
            submissions/:user_id/comments/:id \
        <https://canvas.instructure.com/doc/api/submission_comments.html#method.submission_comments_api.destroy>`_

        :param submission_comment: The comment to be deleted
        :type user: :class:`canvasapi.submission.SubmissionComment` or int

        :rtype: :class:`canvasapi.submission.SubmissionComment`
        """
        submission_comment_id = obj_or_id(
            submission_comment, "submission_comment", (SubmissionComment,)
        )
        response = self._requester.request(
            "DELETE",
            "courses/{}/assignments/{}/submissions/{}/comments/{}".format(
                self.course_id, self.assignment_id, self.user_id, submission_comment_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        return SubmissionComment(self._requester, response.json())

    def delete_submission_peer_review(self, user, **kwargs):
        """
        Delete a peer review for this submission.

        :calls: `DELETE /api/v1/courses/:course_id/assignments/:assignment_id/ \
            submissions/:submission_id/peer_reviews \
        <https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index>`_

        :param user: The user object or ID to retrieve notifications for.
        :type user: :class:`canvasapi.user.User` or int

        :rtype: :class:`canvasapi.peer_review.PeerReview`
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))
        kwargs["user_id"] = user_id
        response = self._requester.request(
            "DELETE",
            "courses/{}/assignments/{}/submissions/{}/peer_reviews".format(
                self.course_id, self.assignment_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PeerReview(self._requester, response.json())

    def edit(self, **kwargs):
        """
        Comment on and/or update the grading for a student's assignment submission.

        :calls: `PUT /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.update>`_

        :rtype: :class:`canvasapi.submission.Submission`
        """
        response = self._requester.request(
            "PUT",
            "courses/{}/assignments/{}/submissions/{}".format(
                self.course_id, self.assignment_id, self.user_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()

        response_json.update(course_id=self.course_id)

        super(Submission, self).set_attributes(response_json)
        return self

    def edit_comment(self, submission_comment, **kwargs):
        """
        Edit a submission comment

        :calls: `PUT /api/v1/courses/:course_id/assignments/:assignment_id/ \
            submissions/:user_id/comments/:id
        <https://canvas.instructure.com/doc/api/submission_comments.html#method.submission_comments_api.update>`_

        :param submission_comment: The comment to be edited
        :type user: :class:`canvasapi.submission.SubmissionComment` or int

        :rtype: :class:`canvasapi.submission.SubmissionComment`
        """
        submission_comment_id = obj_or_id(
            submission_comment, "submission_comment", (SubmissionComment,)
        )
        response = self._requester.request(
            "PUT",
            "courses/{}/assignments/{}/submissions/{}/comments/{}".format(
                self.course_id, self.assignment_id, self.user_id, submission_comment_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        return SubmissionComment(self._requester, response.json())

    def get_submission_peer_reviews(self, **kwargs):
        """
        Get a list of all Peer Reviews this submission.

        :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/ \
            submissions/:submission_id/peer_reviews \
        <https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.peer_review.PeerReview`
        """
        return PaginatedList(
            PeerReview,
            self._requester,
            "GET",
            "courses/{}/assignments/{}/submissions/{}/peer_reviews".format(
                self.course_id, self.assignment_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

    def mark_read(self, **kwargs):
        """
        Mark submission as read. No request fields are necessary.

        :calls: `PUT
            /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/read \
            <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_read>`_

        :returns: True if successfully marked as read.
        :rtype: bool
        """
        response = self._requester.request(
            "PUT",
            "courses/{}/assignments/{}/submissions/{}/read".format(
                self.course_id, self.assignment_id, self.user_id
            ),
        )
        return response.status_code == 204

    def mark_unread(self, **kwargs):
        """
        Mark submission as unread. No request fields are necessary.

        :calls: `DELETE
            /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/read \
            <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_unread>`_

        :returns: True if successfully marked as unread.
        :rtype: bool
        """
        response = self._requester.request(
            "DELETE",
            "courses/{}/assignments/{}/submissions/{}/read".format(
                self.course_id, self.assignment_id, self.user_id
            ),
        )
        return response.status_code == 204

    def upload_comment(self, file: FileOrPathLike, **kwargs):
        """
        Upload a file to attach to this submission as a comment.

        :calls: `POST \
        /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/comments/files \
        <https://canvas.instructure.com/doc/api/submission_comments.html#method.submission_comments_api.create_file>`_

        :param file: The file or path of the file to upload.
        :type file: file or str
        :returns: True if the file uploaded successfully, False otherwise, \
            and the JSON response from the API.
        :rtype: tuple
        """
        response = Uploader(
            self._requester,
            "courses/{}/assignments/{}/submissions/{}/comments/files".format(
                self.course_id, self.assignment_id, self.user_id
            ),
            file,
            **kwargs,
        ).start()

        if response[0]:
            self.edit(comment={"file_ids": [response[1]["id"]]})
        return response


class GroupedSubmission(CanvasObject):
    def __init__(self, requester, attributes):
        super(GroupedSubmission, self).__init__(requester, attributes)

        try:
            self.submissions = [
                Submission(requester, submission)
                for submission in attributes["submissions"]
            ]
        except KeyError:
            self.submissions = list()

    def __str__(self):
        return "{} submission(s) for User #{}".format(
            len(self.submissions), self.user_id
        )


class SubmissionComment(CanvasObject):
    def __init__(self, requester, attributes):
        super(SubmissionComment, self).__init__(requester, attributes)

        self.author = UserDisplay(requester, self.author)

    def __str__(self):
        return f"{self.id} (by {self.author})"
