from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.util import combine_kwargs

@python_2_unicode_compatible
class GradingPeriod(CanvasObject):

    def __str__(self):
        return '{} ({})'.format(self.title, self.id)

    def update(self, course_id, grading_period, **kwargs):
        """
        Update a grading period for a course.

        :calls: `PUT /api/v1/courses/:course_id/grading_periods/:id \
        <https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.update>`_

        :param course_id: Id for course of grading period which is to be changed.
        :type course_id: int

        :param grading_period: List of nested paramameters which requires the start_date and end_date parameters.
        :type grading_period: list[dict]

        :rtype: :class:`canvasapi.grading_period.GradingPeriod`
        """
        if isinstance(grading_period, list):
            kwargs['grading_periods'] = grading_period
        else:
            raise RequiredFieldMissing("List is required")

        response = self._requester.request(
            'PUT',
            'courses/{}/grading_periods/{}'.format(course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        response_json = response.json()
        response_json.update({'course_id': course_id})

        return GradingPeriod(self._requester, response_json['grading_periods'][0])

    def delete(self, course_id, **kwargs):
        """
        Delete a grading period for a course.

        :calls: `DELETE /api/v1/courses/:course_id/grading_periods/:id \
        <https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.update>`_

        :param course_id: Id for course of grading period which is to be deleted.
        :type: int

        :returns: True if the grading period was deleted, False otherwise.
        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            'courses/{}/grading_periods/{}'.format(course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        response_json = response.json()

        return response.json().get('delete')
