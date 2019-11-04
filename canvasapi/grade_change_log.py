from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject


@python_2_unicode_compatible
class GradeChangeLog(CanvasObject):
    def __init__(self, requester, attributes):
        """
        :param requester: The requester to pass HTTP requests through.
        :type requester: :class:`canvasapi.requester.Requester`
        :param attributes: The JSON object to build this object with.
        :type attributes: dict
        """
        super(GradeChangeLog, self).__init__(requester, attributes)

        self.events = [
            GradeChangeEvent(self._requester, event) for event in self.events
        ]

    def __str__(self):
        return "GradeChangeLog for {} ({})".format(self.context, self.context_id)


@python_2_unicode_compatible
class GradeChangeEvent(CanvasObject):
    def __str__(self):
        return "{} {} - {} ({})".format(
            self.event_type, self.grade_before, self.grade_after, self.id
        )
