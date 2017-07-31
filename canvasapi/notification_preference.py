from __future__ import absolute_import, division, print_function, unicode_literals

from canvasapi.canvas_object import CanvasObject


class NotificationPreference(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.notification, self.frequency)
