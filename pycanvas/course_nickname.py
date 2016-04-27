from canvas_object import CanvasObject


class CourseNickname(CanvasObject):

    def __str__(self):
        return "course_id: %s, name: %s, nickname: %s, " % (
            self.course_id,
            self.name,
            self.nickname
        )

    def remove(self):
        """
        Remove the nickname for the given course. Subsequent course API
        calls will return the actual name for the course.

        .. :calls: `DELETE /api/v1/users/self/course_nicknames/:course_id
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.delete>`_

        :rtype: :class:`CourseNickname`
        """
        from course_nickname import CourseNickname

        response = self._requester.request(
            'DELETE',
            'users/self/course_nicknames/%s' % (self.course_id)
        )
        return CourseNickname(self._requester, response.json())
