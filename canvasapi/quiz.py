from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.paginated_list import PaginatedList
from canvasapi.quiz_group import QuizGroup
from canvasapi.submission import Submission
from canvasapi.user import User
from canvasapi.util import combine_kwargs, obj_or_id


class Quiz(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)

    def broadcast_message(self, conversations, **kwargs):
        """
        Send a message to unsubmitted or submitted users for the quiz.

        :calls: `POST /api/v1/courses/:course_id/quizzes/:id/submission_users/message \
        <https://canvas.instructure.com/doc/api/quiz_submission_user_list.html#method.quizzes/quiz_submission_users.message>`_

        :param conversations: A dictionary representing a Conversation.
            Requires `'body'`, `'recipients'`, and `'subject'` keys.
        :type conversations: dict

        :returns: True if the message was created, False otherwize
        :rtype: bool
        """

        required_key_list = ["body", "recipients", "subject"]
        required_keys_present = all((x in conversations for x in required_key_list))

        if isinstance(conversations, dict) and required_keys_present:
            kwargs["conversations"] = conversations
        else:
            raise RequiredFieldMissing(
                (
                    "conversations must be a dictionary with keys "
                    "'body', 'recipients', and 'subject'."
                )
            )

        response = self._requester.request(
            "POST",
            "courses/{}/quizzes/{}/submission_users/message".format(
                self.course_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.status_code == 201

    def create_question(self, **kwargs):
        """
        Create a new quiz question for this quiz.

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/questions \
        <https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.create>`_

        :rtype: :class:`canvasapi.quiz.QuizQuestion`
        """

        response = self._requester.request(
            "POST",
            "courses/{}/quizzes/{}/questions".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return QuizQuestion(self._requester, response_json)

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

        param_list = [
            "name",
            "pick_count",
            "question_points",
            "assessment_question_bank_id",
        ]
        if not any(param in quiz_groups[0] for param in param_list):
            raise RequiredFieldMissing("quiz_groups must contain at least 1 parameter.")

        kwargs["quiz_groups"] = quiz_groups

        response = self._requester.request(
            "POST",
            "courses/{}/quizzes/{}/groups".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json["quiz_groups"][0].update({"course_id": self.id})

        return QuizGroup(self._requester, response_json.get("quiz_groups")[0])

    def create_report(self, report_type, **kwargs):
        """
        Create and return a new report for this quiz. If a previously generated report
        matches the arguments and is still current (i.e. there have been no new submissions),
        it will be returned.

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/reports \
        <https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.create>`_

        :param report_type: The type of report, either student_analysis or item_analysis
        :type report_type: str

        :returns: `QuizReport` object
        :rtype: :class:`canvasapi.quiz.QuizReport`
        """
        if report_type not in ["student_analysis", "item_analysis"]:
            raise ValueError(
                "Param `report_type` must be a either 'student_analysis' or 'item_analysis'"
            )

        kwargs["quiz_report"] = {"report_type": report_type}

        response = self._requester.request(
            "POST",
            "courses/{}/quizzes/{}/reports".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return QuizReport(self._requester, response_json)

    def create_submission(self, **kwargs):
        """
        Start taking a Quiz by creating a QuizSubmission can be used to answer
        questions and submit answers.

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/submissions \
        <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.create>`_

        :rtype: :class:`canvasapi.quiz.QuizSubmission`
        """
        response = self._requester.request(
            "POST",
            "courses/{}/quizzes/{}/submissions".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()["quiz_submissions"][0]
        response_json.update({"course_id": self.course_id})

        return QuizSubmission(self._requester, response_json)

    def delete(self, **kwargs):
        """
        Delete this quiz.

        :calls: `DELETE /api/v1/courses/:course_id/quizzes/:id \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.destroy>`_

        :rtype: :class:`canvasapi.quiz.Quiz`
        """
        response = self._requester.request(
            "DELETE",
            "courses/{}/quizzes/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        quiz_json = response.json()
        quiz_json.update({"course_id": self.course_id})

        return Quiz(self._requester, quiz_json)

    def edit(self, **kwargs):
        """
        Modify this quiz.

        :calls: `PUT /api/v1/courses/:course_id/quizzes/:id \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.update>`_

        :returns: The updated quiz.
        :rtype: :class:`canvasapi.quiz.Quiz`
        """
        response = self._requester.request(
            "PUT",
            "courses/{}/quizzes/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        quiz_json = response.json()
        quiz_json.update({"course_id": self.course_id})

        return Quiz(self._requester, quiz_json)

    def get_all_quiz_reports(self, **kwargs):
        """
        Get a list of all quiz reports for this quiz

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/reports \
        <https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.quiz.QuizReport`
        """
        return PaginatedList(
            QuizReport,
            self._requester,
            "GET",
            "courses/{}/quizzes/{}/reports".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

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
            "GET",
            "courses/{}/quizzes/{}/questions/{}".format(
                self.course_id, self.id, question_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"course_id": self.course_id})

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
            "GET",
            "courses/{}/quizzes/{}/questions".format(self.course_id, self.id),
            {"course_id": self.course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

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
            "GET",
            "courses/{}/quizzes/{}/groups/{}".format(self.course_id, self.id, id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return QuizGroup(self._requester, response_json)

    def get_quiz_report(self, id, **kwargs):
        """
        Returns the data for a single quiz report.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/reports/:id \
        <https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.show>`_

        :param id: The ID of the quiz report you want to retrieve, or the report object
        :type id: int or :class:`canvasapi.quiz.QuizReport`

        :returns: `QuizReport` object
        :rtype: :class:`canvasapi.quiz.QuizReport`
        """
        id = obj_or_id(id, "id", (QuizReport,))

        response = self._requester.request(
            "GET",
            "courses/{}/quizzes/{}/reports/{}".format(self.course_id, self.id, id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return QuizReport(self._requester, response_json)

    def get_quiz_submission(self, quiz_submission, **kwargs):
        """
        Get a single quiz submission.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id \
        <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.show>`_

        :param quiz_submission: The object or ID of the quiz submission to retrieve.
        :type quiz_submission: int, string, :class:`canvasapi.quiz.QuizSubmission`

        :rtype: :class:`canvasapi.quiz.QuizSubmission`
        """
        quiz_submission_id = obj_or_id(
            quiz_submission, "quiz_submission", (QuizSubmission,)
        )

        response = self._requester.request(
            "GET",
            "courses/{}/quizzes/{}/submissions/{}".format(
                self.course_id, self.id, quiz_submission_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()["quiz_submissions"][0]
        response_json.update({"course_id": self.course_id})
        if len(response.json().get("quizzes", [])) > 0:
            response_json.update(
                {"quiz": Quiz(self._requester, response.json()["quizzes"][0])}
            )
        if len(response.json().get("submissions", [])) > 0:
            response_json.update(
                {
                    "submission": Submission(
                        self._requester, response.json()["submissions"][0]
                    )
                }
            )
        if len(response.json().get("users", [])) > 0:
            response_json.update(
                {"user": User(self._requester, response.json()["users"][0])}
            )

        return QuizSubmission(self._requester, response_json)

    def get_statistics(self, **kwargs):
        """
        Get statistics for for all quiz versions, or the latest quiz version.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/statistics \
        <https://canvas.instructure.com/doc/api/quiz_statistics.html#method.quizzes/quiz_statistics.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.quiz.QuizStatistic`
        """
        return PaginatedList(
            QuizStatistic,
            self._requester,
            "GET",
            "courses/{}/quizzes/{}/statistics".format(self.course_id, self.id),
            {"course_id": self.course_id},
            _root="quiz_statistics",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_submissions(self, **kwargs):
        """
        Get a list of all submissions for this quiz.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions \
        <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.quiz.QuizSubmission`
        """
        return PaginatedList(
            QuizSubmission,
            self._requester,
            "GET",
            "courses/{}/quizzes/{}/submissions".format(self.course_id, self.id),
            {"course_id": self.course_id},
            _root="quiz_submissions",
            _kwargs=combine_kwargs(**kwargs),
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
            raise ValueError("Param `quiz_extensions` must be a non-empty list.")

        if any(not isinstance(extension, dict) for extension in quiz_extensions):
            raise ValueError("Param `quiz_extensions` must only contain dictionaries")

        if any("user_id" not in extension for extension in quiz_extensions):
            raise RequiredFieldMissing(
                "Dictionaries in `quiz_extensions` must contain key `user_id`"
            )

        kwargs["quiz_extensions"] = quiz_extensions

        response = self._requester.request(
            "POST",
            "courses/{}/quizzes/{}/extensions".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        extension_list = response.json()["quiz_extensions"]
        return [
            QuizExtension(self._requester, extension) for extension in extension_list
        ]


class QuizStatistic(CanvasObject):
    def __str__(self):
        return "Quiz Statistic {}".format(self.id)


class QuizSubmission(CanvasObject):
    def __str__(self):
        return "Quiz {} - User {} ({})".format(self.quiz_id, self.user_id, self.id)

    def answer_submission_questions(self, validation_token=None, **kwargs):
        """
        Provide or update an answer to one or more quiz questions.

        :calls: `POST /api/v1/quiz_submissions/:quiz_submission_id/questions \
        <https://canvas.instructure.com/doc/api/quiz_submission_questions.html#method.quizzes/quiz_submission_questions.answer>`_

        :param validation_token: (Optional) The unique validation token for this quiz submission.
            If one is not provided, canvasapi will attempt to use `self.validation_token`.
        :type validation_token: str
        :returns: A list of quiz submission questions.
        :rtype: list of :class:`canvasapi.quiz.QuizSubmissionQuestion`
        """
        try:
            kwargs["validation_token"] = validation_token or self.validation_token
        except AttributeError:
            raise RequiredFieldMissing(
                "`validation_token` not set on this QuizSubmission, must be passed"
                " as a function argument."
            )

        # Only the latest attempt for a quiz submission can be updated, and Canvas
        # automatically returns the latest attempt with every quiz submission response,
        # so we can just use that.
        kwargs["attempt"] = self.attempt

        response = self._requester.request(
            "POST",
            "quiz_submissions/{}/questions".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        questions = list()
        for question in response.json().get("quiz_submission_questions", []):
            question.update(
                {
                    "quiz_submission_id": self.id,
                    "validation_token": kwargs["validation_token"],
                    "attempt": self.attempt,
                }
            )
            questions.append(QuizSubmissionQuestion(self._requester, question))

        return questions

    def complete(self, validation_token=None, **kwargs):
        """
        Complete the quiz submission by marking it as complete and grading it. When the quiz
        submission has been marked as complete, no further modifications will be allowed.


        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/complete \
        <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.complete>`_

        :param validation_token: (Optional) The unique validation token for this quiz submission.
            If one is not provided, canvasapi will attempt to use `self.validation_token`.
        :type validation_token: str
        :rtype: :class:`canvasapi.quiz.QuizSubmission`
        """
        try:
            kwargs["validation_token"] = validation_token or self.validation_token
        except AttributeError:
            raise RequiredFieldMissing(
                "`validation_token` not set on this QuizSubmission, must be passed"
                " as a function argument."
            )

        # Only the latest attempt for a quiz submission can be updated, and Canvas
        # automatically returns the latest attempt with every quiz submission response,
        # so we can just use that.
        kwargs["attempt"] = self.attempt

        response = self._requester.request(
            "POST",
            "courses/{}/quizzes/{}/submissions/{}/complete".format(
                self.course_id, self.quiz_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()["quiz_submissions"][0]
        return QuizSubmission(self._requester, response_json)

    def get_submission_events(self, **kwargs):
        """
        Retrieve the set of events captured during a specific submission attempt.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/events \
        <https://canvas.instructure.com/doc/api/quiz_submission_events.html#method.quizzes/quiz_submission_events_api.index>`_

        :returns: list of QuizSubmissionEvents.
        :rtype: list
        """
        response = self._requester.request(
            "GET",
            "courses/{}/quizzes/{}/submissions/{}/events".format(
                self.course_id, self.quiz_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        events = response.json()["quiz_submission_events"]

        return [QuizSubmissionEvent(self._requester, event) for event in events]

    def get_submission_questions(self, **kwargs):
        """
        Get a list of all the question records for this quiz submission.

        :calls: `GET /api/v1/quiz_submissions/:quiz_submission_id/questions \
        <https://canvas.instructure.com/doc/api/quiz_submission_questions.html#method.quizzes/quiz_submission_questions.index>`_

        :returns: A list of quiz submission questions.
        :rtype: list of :class:`canvasapi.quiz.QuizSubmissionQuestion`
        """
        response = self._requester.request(
            "GET",
            "quiz_submissions/{}/questions".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        questions = list()
        for question in response.json().get("quiz_submission_questions", []):
            question.update({"quiz_submission_id": self.id, "attempt": self.attempt})
            questions.append(QuizSubmissionQuestion(self._requester, question))

        return questions

    def get_times(self, **kwargs):
        """
        Get the current timing data for the quiz attempt, both the end_at timestamp and the
        time_left parameter.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/time \
        <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.time>`_

        :rtype: dict
        """
        response = self._requester.request(
            "GET",
            "courses/{}/quizzes/{}/submissions/{}/time".format(
                self.course_id, self.quiz_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()

    def submit_events(self, quiz_submission_events, **kwargs):
        """
        Store a set of events which were captured during a quiz taking session.

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/events \
        <https://canvas.instructure.com/doc/api/quiz_submission_events.html#method.quizzes/quiz_submission_events_api.create>`_

        :param quiz_submission_events: The submission events to be recorded.
        :type quiz_submission_events: list

        :returns: True if the submission was successful, false otherwise.
        :rtype: bool
        """
        if isinstance(quiz_submission_events, list) and isinstance(
            quiz_submission_events[0], QuizSubmissionEvent
        ):
            kwargs["quiz_submission_events"] = quiz_submission_events
        else:
            raise RequiredFieldMissing(
                "Required parameter quiz_submission_events missing."
            )

        response = self._requester.request(
            "POST",
            "courses/{}/quizzes/{}/submissions/{}/events".format(
                self.course_id, self.quiz_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.status_code == 204

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
            "PUT",
            "courses/{}/quizzes/{}/submissions/{}".format(
                self.course_id, self.quiz_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()["quiz_submissions"][0]
        response_json.update({"course_id": self.course_id})

        return QuizSubmission(self._requester, response_json)


class QuizExtension(CanvasObject):
    def __str__(self):
        return "{}-{}".format(self.quiz_id, self.user_id)


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
            "DELETE",
            "courses/{}/quizzes/{}/questions/{}".format(
                self.course_id, self.quiz_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
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
            "PUT",
            "courses/{}/quizzes/{}/questions/{}".format(
                self.course_id, self.quiz_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        super(QuizQuestion, self).set_attributes(response_json)
        return self


class QuizReport(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.report_type, self.id)

    def abort_or_delete(self, **kwargs):
        """
        This API allows you to cancel a previous request you issued for a report to be generated.
        Or in the case of an already generated report, you'd like to remove it, perhaps to generate
        it another time with an updated version that provides new features.

        :calls: `DELETE /api/v1/courses/:course_id/quizzes/:quiz_id/reports/:id \
        <https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.abort>`_

        :returns: True if attempt was successful; False otherwise
        :rtype: bool
        """
        response = self._requester.request(
            "DELETE",
            "courses/{}/quizzes/{}/reports/{}".format(
                self.course_id, self.quiz_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.status_code == 204


class QuizSubmissionEvent(CanvasObject):
    def __str__(self):
        return "{}".format(self.event_type)


class QuizSubmissionQuestion(CanvasObject):
    def __str__(self):
        return "QuizSubmissionQuestion #{}".format(self.id)

    def flag(self, validation_token=None, **kwargs):
        """
        Set a flag on a quiz question to indicate that it should be returned to later.

        :calls: `PUT /api/v1/quiz_submissions/:quiz_submission_id/questions/:id/flag \
        <https://canvas.instructure.com/doc/api/quiz_submission_questions.html#method.quizzes/quiz_submission_questions.flag>`_

        :param validation_token: (Optional) The unique validation token for the quiz submission.
            If one is not provided, canvasapi will attempt to use `self.validation_token`.
        :type validation_token: str
        :returns: True if the question was successfully flagged, False otherwise.
        :rtype: bool
        """
        try:
            kwargs["validation_token"] = validation_token or self.validation_token
        except AttributeError:
            raise RequiredFieldMissing(
                "`validation_token` not set on this QuizSubmissionQuestion, must be passed"
                " as a function argument."
            )

        # Only the latest attempt for a quiz submission can be updated, and Canvas
        # automatically returns the latest attempt with every quiz submission response,
        # so we can just use that.
        kwargs["attempt"] = self.attempt

        response = self._requester.request(
            "PUT",
            "quiz_submissions/{}/questions/{}/flag".format(
                self.quiz_submission_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        question = response.json()["quiz_submission_questions"][0]
        question.update(
            {
                "validation_token": kwargs["validation_token"],
                "quiz_submission_id": self.quiz_submission_id,
            }
        )
        super(QuizSubmissionQuestion, self).set_attributes(question)

        return True

    def unflag(self, validation_token=None, **kwargs):
        """
        Remove a previously set flag on a quiz question.

        :calls: `PUT /api/v1/quiz_submissions/:quiz_submission_id/questions/:id/unflag \
        <https://canvas.instructure.com/doc/api/quiz_submission_questions.html#method.quizzes/quiz_submission_questions.unflag>`_

        :param validation_token: (Optional) The unique validation token for the quiz submission.
            If one is not provided, canvasapi will attempt to use `self.validation_token`.
        :type validation_token: str
        :returns: True if the question was successfully unflagged, False otherwise.
        :rtype: bool
        """
        try:
            kwargs["validation_token"] = validation_token or self.validation_token
        except AttributeError:
            raise RequiredFieldMissing(
                "`validation_token` not set on this QuizSubmissionQuestion, must be passed"
                " as a function argument."
            )

        # Only the latest attempt for a quiz submission can be updated, and Canvas
        # automatically returns the latest attempt with every quiz submission response,
        # so we can just use that.
        kwargs["attempt"] = self.attempt

        response = self._requester.request(
            "PUT",
            "quiz_submissions/{}/questions/{}/unflag".format(
                self.quiz_submission_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

        question = response.json()["quiz_submission_questions"][0]
        question.update(
            {
                "validation_token": kwargs["validation_token"],
                "quiz_submission_id": self.quiz_submission_id,
            }
        )
        super(QuizSubmissionQuestion, self).set_attributes(question)

        return True


class QuizAssignmentOverrideSet(CanvasObject):
    def __str__(self):
        return "Overrides for quiz_id {}".format(self.quiz_id)
