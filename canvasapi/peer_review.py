from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject


@python_2_unicode_compatible
class PeerReview(CanvasObject):
    def __str__(self):
        return "{} {} ({})".format(self.asset_id, self.user_id, self.id)
