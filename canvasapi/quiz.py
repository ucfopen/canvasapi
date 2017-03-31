from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class Quiz(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.title, self.id)

    def edit(self, **kwargs):
        """
        Modify this quiz.

        :calls: `PUT /api/v1/courses/:course_id/quizzes/:id \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.update>`_

        :returns: The updated quiz.
        :rtype: :class:`canvasapi.quiz.Quiz`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/quizzes/%s' % (self.course_id, self.id),
            **combine_kwargs(**kwargs)
        )
        quiz_json = response.json()
        quiz_json.update({'course_id': self.course_id})

        return Quiz(self._requester, quiz_json)

    def delete(self, **kwargs):
        """
        Delete this quiz.

        :calls: `DELETE /api/v1/courses/:course_id/quizzes/:id \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.destroy>`_

        :rtype: :class:`canvasapi.quiz.Quiz`
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s/quizzes/%s' % (self.course_id, self.id),
            **combine_kwargs(**kwargs)
        )
        quiz_json = response.json()
        quiz_json.update({'course_id': self.course_id})

        return Quiz(self._requester, quiz_json)
