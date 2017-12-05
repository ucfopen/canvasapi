from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.util import combine_kwargs


@python_2_unicode_compatible
class QuizGroup(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def update(self, id, quiz_groups, **kwargs):
        """
        Update a question group given by id

        :calls: `PUT /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id \
        <https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.update>`

        :param id: The ID of the question group.
        :type int
        :param quiz_groups: The name, pick count, and/or question points.
        All of these parameters are optional, but at least one must exist
        (even if empty) to recieve a response.
        The request expects a list, but will only update 1 question group per request.
        :type list[dict]

        :returns: QuizGroup object
        :rtype: :class:`canvasapi.quiz_group.QuizGroup`
        """
        if not isinstance(quiz_groups, list) or len(quiz_groups) <= 0:
            raise ValueError("Param `quiz_groups` must be a non-empty list.")

        if not isinstance(quiz_groups[0], dict):
            raise ValueError("Param `quiz_groups` must contain a dictionary")

        if ("name" not in quiz_groups[0] and "pick_count" not in quiz_groups[0]
                and "question_points" not in quiz_groups[0]):
            raise RequiredFieldMissing("quiz_groups must contain at least 1 parameter.")

        kwargs["quiz_groups"] = quiz_groups

        response = self._requester.request(
            'PUT',
            'courses/{}/quizzes/{}/groups/{}'.format(self.course_id, self.quiz_id, id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return QuizGroup(self._requester, response.json().get('quiz_groups')[0])

    def delete(self, id):
        """
        Get details of the quiz group with the given id

        :calls: `DELETE /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id \
        <https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.destroy>`

        :param: id: The ID of the question group.
        :type: `int`

        :returns: True if the result was successful (Status code of 204)
        :rtype: `bool`
        """
        response = self._requester.request(
            'DELETE',
            'courses/{}/quizzes/{}/groups/{}'.format(self.course_id, self.quiz_id, id)
        )
        return (response.status_code == 204)

    def reorder_question_group(self, id, order, **kwargs):
        """
        Update the order of questions within a given group

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id/reorder \
        <https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.reorder>`

        :param: id: The ID of the question group.
        :type: int
        :param: order: A list of dictionaries containing the key 'id' of the
        question to be placed at order's index.
        :type: list[dict]

        :returns: True if the result was successful (Status code of 204)
        :rtype: `bool`
        """

        if not isinstance(order, list) or len(order) <= 0:
            raise ValueError("Param `order` must be a non-empty list.")

        for orderDict in order:
            if not isinstance(orderDict, dict):
                raise ValueError("order must consist of dictionaries.")
            if "id" not in orderDict:
                raise ValueError("Dictionaries in order must contain an 'id' key.")

        kwargs["order"] = order

        response = self._requester.request(
            'POST',
            'courses/{}/quizzes/{}/groups/{}/reorder'.format(self.course_id, self.quiz_id, id),
            _kwargs=combine_kwargs(**kwargs)
        )

        return (response.status_code == 204)
