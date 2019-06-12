from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject


@python_2_unicode_compatible
class ContentExport(CanvasObject):
    def __str__(self):
        return "{} {} ({})".format(self.export_type, self.user_id, self.id)
