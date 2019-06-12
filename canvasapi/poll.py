from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs, obj_or_id
from canvasapi.paginated_list import PaginatedList
from canvasapi.poll_choice import PollChoice


@python_2_unicode_compatible
class Poll(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.question, self.id)

    def update(self, question, description, **kwargs):
        """
        Update an existing poll belonging to the current user, based on poll id.

        :calls: `PUT /api/v1/polls/:id \
        <https://canvas.instructure.com/doc/api/polls.html#method.polling/polls.update>`_

        :returns: True is the poll was updated, False otherwise.
        :rtype: bool
        """
        kwargs['question'] = question
        kwargs['description'] = description

        response = self._requester.request(
            'PUT',
            'polls/{}'.format(self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return Poll(self._requester, response.json())

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
        return PollChoice(self._requester, response.json())
