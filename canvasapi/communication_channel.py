from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.notification_preference import NotificationPreference
from canvasapi.util import combine_kwargs


@python_2_unicode_compatible
class CommunicationChannel(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.address, self.id)

    def list_preferences(self):
        """
        Fetch all preferences for the given communication channel.

        :calls: `GET
            /api/v1/users/:user_id/communication_channels/:communication_channel_id/ \
                notification_preferences \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.index>`_

        :rtype: `list`
        """
        response = self._requester.request(
            'GET',
            'users/{}/communication_channels/{}/notification_preferences'.format(
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
            /api/v1/users/:u_id/communication_channels/:communication_channel_id/ \
                notification_preference_categories \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.category_index>`_

        :rtype: `list`
        """
        response = self._requester.request(
            'GET',
            'users/{}/communication_channels/{}/notification_preference_categories'.format(
                self.user_id,
                self.id
            )
        )
        return response.json()['categories']

    def get_preference(self, notification):
        """
        Fetch the preference for the given notification for the given
        communication channel.

        :calls: `GET
            /api/v1/users/:u_id/communication_channels/:communication_channel_id/ \
                notification_preferences/:notification \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.show>`_

        :param notification: The name of the notification.
        :type notification: str
        :rtype: :class:`canvasapi.notification_preference.NotificationPreference`
        """
        response = self._requester.request(
            'GET',
            'users/{}/communication_channels/{}/notification_preferences/{}'.format(
                self.user_id,
                self.id,
                notification
            )
        )
        data = response.json()['notification_preferences'][0]
        return NotificationPreference(self._requester, data)

    def update_preference(self, notification, frequency, **kwargs):
        """
        Update the preference for the given notification for the given communication channel.

        :calls: `PUT
            /api/v1/users/:u_id/communication_channels/:communication_channel_id/ \
                notification_preferences/:notification \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.update>`_

        :param notification: The name of the notification.
        :type notification: str
        :param frequency: The desired frequency for this notification.
        :type frequency: str
            Can be 'immediately', 'daily', 'weekly', or 'never'

        :rtype: :class:`canvasapi.notification_preference.NotificationPreference`
        """
        kwargs['notification_preferences[frequency]'] = frequency
        response = self._requester.request(
            'PUT',
            'users/self/communication_channels/{}/notification_preferences/{}'.format(
                self.id,
                notification
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        data = response.json()['notification_preferences'][0]
        return NotificationPreference(self._requester, data)

    def update_preferences_by_catagory(self, category, frequency, **kwargs):
        """
        Change preferences for multiple notifications based on the category
        for a single communication channel.

        :calls: `PUT
            /api/v1/users/:u_id/communication_channels/:communication_channel_id/ \
                notification_preference_categories/:category \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.update_preferences_by_category>`_

        :param category: The name of the category. \
            Must be parameterized e.g. The category Course Content should be course_content
        :type category: str
        :param frequency: The desired frequency for this notification.
        :type frequency: str
            Can be 'immediately', 'daily', 'weekly', or 'never'

        :rtype: :class:`canvasapi.notification_preference.NotificationPreference`
        """
        kwargs['notification_preferences[frequency]'] = frequency
        response = self._requester.request(
            'PUT',
            'users/self/communication_channels/{}/notification_preference_categories/{}'.format(
                self.id,
                category
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        return response.json()['notification_preferences']

    def update_multiple_preferences(self, notification_preferences, **kwargs):
        """
        Change preferences for multiple notifications based on the category
        for a single communication channel.

        :calls: `PUT
            /api/v1/users/self/communication_channels/:communication_channel_id/ \
                notification_preferences \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.update_all>`_

        :param notification_preferences: Dict that indicates the frequency for \
            different notification types.
        :type notification: dict

        :rtype: :class:`canvasapi.notification_preference.NotificationPreference`
        """
        if isinstance(notification_preferences, dict) and notification_preferences:

            for key, value in notification_preferences.items():
                try:
                    if not value['frequency']:
                        return False
                except KeyError:
                    return False

            kwargs['notification_preferences'] = notification_preferences
            response = self._requester.request(
                'PUT',
                'users/self/communication_channels/{}/notification_preferences'.format(
                    self.id
                ),
                _kwargs=combine_kwargs(**kwargs)
            )
            return response.json()['notification_preferences']
        return False
