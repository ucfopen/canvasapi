from canvas_object import CanvasObject
from util import combine_kwargs


class Assignment(CanvasObject):

    def __str__(self):
        return "id: %s, name: %s, description: %s" % (
            self.id,
            self.name,
            self.description
        )

    def delete(self):
        """
        Delete the given assignment.

        :calls: `DELETE /api/v1/courses/:course_id/assignments/:id`
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments.destroy>
        :rtype: Assignment
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s/assignments/%s' % (self.course_id, self.id),
        )
        return Assignment(self._requester, response.json())

    def edit(self, **kwargs):
        """
        Modify an existing assignment.
        :calls: `PUT /api/v1/courses/:course_id/assignments/:id`
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.update>
        :rtype: :class:`Assignment`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/assignments/%s' % (self.course_id, self.id),
            **combine_kwargs(**kwargs)
        )

        if 'name' in response.json():
            super(Assignment, self).set_attributes(response.json())

        return Assignment(self._requester, response.json())
