from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class Assignment(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def delete(self):
        """
        Delete this assignment.

        :calls: `DELETE /api/v1/courses/:course_id/assignments/:id \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments.destroy>`_

        :rtype: :class:`canvasapi.assignment.Assignment`
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

        :rtype: :class:`canvasapi.assignment.Assignment`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/assignments/%s' % (self.course_id, self.id),
            **combine_kwargs(**kwargs)
        )

        if 'name' in response.json():
            super(Assignment, self).set_attributes(response.json())

        return Assignment(self._requester, response.json())


class AssignmentGroup(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def edit(self, **kwargs):
        """
        Modify this assignment group.

        :calls: `PUT /api/v1/courses/:course_id/assignment_groups/:assignment_group_id \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.update>`_

        :rtype: :class:`canvasapi.assignment.AssignmentGroup`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/assignment_groups/%s' % (self.course_id, self.id),
            **combine_kwargs(**kwargs)
        )

        if 'name' in response.json():
            super(AssignmentGroup, self).set_attributes(response.json())

        return AssignmentGroup(self._requester, response.json())

    def delete(self, **kwargs):
        """
        Delete this assignment.

        :calls: `DELETE /api/v1/courses/:course_id/assignment_groups/:assignment_group_id \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.destroy>`_

        :rtype: :class:`canvasapi.assignment.AssignmentGroup`
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s/assignment_groups/%s' % (self.course_id, self.id),
            **combine_kwargs(**kwargs)
        )
        return AssignmentGroup(self._requester, response.json())
