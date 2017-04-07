from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class CommunicationChannel(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.address, self.id)

    def delete(self, **kwargs):
        """
        Delete this communication channel.

        :calls: `DELETE /api/v1/users/:user_id/communication_channels/:id \
        <https://canvas.instructure.com/doc/api/communication_channels.html#method.communication_channels.destroy>`_

        :rtype: :class:`canvasapi.communication_channel.CommunicationChannel`
        """
        response = self._requester.request(
            'DELETE',
            'users/%s/communication_channels/%s' % (self.user_id, self.id),
            **combine_kwargs(**kwargs)
        )

        return CommunicationChannel(self._requester, response.json())
