from canvas_object import CanvasObject
from util import combine_kwargs


class Assignment(CanvasObject):

    def __str__(self):  # pragma: no cover
        return "id: %s, name: %s, description: %s" % (
            self.id,
            self.name,
            self.description
        )

    def delete(self):
        """
        Delete this assignment.

        :calls: `DELETE /api/v1/courses/:course_id/assignments/:id \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments.destroy>`_

        :rtype: :class:`pycanvas.assignment.Assignment`
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s/assignments/%s' % (self.course_id, self.id),
        )
        return Assignment(self._requester, response.json())

    def edit(self, **kwargs):
        """
        Modify this assignment.

        :calls: `PUT /api/v1/courses/:course_id/assignments/:id \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.update>`_

        :rtype: :class:`pycanvas.assignment.Assignment`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/assignments/%s' % (self.course_id, self.id),
            **combine_kwargs(**kwargs)
        )

        if 'name' in response.json():
            super(Assignment, self).set_attributes(response.json())

        return Assignment(self._requester, response.json())
