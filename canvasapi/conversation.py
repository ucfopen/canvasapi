from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class Conversation(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.subject, self.id)

    def edit(self, **kwargs):
        """
        Update a conversation.

        :calls: `PUT /api/v1/conversations/:id \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.update>`_

        :rtype: `bool`
        """
        response = self._requester.request(
            "PUT", "conversations/{}".format(self.id), _kwargs=combine_kwargs(**kwargs)
        )

        if response.json().get("id"):
            super(Conversation, self).set_attributes(response.json())
            return True
        else:
            return False

    def delete(self):
        """
        Delete a conversation.

        :calls: `DELETE /api/v1/conversations/:id \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.destroy>`_

        :rtype: `bool`
        """
        response = self._requester.request("DELETE", "conversations/{}".format(self.id))

        if response.json().get("id"):
            super(Conversation, self).set_attributes(response.json())
            return True
        else:
            return False

    def add_recipients(self, recipients):
        """
        Add a recipient to a conversation.

        :calls: `POST /api/v1/conversations/:id/add_recipients \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.add_recipients>`_

        :param recipients: A list of string format recipient ids.
            These may be user ids or course/group ids prefixed
            with 'course\\_' or 'group\\_' respectively,
            e.g. recipients['1', '2', 'course_3']
        :type recipients:  `list` of `str`
        :rtype: :class:`canvasapi.account.Conversation`
        """
        response = self._requester.request(
            "POST",
            "conversations/{}/add_recipients".format(self.id),
            recipients=recipients,
        )
        return Conversation(self._requester, response.json())

    def add_message(self, body, **kwargs):
        """
        Add a message to a conversation.

        :calls: `POST /api/v1/conversations/:id/add_message \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.add_message>`_

        :param body: The body of the conversation.
        :type body: str
        :returns: A conversation with only the most recent message.
        :rtype: :class:`canvasapi.account.Conversation`
        """
        response = self._requester.request(
            "POST",
            "conversations/{}/add_message".format(self.id),
            body=body,
            _kwargs=combine_kwargs(**kwargs),
        )
        return Conversation(self._requester, response.json())

    def delete_messages(self, remove):
        """
        Delete messages from this conversation.

        Note that this only affects this user's view of the conversation.
        If all messages are deleted, the conversation will be as well.

        :calls: `POST /api/v1/conversations/:id/remove_messages \
        <https://canvas.instructure.com/doc/api/conversations.html#method.conversations.remove_messages>`_

        :param remove: List of message ids to be removed.
        :type remove: `list` of `str`
        :rtype: `dict`
        """
        response = self._requester.request(
            "POST", "conversations/{}/remove_messages".format(self.id), remove=remove
        )
        return response.json()
