from canvas_object import CanvasObject
from util import combine_kwargs


class Quiz(CanvasObject):

    def __str__(self):
        return "id %s, title: %s" % (
            self.id,
            self.title
        )

    def edit(self, course_id, **kwargs):
        """
        Modify this quiz.

        :calls: `PUT /api/v1/courses/:course_id/quizzes/:id \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.update>`_

        :returns: The updated quiz.
        :rtype: :class:`pycanvas.quiz.Quiz`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/quizzes/%s' % (course_id, self.id),
            **combine_kwargs(**kwargs)
        )
        return Quiz(self._requester, response.json())

    def delete(self, course_id, **kwargs):
        """
        Delete this quiz.

        :calls: `DELETE /api/v1/courses/:course_id/quizzes/:id \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.destroy>`_

        :rtype: :class:`pycanvas.quiz.Quiz`
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s/quizzes/%s' % (course_id, self.id),
            **combine_kwargs(**kwargs)
        )
        return Quiz(self._requester, response.json())
