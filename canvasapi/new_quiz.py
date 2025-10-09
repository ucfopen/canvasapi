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
            _url="new_quizzes",
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return NewQuiz(self._requester, response_json)

    def set_accommodations(self, accommodations, **kwargs):
        """
        Apply accommodations at the quiz level for students in a specific assignment.

        :calls: `POST /api/quiz/v1/courses/:course_id/quizzes/:assignment_id/accommodations \
        <https://developerdocs.instructure.com/services/canvas/resources/new_quizzes_accommodations#method.new_quizzes-accommodation_api.quiz_level_accommodations>`_

        :param accommodations: A list of dictionaries containing accommodation details
            for each user. Each dictionary must contain `user_id` and can optionally include
            `extra_time`, `extra_attempts`, and/or `reduce_choices_enabled`.
        :type accommodations: list of dict

        :returns: AccommodationResponse object containing the status of the accommodation request.
        :rtype: :class:`canvasapi.new_quiz.AccommodationResponse`
        """
        endpoint = "courses/{}/quizzes/{}/accommodations".format(
            self.course_id, self.id
        )

        response = self._requester.request(
            "POST",
            endpoint,
            _url="new_quizzes",
            _kwargs=combine_kwargs(**kwargs),
            json=accommodations,
        )
        return AccommodationResponse(self._requester, response.json())

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
            _url="new_quizzes",
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return NewQuiz(self._requester, response_json)


class AccommodationResponse(CanvasObject):
    def __str__(self):
        return f"{self.message}"
