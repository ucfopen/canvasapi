from __future__ import absolute_import, division, print_function, unicode_literals

import warnings

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.notification_preference import NotificationPreference
from canvasapi.util import combine_kwargs

@python_2_unicode_compatible
class Favorite(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.context_id, self.context_type)


