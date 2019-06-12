from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


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
        :type poll: list
        :returns: True is the poll was updated, False otherwise.
        :rtype: bool
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

        :returns: True if the deletion was successfull, false otherwise.

        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            'polls/{}'.format(self.id)
        )
        return response.status_code == 204
