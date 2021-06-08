from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.paginated_list import PaginatedList
from canvasapi.poll_choice import PollChoice
from canvasapi.poll_session import PollSession
from canvasapi.util import combine_kwargs, obj_or_id


class Poll(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.question, self.id)

    def update(self, poll, **kwargs):
        """
        Update an existing poll belonging to the current user.

        :calls: `PUT /api/v1/polls/:id \
        <https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.update>`_

        :param poll: List of arguments. 'Question' is required and 'Description' is optional
        :type poll: list
        :rtype: :class:`canvasapi.poll.Poll`
        """
        if (
            isinstance(poll, list)
            and isinstance(poll[0], dict)
            and "question" in poll[0]
        ):
            kwargs["poll"] = poll
        else:
            raise RequiredFieldMissing("Dictionary with key 'question' is required.")

        response = self._requester.request(
            "PUT", "polls/{}".format(self.id), _kwargs=combine_kwargs(**kwargs)
        )
        return Poll(self._requester, response.json()["polls"][0])

    def delete(self, **kwargs):
        """
        Delete a single poll, based on the poll id.

        :calls: `DELETE /api/v1/polls/:id \
        <https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.destroy>`_

        :returns: True if the deletion was successful, false otherwise.

        :rtype: bool
        """
        response = self._requester.request(
            "DELETE", "polls/{}".format(self.id), _kwargs=combine_kwargs(**kwargs)
        )
        return response.status_code == 204

    def get_choices(self, **kwargs):
        """
        Returns a paginated list of PollChoices of a poll, based on poll id.

        :calls: `GET /api/v1/polls/:poll_id/poll_choices \
        <https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.poll_choice.PollChoice`
        """
        return PaginatedList(
            PollChoice,
            self._requester,
            "GET",
            "polls/{}/poll_choices".format(self.id),
            _root="poll_choices",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_choice(self, poll_choice, **kwargs):
        """
        Returns the poll choice with the given id.

        :calls: `GET /api/v1/polls/:poll_id/poll_choices/:id \
        <https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.show>`_

        :rtype: :class:`canvasapi.poll_choice.PollChoice`
        """
        poll_choice_id = obj_or_id(poll_choice, "poll_choice", (PollChoice,))

        response = self._requester.request(
            "GET",
            "polls/{}/poll_choices/{}".format(self.id, poll_choice_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollChoice(self._requester, response.json()["poll_choices"][0])

    def create_choice(self, poll_choice, **kwargs):
        """
        Create a new choice for the current poll.

        :calls: `POST /api/v1/polls/:poll_id/poll_choices \
        <https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.create>`_

        :param poll_choice: 'text' is required, 'is_correct' and 'position' are optional.
        :type poll_choice: list
        :rtype: :class:`canvasapi.poll_choice.PollChoice`
        """
        if (
            isinstance(poll_choice, list)
            and isinstance(poll_choice[0], dict)
            and "text" in poll_choice[0]
        ):
            kwargs["poll_choice"] = poll_choice
        else:
            raise RequiredFieldMissing("Dictionary with key 'text' is required.")

        response = self._requester.request(
            "POST",
            "polls/{}/poll_choices".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollChoice(self._requester, response.json()["poll_choices"][0])

    def get_sessions(self, **kwargs):
        """
        Returns the paginated list of PollSessions in a poll.

        :calls: `GET /api/v1/polls/:poll_id/poll_sessions \
        <https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.index>`_

        :rtype: :class:`canvasapi.paginated_lsit.Paginated List` of
            :class:`canvasapi.poll_session.PollSession`
        """
        return PaginatedList(
            PollSession,
            self._requester,
            "GET",
            "polls/{}/poll_sessions".format(self.id),
            _root="poll_sessions",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_session(self, poll_session, **kwargs):
        """
        Returns the poll session with the given id.

        :calls: `GET /api/v1/polls/:poll_id/poll_sessions/:id \
        <https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.show>`_

        :param poll_session: List of arguments. Takes a poll session id (int) or poll session \
        object.

        :rtype: :class:`canvasapi.poll_session.PollSession`
        """
        poll_session_id = obj_or_id(poll_session, "poll_session", (PollSession,))

        response = self._requester.request(
            "GET",
            "polls/{}/poll_sessions/{}".format(self.id, poll_session_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollSession(self._requester, response.json()["poll_sessions"][0])

    def create_session(self, poll_session, **kwargs):
        """
        Create a new poll session for this poll

        :calls: `POST /api/v1/polls/:poll_id/poll_sessions \
        <https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.create>`_

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
            "POST",
            "polls/{}/poll_sessions".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollSession(self._requester, response.json()["poll_sessions"][0])
