from __future__ import unicode_literals

from builtins import str

from canvasapi.canvas_object import CanvasObject


class Avatar(CanvasObject):

    def __str__(self):  # pragma: no cover
        return str(self.display_name)
