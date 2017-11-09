from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


@python_2_unicode_compatible
class NotificationPreference(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.notification, self.frequency)

    def update(self, frequency, **kwargs):
        """
        Update the preference for the given notification for the given communication channel.

        :calls: `PUT
            /api/v1/users/:u_id/communication_channels/:co_id/notification_preferences/:notif \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.update>`_

        :param frequency: The desired frequency for this notification.
        :type frequency: str
            Can be 'immediately', 'daily', 'weekly', or 'never'

        :rtype: :class:`canvasapi.notification_preference.NotificationPreference`
        """
        kwargs['notification_preferences[frequency]'] = frequency
        response = self._requester.request(
            'GET',
            'users/%s/communication_channels/%s/notification_preferences/%s' % (
                self.user_id,
                self.communication_channel,
                self.notification
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        data = response.json()['notification_preferences'][0]
        return NotificationPreference(self._requester, data)
