from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.util import combine_kwargs


class PollChoice(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.text, self.id)

    def update(self, poll_choice, **kwargs):
        """
        Update an existing choice for this poll.

        :calls: `PUT /api/v1/polls/:poll_id/poll_choices/:id \
        <https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.update>`_

        :param poll_choice: List of arguments. 'text' is required and 'is_correct' and 'position' \
        are optional.
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
            "PUT",
            "polls/{}/poll_choices/{}".format(self.poll_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PollChoice(self._requester, response.json()["poll_choices"][0])

    def delete(self, **kwargs):
        """
        Delete a single poll, based on the poll id.

        :calls: `DELETE /api/v1/polls/:poll_id/poll_choices/:id \
        <https://canvas.instructure.com/doc/api/poll_choices.html#method.polling/poll_choices.destroy>`_

        :returns: True if the deletion was successful, false otherwise.

        :rtype: bool
        """
        response = self._requester.request(
            "DELETE",
            "polls/{}/poll_choices/{}".format(self.poll_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.status_code == 204
