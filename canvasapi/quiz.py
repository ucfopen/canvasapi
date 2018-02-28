from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.paginated_list import PaginatedList
from canvasapi.quiz_group import QuizGroup
from canvasapi.util import combine_kwargs, obj_or_id


@python_2_unicode_compatible
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
            'courses/{}/quizzes/{}'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
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
            'courses/{}/quizzes/{}'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        quiz_json = response.json()
        quiz_json.update({'course_id': self.course_id})

        return Quiz(self._requester, quiz_json)

    def get_quiz_group(self, id, **kwargs):
        """
        Get details of the quiz group with the given id

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id \
        <https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.show>`_


        :param id: The ID of the question group.
        :type id: int

        :returns: `QuizGroup` object
        :rtype: :class:`canvasapi.quiz_group.QuizGroup`
        """
        response = self._requester.request(
            'GET',
            'courses/{}/quizzes/{}/groups/{}'.format(self.course_id, self.id, id),
            _kwargs=combine_kwargs(**kwargs)
        )

        response_json = response.json()
        response_json.update({'course_id': self.id})

        return QuizGroup(self._requester, response_json)

    def create_question_group(self, quiz_groups, **kwargs):
        """
        Create a new question group for the given quiz id

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id \
        <https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.create>`_

        :param quiz_groups: The name, pick count, question points,
            and/or assessment question bank id.
            All of these parameters are optional, but at least one must exist
            (even if empty) to receive a response.
            The request expects a list, but will only create 1 question group per request.
        :type quiz_groups: list[dict]

        :returns: `QuizGroup` object
        :rtype: :class:`canvasapi.quiz_group.QuizGroup`
        """

        if not isinstance(quiz_groups, list) or not quiz_groups:
            raise ValueError("Param `quiz_groups` must be a non-empty list.")

        if not isinstance(quiz_groups[0], dict):
            raise ValueError("Param `quiz_groups must contain a dictionary")

        param_list = ['name', 'pick_count', 'question_points', 'assessment_question_bank_id']
        if not any(param in quiz_groups[0] for param in param_list):
            raise RequiredFieldMissing("quiz_groups must contain at least 1 parameter.")

        kwargs["quiz_groups"] = quiz_groups

        response = self._requester.request(
            'POST',
            'courses/{}/quizzes/{}/groups'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        response_json = response.json()
        response_json['quiz_groups'][0].update({'course_id': self.id})

        return QuizGroup(self._requester, response_json.get('quiz_groups')[0])

    def create_question(self, **kwargs):
        """
        Create a new quiz question for this quiz.

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/questions \
        <https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.create>`_

        :rtype: :class:`canvasapi.quiz.QuizQuestion`
        """

        response = self._requester.request(
            'POST',
            'courses/{}/quizzes/{}/questions'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update({'course_id': self.course_id})

        return QuizQuestion(self._requester, response_json)

    def get_question(self, question, **kwargs):
        """
        Get as single quiz question by ID.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id \
        <https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.show>`_

        :param question: The object or ID of the quiz question to retrieve.
        :type question: int, str or :class:`canvasapi.quiz.QuizQuestion`

        :rtype: :class:`canvasapi.quiz.QuizQuestion`
        """
        question_id = obj_or_id(question, "question", (QuizQuestion,))

        response = self._requester.request(
            'GET',
            'courses/{}/quizzes/{}/questions/{}'.format(self.course_id, self.id, question_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update({'course_id': self.course_id})

        return QuizQuestion(self._requester, response_json)

    def get_questions(self, **kwargs):
        """
        List all questions for a quiz.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/questions \
        <https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.quiz.QuizQuestion`
        """
        return PaginatedList(
            QuizQuestion,
            self._requester,
            'GET',
            'courses/{}/quizzes/{}/questions'.format(self.course_id, self.id),
            {'course_id': self.course_id},
            _kwargs=combine_kwargs(**kwargs)
        )


@python_2_unicode_compatible
class QuizQuestion(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.question_name, self.id)

    def delete(self, **kwargs):
        """
        Delete an existing quiz question.

        :calls: `DELETE /api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id \
        <https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.destroy>`_

        :returns: True if question was successfully deleted; False otherwise.
        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            'courses/{}/quizzes/{}/questions/{}'.format(
                self.course_id,
                self.quiz_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )

        return response.status_code == 204

    def edit(self, **kwargs):
        """
        Update an existing quiz question.

        :calls: `PUT /api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id \
        <https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.update>`_

        :rtype: :class:`canvasapi.quiz.QuizQuestion`
        """
        response = self._requester.request(
            'PUT',
            'courses/{}/quizzes/{}/questions/{}'.format(
                self.course_id,
                self.quiz_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update({'course_id': self.course_id})

        super(QuizQuestion, self).set_attributes(response_json)
        return self
