from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import str

from canvasapi.canvas_object import CanvasObject


class Submission(CanvasObject):

    def __str__(self):
        return str(self.id)
