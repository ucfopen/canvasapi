from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs, obj_or_id
from canvasapi.paginated_list import PaginatedList
from canvasapi.poll_choice import PollChoice


@python_2_unicode_compatible
class Poll(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.question, self.id)

    def update(self, poll, **kwargs):
        """
        Update an existing poll belonging to the current user.

        :calls: `PUT /api/v1/polls/:id \
        <https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.update>`_

        :param poll: List of arguments. 'Question' is required and 'Description' is optional
        :type poll:
        :rtype: :class:`canvasapi.poll.Poll
        """
        if isinstance(poll, list) and isinstance(poll[0], dict) and 'question' in poll[0]:
            kwargs['poll'] = poll
        else:
            raise RequiredFieldMissing(
                "Dictionary with key 'question' is required."
            )

        response = self._requester.request(
            'PUT',
            'polls/{}'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return Poll(self._requester, response.json()['polls'][0])

    def delete(self, **kwargs):
        """
        Delete a single poll, based on the poll id.

        :calls: `DELETE /api/v1/polls/:id \
        <https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.destroy>`_

        :returns: True if the deletion was successful, false otherwise.

        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            'polls/{}'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
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
            self.__requester,
            'GET',
            'polls/{}/poll_choices'.format(self.id),
            _root='poll_choices',
            _kwargs=combine_kwargs(**kwargs)
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
            'GET',
            'polls/{}/poll_choices/{}'.format(self.id, poll_choice_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return PollChoice(self._requester, response.json()['polls'][0])

    def create_choice(self, poll_choice, **kwargs):
        """
        Create a new choice for the current poll.

        :calls: `POST /api/v1/polls/:poll_id/poll_choices \
        <https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.create>`_

        :param choice: 'Text' of the poll is required, 'is_correct' and 'position' are optional.
        :type choice:
        :rtype: :class:`canvasapi.poll_choice.PollChoice`
        """
        if (isinstance(poll_choice, list) and isinstance(poll_choice[0], dict)
                and 'text' in poll_choice[0]):
            kwargs['poll_choice'] = poll_choice
        else:
            raise RequiredFieldMissing(
                    "Dictionary with key 'text' is required."
                )

        response = self._requester.request(
            'POST',
            'polls/{}/poll_choices'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return PollChoice(self._requester, response.json()['poll_choices'][0])
