from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.notification_preference import NotificationPreferenceList
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

    def list_preferences(self):
        """
        Fetch all preferences for the given communication channel.

        :calls: `GET
            /api/v1/users/:user_id/communication_channels/:cc_id/notification_preferences \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.notification_preference.NotificationPreference`
        """
        response = self._requester.request(
            'GET',
            'users/%s/communication_channels/%s/notification_preferences' % (
                self.user_id,
                self.id
            )
        )
        return NotificationPreferenceList(self._requester, response.json())

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
        data = NotificationPreferenceList(self._requester, response.json())
        return data.categories

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

        # returns a dict with a list of NotificationPreferences
        data = NotificationPreferenceList(self._requester, response.json())
        return data.notification_preferences[0]

    def update_preference(self, notification, notification_preferences, **kwargs):
        """
        Change the preference for a single notification for a single
        communication channel.

        :calls: `PUT
            /api/v1/users/:u_id/communication_channels/:cc_id/notification_preferences/:notif \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.update>`_

        :rtype: :class:`canvasapi.notification_preference.NotificationPreference`
        """
        if isinstance(notification_preferences, dict) and 'frequency' in notification_preferences:
            kwargs['notification_preferences'] = notification_preferences
        else:
            raise RequiredFieldMissing(
                "Dictionary with key 'frequency' is required"
            )

        response = self._requester.request(
            'PUT',
            'users/%s/communication_channels/%s/notification_preferences/%s' % (
                self.user_id,
                self.id,
                notification
            ),
            **combine_kwargs(**kwargs)
        )

        return response.json()
