from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject


@python_2_unicode_compatible
class GradingPeriod(CanvasObject):

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)

    def update(self, **kwargs):
        """
        Update a grading period for a course.

        :calls: `PUT /api/v1/courses/:course_id/grading_periods/:id \
        <https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.update>`_

        :rtype: :class:`canvasapi.grading_period.GradingPeriod`
        """
