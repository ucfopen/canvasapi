from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.poll_submission import PollSubmission
from canvasapi.util import combine_kwargs, obj_or_id


class PollSession(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.poll_id, self.id)

    def update(self, poll_session, **kwargs):
        """
        Update an existing poll session for a poll based on poll id.

        :calls: `PUT /api/v1/polls/:poll_id/poll_sessions/:id \
        <https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.update>`_

        :param poll_session: List of arguments. course_id (required): id of the course for the
            session, course_section_id (optional): id of the course section for this session,
            has_public_results (optional): whether the results are viewable by students.
        :type poll_session: list

        :rtype: :class:`canvasapi.poll_session.PollSession`
        """
        if (
            isinstance(poll_session, list)
            and isinstance(poll_session[0], dict)
            and "course_id" in poll_session[0]
        ):
            kwargs["poll_session"] = poll_session
        else:
            raise RequiredFieldMissing("Dictionary with key 'course_id' is required.")

        response = self._requester.request(
            "PUT",
            "polls/{}/poll_sessions/{}".format(self.poll_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollSession(self._requester, response.json()["poll_sessions"][0])

    def delete(self, **kwargs):
        """
        Delete a single poll session, based on the session id.

        :calls: `DELETE /api/v1/polls/:poll_id/poll_sessions/:id \
        <https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.destroy>`_

        :returns: True if the deletion was successful, false otherwise.

        :rtype: bool
        """
        response = self._requester.request(
            "DELETE",
            "polls/{}/poll_sessions/{}".format(self.poll_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.status_code == 204

    def open(self, **kwargs):
        """
        Open a poll session to answers based on the poll id.

        :calls: `GET /api/v1/polls/:poll_id/poll_sessions/:id/open \
        <https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.open>`_

        :returns: :class:`canvasapi.poll_session.PollSession`
        """
        response = self._requester.request(
            "GET",
            "polls/{}/poll_sessions/{}/open".format(self.poll_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollSession(self._requester, response.json()["poll_sessions"][0])

    def close(self, **kwargs):
        """
        Close a poll session to answers based on the poll id.

        :calls: `GET /api/v1/polls/:poll_id/poll_sessions/:id/close \
        <https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.close>`_

        :returns: :class:`canvasapi.poll_session.PollSession`
        """
        response = self._requester.request(
            "GET",
            "polls/{}/poll_sessions/{}/close".format(self.poll_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollSession(self._requester, response.json()["poll_sessions"][0])

    def get_submission(self, poll_submission, **kwargs):
        """
        Returns the poll submission with the given id.

        :calls: `GET /api/v1/polls/:poll_id/poll_sessions/:poll_session_id/poll_submissions/:id \
        <https://canvas.instructure.com/doc/api/poll_submissions.html#method.polling/poll_submissions.show>`_

        :param poll_submission: Takes a poll submission id (int) or object.
        :type poll_submission: int or :class:`canvasapi.poll_submission.PollSubmission`

        :rtype: :class:`canvasapi.poll_submission.PollSubmission`
        """
        poll_submission_id = obj_or_id(
            poll_submission, "poll_submission", (PollSubmission,)
        )

        response = self._requester.request(
            "GET",
            "polls/{}/poll_sessions/{}/poll_submissions/{}".format(
                self.poll_id, self.id, poll_submission_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollSubmission(self._requester, response.json()["poll_submissions"][0])

    def create_submission(self, poll_submissions, **kwargs):
        """
        Create a new poll submission for this poll session.

        :calls: `POST /api/v1/polls/:poll_id/poll_sessions/:poll_session_id/poll_submissions \
        <https://canvas.instructure.com/doc/api/poll_submissions.html#method.polling/poll_submissions.create>`_

        :param poll_submissions: List of arguments. poll_choice_id (required int): Chosen poll \
        choice for this submission.
        :type poll_submissions: list

        :rtype: :class:`canvasapi.poll_submission.PollSubmission`
        """
        if (
            isinstance(poll_submissions, list)
            and isinstance(poll_submissions[0], dict)
            and "poll_choice_id" in poll_submissions[0]
        ):
            kwargs["poll_submissions"] = poll_submissions
        else:
            raise RequiredFieldMissing(
                "Dictionary with key 'poll_choice_id is required."
            )

        response = self._requester.request(
            "POST",
            "polls/{}/poll_sessions/{}/poll_submissions".format(self.poll_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollSubmission(self._requester, response.json()["poll_submissions"][0])
