from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject


@python_2_unicode_compatible
class CourseEpubExport(CanvasObject):
    def __str__(self):
        return "{} course_id:({}) epub_id:({}) {} ".format(
            self.name,
            self.id,
            self.epub_export["id"],
            self.epub_export["workflow_state"],
        )
