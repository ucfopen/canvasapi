from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


@python_2_unicode_compatible
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
        if (isinstance(poll_session, list) and isinstance(poll_session[0], dict) and 'course_id'
                in poll_session[0]):
            kwargs['poll_session'] = poll_session
        else:
            raise RequiredFieldMissing(
                "Dictionary with key 'course_id' is required."
            )

        response = self._requester.request(
            'PUT',
            'polls/{}/poll_sessions/{}'.format(self.poll_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return PollSession(self._requester, response.json()['poll_sessions'][0])

    def delete(self, **kwargs):
        """
        Delete a single poll session, based on the session id.

        :calls: `DELETE /api/v1/polls/:poll_id/poll_sessions/:id \
        <https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.destroy>`_

        :returns: True if the deletion was successful, false otherwise.

        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            'polls/{}/poll_sessions/{}'.format(self.poll_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
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
            'GET',
            'polls/{}/poll_sessions/{}/open'.format(self.poll_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return PollSession(self._requester, response.json()['poll_sessions'][0])

    def close(self, **kwargs):
        """
        Close a poll session to answers based on the poll id.

        :calls: `GET /api/v1/polls/:poll_id/poll_sessions/:id/close \
        <https://canvas.instructure.com/doc/api/poll_sessions.html#method.polling/poll_sessions.close>`_

        :returns: :class:`canvasapi.poll_session.PollSession`
        """
        response = self._requester.request(
            'GET',
            'polls/{}/poll_sessions/{}/close'.format(self.poll_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return PollSession(self._requester, response.json()['poll_sessions'][0])
