from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.util import combine_kwargs

@python_2_unicode_compatible
class GradingPeriod(CanvasObject):

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)

    def update(self, grading_period, **kwargs):
        """
        Update a grading period for a course.

        :calls: `PUT /api/v1/courses/:course_id/grading_periods/:id \
        <https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.update>`_

        :param grading_period: List of keys

        :rtype: :class:`canvasapi.grading_period.GradingPeriod`
        """
        if not hasattr(self, 'course_id'):
            raise ValueError('Can only update grading periods from a Course.')

        if isinstance(grading_period, list):
            kwargs['grading_period'] = grading_period
        else:
            raise RequiredFieldMissing("List is required")

        response = self._requester.request(
            'PUT',
            'courses/{}/grading_periods/{}'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update({'course_id': self.course_id})

        return GradingPeriod(self._requester, response_json['grading_periods'][0])
