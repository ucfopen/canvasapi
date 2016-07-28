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

    def add_recipients(self, recipients): # NEEDS TESTING ON PRODUCTION
        """
        Add a recipient to a conversation.

        :calls: `POST /api/v1/conversations/:id/add_recipients \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.add_recipients>`_

        :param recipients[]: A list of recipient ids.
            These may be user ids or course/group ids prefixed
            with 'course_' or 'group_' respectively,
            e.g. recipients[]=1&recipients=2&recipients[]=course_3
        :type recipients[]: string list
        :rtype: :class:`pycanvas.account.Conversation`
        """
        response = self._requester.request(
            'POST',
            'conversations/%s/add_recipients' % (self.id),
            recipients=recipients
        )
        return Conversation(self._requester, response.json())

    def add_message(self, body, **kwargs): # NEEDS TESTING
        """
        Add a message to a conversation.

        :calls: `POST /api/v1/conversations/:id/add_message \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.add_message>`_
        
        :param body: The body of the conversation.
        :type body: string
        :rtype: :class:`pycanvas.account.Conversation` but with only one message, the most recent one.
        """
        response = self._requester.request(
            'POST',
            'conversations/%s/add_message' % (self.id),
            body=body,
            **combine_kwargs(**kwargs)
        )
        return Conversation(self._requester, response.json())

    def delete_message(self, remove): # NEEDS TESTING
        """
        Delete messages from this conversation.
        Note that this only affects this user's view of the conversation.
        If all messages are deleted, the conversation will be as well (equivalent to DELETE) by canvas

        :calls: `POST /api/v1/conversations/:id/remove_messages \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.remove_messages>`_
        
        :param remove[]: Array of message ids to be removed.
        :type remove: list of strings
        :rtype: dict
        """
        response = self._requester.request(
            'POST',
            'conversations/%s/remove_messages' % (self.id),
            remove=remove
        )
        return response.json()
