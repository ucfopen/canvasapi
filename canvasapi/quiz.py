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

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/groups \
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
            'courses/{}/quizzes/{}/questions/{}'.format(
                self.course_id,
                self.id,
                question_id
            ),
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

    def set_extensions(self, quiz_extensions, **kwargs):
        """
        Set extensions for student quiz submissions.

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/extensions
            <https://canvas.instructure.com/doc/api/quiz_extensions.html#method.quizzes/quiz_extensions.create>`_

        :param quiz_extensions: List of dictionaries representing extensions.
        :type quiz_extensions: list

        :rtype: list of :class:`canvasapi.quiz.QuizExtension`

        Example Usage:

        >>> quiz.set_extensions([
        ...     {
        ...         'user_id': 1,
        ...         'extra_time': 60,
        ...         'extra_attempts': 1
        ...     },
        ...     {
        ...         'user_id': 2,
        ...         'extra_attempts': 3
        ...     },
        ...     {
        ...         'user_id': 3,
        ...         'extra_time': 20
        ...     }
        ... ])
        """

        if not isinstance(quiz_extensions, list) or not quiz_extensions:
            raise ValueError('Param `quiz_extensions` must be a non-empty list.')

        if any(not isinstance(extension, dict) for extension in quiz_extensions):
            raise ValueError('Param `quiz_extensions` must only contain dictionaries')

        if any('user_id' not in extension for extension in quiz_extensions):
            raise RequiredFieldMissing(
                'Dictionaries in `quiz_extensions` must contain key `user_id`'
            )

        kwargs['quiz_extensions'] = quiz_extensions

        response = self._requester.request(
            'POST',
            'courses/{}/quizzes/{}/extensions'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        extension_list = response.json()['quiz_extensions']
        return [QuizExtension(self._requester, extension) for extension in extension_list]

    def get_all_quiz_submissions(self, **kwargs):
        """
        Get a list of all submissions for this quiz.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions \
        <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.index>`_

        :rtype: list of :class:`canvasapi.quiz.QuizSubmission`
        """
        response = self._requester.request(
            'GET',
            'courses/{}/quizzes/{}/submissions'.format(
                self.course_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        submission_list = response.json()['quiz_submissions']

        return [QuizSubmission(self._requester, submission) for submission in submission_list]

    def get_quiz_submission(self, quiz_submission, **kwargs):
        """
        Get a single quiz submission.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id \
        <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.show>`_

        :param quiz_submission: The object or ID of the quiz submission to retrieve.
        :type quiz_submission: int, string, :class:`canvasapi.quiz.QuizSubmission`

        :rtype: :class:`canvasapi.quiz.QuizSubmission`
        """
        quiz_submission_id = obj_or_id(quiz_submission, "quiz_submission", (QuizSubmission,))

        response = self._requester.request(
            'GET',
            'courses/{}/quizzes/{}/submissions/{}'.format(
                self.course_id,
                self.id,
                quiz_submission_id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )

        response_json = response.json()["quiz_submissions"][0]
        response_json.update({'course_id': self.course_id})

        return QuizSubmission(self._requester, response_json)

    def create_submission(self, **kwargs):
        """
        Start taking a Quiz by creating a QuizSubmission can be used to answer
        questions and submit answers.

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/submissions \
        <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.create>`_

        :rtype: :class:`canvasapi.quiz.QuizSubmission`
        """
        response = self._requester.request(
            'POST',
            'courses/{}/quizzes/{}/submissions'.format(
                self.course_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )

        response_json = response.json()["quiz_submissions"][0]
        response_json.update({'course_id': self.course_id})

        return QuizSubmission(self._requester, response_json)


@python_2_unicode_compatible
class QuizSubmission(CanvasObject):

    def __str__(self):
        return "{}-{}".format(self.quiz_id, self.user_id)

    def complete(self, **kwargs):
        """
        Complete the quiz submission by marking it as complete and grading it. When the quiz
        submission has been marked as complete, no further modifications will be allowed.

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/complete \
        <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.complete>`_

        :rtype: :class:`canvasapi.quiz.QuizSubmission`
        """
        if 'attempt' in kwargs:
            raise ValueError("Key `attempt` provided by Canvas, should not be set.")

        if 'validation_token' in kwargs:
            raise ValueError("Key `validation_token` provided by Canvas, should not be set.")

        kwargs['attempt'] = self.attempt
        kwargs['validation_token'] = self.validation_token

        response = self._requester.request(
            'POST',
            'courses/{}/quizzes/{}/submissions/{}/complete'.format(
                self.course_id,
                self.quiz_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )

        response_json = response.json()["quiz_submissions"][0]
        return QuizSubmission(self._requester, response_json)

    def get_times(self, **kwargs):
        """
        Get the current timing data for the quiz attempt, both the end_at timestamp and the
        time_left parameter.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/time \
        <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.time>`_

        :rtype: dict
        """
        if 'attempt' in kwargs:
            raise ValueError("Key `attempt` provided by Canvas, should not be set.")

        response = self._requester.request(
            'GET',
            'courses/{}/quizzes/{}/submissions/{}/time'.format(
                self.course_id,
                self.quiz_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )

        return response.json()

    def update_score_and_comments(self, **kwargs):
        """
        Update the amount of points a student has scored for questions they've answered, provide
        comments for the student about their answer(s), or simply fudge the total score by a
        specific amount of points.

        :calls: `PUT /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id \
        <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.update>`_

        :returns: The updated quiz.
        :rtype: :class:`canvasapi.quiz.QuizSubmission`
        """
        response = self._requester.request(
            'PUT',
            'courses/{}/quizzes/{}/submissions/{}'.format(
                self.course_id,
                self.quiz_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()["quiz_submissions"][0]

        return QuizSubmission(self._requester, response_json)


@python_2_unicode_compatible
class QuizExtension(CanvasObject):

    def __str__(self):
        return "{}-{}".format(self.quiz_id, self.user_id)


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
