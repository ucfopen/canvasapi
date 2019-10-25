from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject


@python_2_unicode_compatible
class GradeChangeEvent(CanvasObject):
    def __str__(self):
        return "{} {} - {} ({})".format(
            self.event_type, self.grade_before, self.grade_after, self.id
        )
