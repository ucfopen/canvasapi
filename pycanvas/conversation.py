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

        :param recipients[]: An array of recipient ids.
            These may be user ids or course/group ids prefixed
            with 'course_' or 'group_' respectively,
            e.g. recipients[]=1&recipients=2&recipients[]=course_3
        :type recipients[]: string array
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

    def delete_message(self, messages): # NEEDS TESTING
        """
        Delete messages from this conversation.
        Note that this only affects this user's view of the conversation.
        If all messages are deleted, the conversation will be as well (equivalent to DELETE) by canvas

        :calls: `POST /api/v1/conversations/:id/remove_messages \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.remove_messages>`_
        
        :param remove[]: Array of message ids to be removed.
        :type remove: array of strings
        :rtype: dict
        """
        response = self._requester.request(
            'POST',
            'conversations/%s/remove_messages' % (self.id),
            remove=messages
        )
        return response.json()

    def mark_all_as_read(self):
        """
        Mark all conversations as read.
        :calls: `POST /api/v1/conversations/mark_all_as_read \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.mark_all_as_read>`_
        
        :rtype: bool
        """
        response = self._requester.request(
            'POST',
            'conversations/mark_all_as_read'
        )
        return response.json() == {}

    def unread_count(self):
        """
        Get the number of unread conversations for the current user

        :calls: `GET /api/v1/conversations/unread_count \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.unread_count>`_
        
        :rtype: simple object with unread_count, example: {'unread_count': '7'}
        """
        response = self._requester.request(
            'GET',
            'conversations/unread_count'
        )

        return response.json()
        
    def get_running_batches(self):
        """
        Returns any currently running conversation batches for the current user.
        Conversation batches are created when a bulk private message is sent 
        asynchronously.

        :calls: `GET /api/v1/conversations/batches \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.batches>`_
        
        :rtype: dict with array of batch objects - not currently a Class
        """

        response = self._requester.request(
            'GET',
            'conversations/batches'
        )

        return response.json()

    def batch_update(self, conversation_ids, event): # IN PROGRESS
        """
        
        :calls: `PUT /api/v1/conversations \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.batch_update>`_
        
        :param conversation_ids[]: List of conversations to update. Limited to 500 conversations.
        :type conversation_ids: array of strings
        :param event: The action to take on each conversation.
        :type event: string
        :rtype: json object for a Progress - currently undefined class
        """

        from pycanvas.process import Process

        ALLOWED_EVENTS = [
            'mark_as_read',
            'mark_as_unread',
            'star',
            'unstar',
            'archive',
            'destroy'
        ]

        try:
            if not event in ALLOWED_EVENTS:
                raise ValueError('%s is not a valid action. Please use one of the following: %s' % (
                    event,
                    ','.join(ALLOWED_EVENTS)
                ))

            if len(conversation_ids) > 500:
                raise ValueError('You have requested %s updates, which exceeds the limit of 500' % (
                    len(conversation_ids)
                ))

            response = self._requester.request(
                'PUT',
                'conversations',
                conversation_ids=conversation_ids,
                event=event
            )
            return_process = Process(self._requester, response.json())
            return return_process

        except ValueError as e:
            return e
