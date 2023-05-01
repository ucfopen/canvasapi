from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class NewQuiz(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)

    def delete(self, **kwargs):
        """
        Delete a single new quiz.

        :calls: `DELETE /api/quiz/v1/courses/:course_id/quizzes/:assignment_id \
        <https://canvas.instructure.com/doc/api/new_quizzes.html#method.new_quizzes/quizzes_api.destroy>`_

        :returns: The deleted New Quiz object
        :rtype: :class:`canvasapi.new_quiz.NewQuiz`
        """
        endpoint = "courses/{}/quizzes/{}".format(self.course_id, self.id)

        response = self._requester.request(
            "DELETE",
            endpoint,
            _url=self._requester.original_url + "/api/quiz/v1/" + endpoint,
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return NewQuiz(self._requester, response_json)

    def update(self, **kwargs):
        """
        Update a single New Quiz for the course.

        :calls: `PATCH /api/quiz/v1/courses/:course_id/quizzes/:assignment_id \
        <https://canvas.instructure.com/doc/api/new_quizzes.html#method.new_quizzes/quizzes_api.update>`_

        :returns: The updated New Quiz object
        :rtype: :class:`canvasapi.new_quiz.NewQuiz`
        """
        endpoint = "courses/{}/quizzes/{}".format(self.course_id, self.id)

        response = self._requester.request(
            "PATCH",
            endpoint,
            _url=self._requester.original_url + "/api/quiz/v1/" + endpoint,
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return NewQuiz(self._requester, response_json)
