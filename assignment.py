from canvas_object import CanvasObject


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
            event="delete"
        )
        return response.json()
