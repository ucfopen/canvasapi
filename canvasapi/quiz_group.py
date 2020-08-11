from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.util import combine_kwargs


class QuizGroup(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def delete(self, id, **kwargs):
        """
        Get details of the quiz group with the given id.

        :calls: `DELETE /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id \
        <https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.destroy>`_

        :param id: The ID of the question group.
        :type id: int

        :returns: True if the result was successful (Status code of 204)
        :rtype: bool
        """
        response = self._requester.request(
            "DELETE",
            "courses/{}/quizzes/{}/groups/{}".format(self.course_id, self.quiz_id, id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.status_code == 204

    def reorder_question_group(self, id, order, **kwargs):
        """
        Update the order of questions within a given group

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id/reorder \
        <https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.reorder>`_

        :param id: The ID of the question group.
        :type id: int
        :param order: A list of dictionaries containing the key 'id' of
            the question to be placed at order's index.
        :type order: list[dict]

        :returns: True if the result was successful (Status code of 204)
        :rtype: bool
        """

        if not isinstance(order, list) or not order:
            raise ValueError("Param `order` must be a non-empty list.")

        for question in order:
            if not isinstance(question, dict):
                raise ValueError(
                    "`order` must consist only of dictionaries representing "
                    "Question items."
                )
            if "id" not in question:
                raise ValueError("Dictionaries in `order` must contain an `id` key.")

        kwargs["order"] = order

        response = self._requester.request(
            "POST",
            "courses/{}/quizzes/{}/groups/{}/reorder".format(
                self.course_id, self.quiz_id, id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.status_code == 204

    def update(self, id, quiz_groups, **kwargs):
        """
        Update a question group given by id.

        :calls: `PUT /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id \
        <https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.update>`_

        :param id: The ID of the question group.
        :type id: int
        :param quiz_groups: The name, pick count, and/or question points.
            All of these parameters are optional, but at least one must exist
            (even if empty) to recieve a response.
            The request expects a list, but will only update 1 question group per request.
        :type quiz_groups: list[dict]

        :returns: `True` if the QuizGroup was updated. `False` otherwise.
        :rtype: bool
        """
        if not isinstance(quiz_groups, list) or len(quiz_groups) <= 0:
            raise ValueError("Param `quiz_groups` must be a non-empty list.")

        if not isinstance(quiz_groups[0], dict):
            raise ValueError("Param `quiz_groups` must contain a dictionary")

        param_list = ["name", "pick_count", "question_points"]
        if not any(param in quiz_groups[0] for param in param_list):
            raise RequiredFieldMissing("quiz_groups must contain at least 1 parameter.")

        kwargs["quiz_groups"] = quiz_groups

        response = self._requester.request(
            "PUT",
            "courses/{}/quizzes/{}/groups/{}".format(self.course_id, self.quiz_id, id),
            _kwargs=combine_kwargs(**kwargs),
        )

        successful = "name" in response.json().get("quiz_groups")[0]
        if successful:
            super(QuizGroup, self).set_attributes(response.json().get("quiz_groups")[0])

        return successful
