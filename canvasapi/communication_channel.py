from canvasapi.canvas_object import CanvasObject
from canvasapi.notification_preference import NotificationPreference


class CommunicationChannel(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.address, self.id)

    def list_preferences(self):
        """
        Fetch all preferences for the given communication channel.

        :calls: `GET
            /api/v1/users/:user_id/communication_channels/:cc_id/notification_preferences \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.index>`_

        :rtype: `list`
        """
        response = self._requester.request(
            'GET',
            'users/%s/communication_channels/%s/notification_preferences' % (
                self.user_id,
                self.id
            )
        )
        return response.json()['notification_preferences']

    def list_preference_categories(self):
        """
        Fetch all notification preference categories for the given communication
        channel.

        :calls: `GET
            /api/v1/users/:u_id/communication_channels/:cc_id/notification_preference_categories \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.category_index>`_

        :rtype: `list`
        """
        response = self._requester.request(
            'GET',
            'users/%s/communication_channels/%s/notification_preference_categories' % (
                self.user_id,
                self.id
            )
        )
        return response.json()['categories']

    def get_preference(self, notification):
        """
        Fetch the preference for the given notification for the  given
        communication channel.

        :calls: `GET
            /api/v1/users/:u_id/communication_channels/:co_id/notification_preferences/:notif \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.show>`_

        :param notification: The name of the notification.
        :type notification: str
        :rtype: :class:`canvasapi.notification_preference.NotificationPreference`
        """
        response = self._requester.request(
            'GET',
            'users/%s/communication_channels/%s/notification_preferences/%s' % (
                self.user_id,
                self.id,
                notification
            )
        )
        data = response.json()['notification_preferences'][0]
        return NotificationPreference(self._requester, data)
