from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


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
