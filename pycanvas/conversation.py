from pycanvas.canvas_object import CanvasObject
from pycanvas.util import combine_kwargs


class Conversation(CanvasObject):

    def __str__(self):
        return "%s %s" % (self.id, self.subject)

    def edit(self, **kwargs):
        """
        Update a conversation.

        :calls: `PUT /api/v1/conversations/:id \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.update>`_

        :rtype: bool
        """
        response = self._requester.request(
            'PUT',
            'conversations/%s' % (self.id),
            **combine_kwargs(**kwargs)
        )

        if response.json().get('id'):
            super(Conversation, self).set_attributes(response.json())
            return True
        else:
            return False

    def delete(self):
        """
        Delete a conversation.

        :calls: `DELETE /api/v1/conversations/:id \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.destroy>`_

        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            'conversations/%s' % (self.id)
        )

        if response.json().get('id'):
            super(Conversation, self).set_attributes(response.json())
            return True
        else:
            return False
