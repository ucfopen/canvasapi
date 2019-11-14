from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject


@python_2_unicode_compatible
class Day(CanvasObject):
    def __str__(self):
        return "{}".format(self.date)


@python_2_unicode_compatible
class Grader(CanvasObject):
    def __str__(self):
        return "{}".format(self.id)


@python_2_unicode_compatible
class SubmissionHistory(CanvasObject):
    def __str__(self):
        return "{}".format(self.submission_id)


@python_2_unicode_compatible
class SubmissionVersion(CanvasObject):
    def __str__(self):
        return "{} {}".format(self.assignment_id, self.id)
