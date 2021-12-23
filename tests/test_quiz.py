import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.paginated_list import PaginatedList
from canvasapi.quiz import (
    Quiz,
    QuizAssignmentOverrideSet,
    QuizExtension,
    QuizQuestion,
    QuizReport,
    QuizStatistic,
    QuizSubmission,
    QuizSubmissionEvent,
    QuizSubmissionQuestion,
)
from canvasapi.quiz_group import QuizGroup
from canvasapi.submission import Submission
from canvasapi.user import User
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestQuiz(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"course": ["get_by_id"], "quiz": ["get_by_id"]}, m)

            self.course = self.canvas.get_course(1)
            self.quiz = self.course.get_quiz(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.quiz)
        self.assertIsInstance(string, str)

    # broadcast_message()
    def test_broadcast_message(self, m):
        register_uris({"quiz": ["broadcast_message"]}, m)

        response = self.quiz.broadcast_message(
            conversations={
                "body": "please take the quiz",
                "recipients": "submitted",
                "subject": "ATTN: Quiz 101 Students",
            }
        )

        self.assertTrue(response)

    def test_broadcast_message_invalid_params(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.quiz.broadcast_message(
                conversations={"body": "no subject here", "recipients": "submitted"}
            )

    # edit()
    def test_edit(self, m):
        register_uris({"quiz": ["edit"]}, m)

        title = "New Title"
        edited_quiz = self.quiz.edit(quiz={"title": title})

        self.assertIsInstance(edited_quiz, Quiz)
        self.assertTrue(hasattr(edited_quiz, "title"))
        self.assertEqual(edited_quiz.title, title)
        self.assertTrue(hasattr(edited_quiz, "course_id"))
        self.assertEqual(edited_quiz.course_id, self.course.id)

    # delete()
    def test_delete(self, m):
        register_uris({"quiz": ["delete"]}, m)

        title = "Great Title"
        deleted_quiz = self.quiz.delete(quiz={"title": title})

        self.assertIsInstance(deleted_quiz, Quiz)
        self.assertTrue(hasattr(deleted_quiz, "title"))
        self.assertEqual(deleted_quiz.title, title)
        self.assertTrue(hasattr(deleted_quiz, "course_id"))
        self.assertEqual(deleted_quiz.course_id, self.course.id)

    # get_quiz_group()
    def test_get_quiz_group(self, m):
        register_uris({"quiz": ["get_by_id_5", "get_quiz_group"]}, m)

        quiz = self.course.get_quiz(5)

        result = quiz.get_quiz_group(10)
        self.assertIsInstance(result, QuizGroup)
        self.assertEqual(result.id, 10)
        self.assertEqual(result.quiz_id, 5)
        self.assertTrue(hasattr(result, "course_id"))
        self.assertEqual(result.course_id, 1)

    # create_question_group()
    def test_create_question_group(self, m):
        register_uris({"quiz": ["create_question_group"]}, m)

        quiz_group = [
            {
                "name": "Test Group",
                "pick_count": 1,
                "question_points": 2,
                "assessment_question_bank_id": 3,
            }
        ]
        result = self.quiz.create_question_group(quiz_group)

        self.assertIsInstance(result, QuizGroup)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.quiz_id, 1)
        self.assertEqual(result.name, quiz_group[0].get("name"))
        self.assertEqual(result.pick_count, quiz_group[0].get("pick_count"))
        self.assertEqual(result.question_points, quiz_group[0].get("question_points"))
        self.assertEqual(
            result.assessment_question_bank_id,
            quiz_group[0].get("assessment_question_bank_id"),
        )

    def test_create_question_group_empty_list(self, m):
        register_uris({"quiz": ["create_question_group"]}, m)

        quiz_group = []

        with self.assertRaises(ValueError):
            self.quiz.create_question_group(quiz_group)

    def test_create_question_group_incorrect_param(self, m):
        register_uris({"quiz": ["create_question_group"]}, m)

        quiz_group = [1]

        with self.assertRaises(ValueError):
            self.quiz.create_question_group(quiz_group)

    def test_create_question_group_incorrect_dict(self, m):
        register_uris({"quiz": ["create_question_group"]}, m)

        quiz_group = [{}]

        with self.assertRaises(RequiredFieldMissing):
            self.quiz.create_question_group(quiz_group)

    # create_question()
    def test_create_question(self, m):
        register_uris({"quiz": ["create_question"]}, m)

        question_dict = {
            "question_name": "Pick Correct Answer",
            "question_type": "multiple_choice_question",
            "question_text": "What is the right answer?",
            "points_possible": 10,
            "correct_comments": "That's correct!",
            "incorrect_comments": "That's wrong!",
        }
        question = self.quiz.create_question(question=question_dict)

        self.assertIsInstance(question, QuizQuestion)
        self.assertTrue(hasattr(question, "question_name"))
        self.assertEqual(question.question_name, question_dict["question_name"])

    # get_question()
    def test_get_question(self, m):
        register_uris({"quiz": ["get_question"]}, m)

        question_id = 1
        question = self.quiz.get_question(question_id)

        self.assertIsInstance(question, QuizQuestion)
        self.assertTrue(hasattr(question, "id"))
        self.assertEqual(question.id, question_id)
        self.assertTrue(hasattr(question, "question_name"))
        self.assertEqual(question.question_name, "Pick Correct Answer")

    # get_questions()
    def test_get_questions(self, m):
        register_uris({"quiz": ["get_questions"]}, m)

        questions = self.quiz.get_questions()
        question_list = [q for q in questions]

        self.assertEqual(len(question_list), 2)
        self.assertIsInstance(question_list[0], QuizQuestion)
        self.assertTrue(hasattr(question_list[0], "id"))
        self.assertEqual(question_list[0].id, 1)
        self.assertIsInstance(question_list[1], QuizQuestion)
        self.assertTrue(hasattr(question_list[1], "id"))
        self.assertEqual(question_list[1].id, 2)

    # set_extensions()
    def test_set_extensions(self, m):
        register_uris({"quiz": ["set_extensions"]}, m)

        extension = self.quiz.set_extensions(
            [{"user_id": 1, "extra_time": 60}, {"user_id": 2, "extra_attempts": 3}]
        )

        self.assertIsInstance(extension, list)
        self.assertEqual(len(extension), 2)

        self.assertIsInstance(extension[0], QuizExtension)
        self.assertEqual(extension[0].user_id, "1")
        self.assertTrue(hasattr(extension[0], "extra_time"))
        self.assertEqual(extension[0].extra_time, 60)

        self.assertIsInstance(extension[1], QuizExtension)
        self.assertEqual(extension[1].user_id, "2")
        self.assertTrue(hasattr(extension[1], "extra_attempts"))
        self.assertEqual(extension[1].extra_attempts, 3)

    def test_set_extensions_not_list(self, m):
        with self.assertRaises(ValueError):
            self.quiz.set_extensions({"user_id": 1, "extra_time": 60})

    def test_set_extensions_empty_list(self, m):
        with self.assertRaises(ValueError):
            self.quiz.set_extensions([])

    def test_set_extensions_non_dicts(self, m):
        with self.assertRaises(ValueError):
            self.quiz.set_extensions([("user_id", 1), ("extra_time", 60)])

    def test_set_extensions_missing_key(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.quiz.set_extensions([{"extra_time": 60, "extra_attempts": 3}])

    # get_all_quiz_reports
    def test_get_all_quiz_reports(self, m):
        register_uris({"quiz": ["get_all_quiz_reports"]}, m)

        reports = self.quiz.get_all_quiz_reports()
        self.assertIsInstance(reports, PaginatedList)

        reports = list(reports)

        for report in reports:
            self.assertIsInstance(report, QuizReport)
            self.assertTrue(hasattr(report, "report_type"))
            self.assertTrue(hasattr(report, "includes_all_versions"))

        self.assertEqual(len(reports), 2)

    # get_submissions()
    def test_get_submissions(self, m):
        register_uris({"quiz": ["get_all_quiz_submissions"]}, m)
        submissions = self.quiz.get_submissions()

        self.assertIsInstance(submissions, PaginatedList)

        submission_list = [sub for sub in submissions]

        self.assertEqual(len(submission_list), 2)

        self.assertIsInstance(submission_list[0], QuizSubmission)
        self.assertEqual(submission_list[0].id, 1)
        self.assertTrue(hasattr(submission_list[0], "attempt"))
        self.assertEqual(submission_list[0].attempt, 3)

        self.assertIsInstance(submission_list[1], QuizSubmission)
        self.assertEqual(submission_list[1].id, 2)
        self.assertTrue(hasattr(submission_list[1], "score"))
        self.assertEqual(submission_list[1].score, 5)

    # get_quiz_report
    def test_get_quiz_report(self, m):
        register_uris({"quiz": ["get_quiz_report"]}, m)

        report = self.quiz.get_quiz_report(1)
        self.assertIsInstance(report, QuizReport)
        self.assertEqual(report.quiz_id, 1)

    # get_quiz_report
    def test_get_statistics(self, m):
        register_uris({"quiz": ["get_statistics"]}, m)

        statistics = self.quiz.get_statistics()

        self.assertIsInstance(statistics, PaginatedList)

        statistic_list = [statistic for statistic in statistics]

        self.assertEqual(len(statistic_list), 1)
        self.assertIsInstance(statistic_list[0], QuizStatistic)
        self.assertEqual(statistic_list[0].id, "1")
        self.assertTrue(hasattr(statistic_list[0], "question_statistics"))
        self.assertEqual(len(statistic_list[0].question_statistics), 2)

    # get_quiz_submission
    def test_get_quiz_submission(self, m):
        register_uris({"quiz": ["get_quiz_submission"]}, m)

        quiz_id = 1
        quiz_submission = self.quiz.get_quiz_submission(
            quiz_id, include=["quiz", "submission", "user"]
        )

        self.assertIsInstance(quiz_submission, QuizSubmission)
        self.assertTrue(hasattr(quiz_submission, "id"))
        self.assertEqual(quiz_submission.quiz_id, quiz_id)
        self.assertTrue(hasattr(quiz_submission, "quiz_version"))
        self.assertEqual(quiz_submission.quiz_version, 1)
        self.assertTrue(hasattr(quiz_submission, "user_id"))
        self.assertEqual(quiz_submission.user_id, 1)
        self.assertTrue(hasattr(quiz_submission, "validation_token"))
        self.assertEqual(quiz_submission.validation_token, "this is a validation token")
        self.assertTrue(hasattr(quiz_submission, "score"))
        self.assertEqual(quiz_submission.score, 0)
        self.assertIsInstance(quiz_submission.quiz, Quiz)
        self.assertIsInstance(quiz_submission.submission, Submission)
        self.assertIsInstance(quiz_submission.user, User)

    # create_submission
    def test_create_submission(self, m):
        register_uris({"quiz": ["create_submission"]}, m)

        submission = self.quiz.create_submission()

        self.assertIsInstance(submission, QuizSubmission)

    def test_create_report(self, m):
        register_uris({"quiz": ["create_report"]}, m)

        report = self.quiz.create_report("student_analysis")

        self.assertIsInstance(report, QuizReport)
        self.assertEqual(report.report_type, "student_analysis")

    def test_create_report_failure(self, m):
        register_uris({"quiz": ["create_report"]}, m)

        with self.assertRaises(ValueError):
            self.quiz.create_report("super_cool_fake_report")


@requests_mock.Mocker()
class TestQuizReport(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "course": ["get_by_id"],
                "quiz": ["get_by_id", "get_quiz_report"],
            }
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.quiz = self.course.get_quiz(1)
            self.quiz_report = self.quiz.get_quiz_report(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.quiz_report)
        self.assertIsInstance(string, str)

    # abort_or_delete
    def test_abort_or_delete(self, m):
        register_uris({"quiz": ["abort_or_delete_report"]}, m)

        resp = self.quiz_report.abort_or_delete()

        self.assertEqual(resp, True)

    # abort_or_delete
    def test_abort_or_delete_failure(self, m):
        register_uris({"quiz": ["abort_or_delete_report_failure"]}, m)

        resp = self.quiz_report.abort_or_delete()

        self.assertEqual(resp, False)


@requests_mock.Mocker()
class TestQuizSubmission(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        self.submission = QuizSubmission(
            self.canvas._Canvas__requester,
            {
                "id": 1,
                "quiz_id": 1,
                "user_id": 1,
                "course_id": 1,
                "submission_id": 1,
                "attempt": 3,
                "validation_token": "this is a validation token",
                "manually_unlocked": None,
                "score": 7,
            },
        )

    # __str__()
    def test__str__(self, m):
        string = str(self.submission)
        self.assertIsInstance(string, str)

    # complete
    def test_complete(self, m):
        register_uris({"submission": ["complete"]}, m)

        submission = self.submission.complete()

        self.assertIsInstance(submission, QuizSubmission)
        self.assertTrue(hasattr(submission, "id"))
        self.assertTrue(hasattr(submission, "quiz_id"))
        self.assertTrue(hasattr(submission, "attempt"))
        self.assertTrue(hasattr(submission, "validation_token"))

    def test_complete_no_validation_token(self, m):
        del self.submission.validation_token

        with self.assertRaises(RequiredFieldMissing):
            self.submission.complete()

    # get_times
    def test_get_times(self, m):
        register_uris({"submission": ["get_times"]}, m)

        submission = self.submission.get_times()

        self.assertIsInstance(submission, dict)
        self.assertIn("end_at", submission)
        self.assertIn("time_left", submission)
        self.assertIsInstance(submission["time_left"], int)
        self.assertIsInstance(submission["end_at"], str)

    # update_score_and_comments
    def test_update_score_and_comments(self, m):
        register_uris({"submission": ["update_score_and_comments"]}, m)

        submission = self.submission.update_score_and_comments(
            quiz_submissions=[
                {
                    "attempt": 1,
                    "fudge_points": 1,
                    "questions": {
                        "question id 1": {"score": 1, "comment": "question 1 comment"},
                        "question id 2": {"score": 2, "comment": "question 2 comment"},
                        "question id 3": {"score": 3, "comment": "question 3 comment"},
                    },
                }
            ]
        )

        self.assertIsInstance(submission, QuizSubmission)
        self.assertTrue(hasattr(submission, "id"))
        self.assertTrue(hasattr(submission, "attempt"))
        self.assertTrue(hasattr(submission, "quiz_id"))
        self.assertTrue(hasattr(submission, "validation_token"))
        self.assertEqual(submission.score, 7)

    # get_submission_events
    def test_get_submission_events(self, m):
        register_uris({"quiz": ["get_submission_events"]}, m)

        events = self.submission.get_submission_events()
        self.assertIsInstance(events, PaginatedList)
        self.assertIsInstance(events[0], QuizSubmissionEvent)
        self.assertIsInstance(events[1], QuizSubmissionEvent)
        self.assertEqual(str(events[0]), "page_blurred")
        self.assertEqual(str(events[1]), "page_focused")

    # get_submission_questions
    def test_get_submission_questions(self, m):
        register_uris({"submission": ["get_submission_questions"]}, m)

        questions = self.submission.get_submission_questions()

        self.assertIsInstance(questions, list)
        self.assertIsInstance(questions[0], QuizSubmissionQuestion)
        self.assertTrue(hasattr(questions[0], "id"))
        self.assertTrue(hasattr(questions[0], "flagged"))

    # answer_submission_questions
    def test_answer_submission_questions(self, m):
        register_uris({"submission": ["answer_submission_questions"]}, m)

        answered_questions = self.submission.answer_submission_questions()

        self.assertIsInstance(answered_questions, list)
        self.assertIsInstance(answered_questions[0], QuizSubmissionQuestion)
        self.assertTrue(hasattr(answered_questions[0], "id"))
        self.assertTrue(hasattr(answered_questions[0], "flagged"))

    def test_answer_submission_questions_manual_validation_token(self, m):
        register_uris({"submission": ["answer_submission_questions"]}, m)

        del self.submission.validation_token

        answered_questions = self.submission.answer_submission_questions(
            validation_token="new validation token"
        )

        self.assertIsInstance(answered_questions, list)
        self.assertIsInstance(answered_questions[0], QuizSubmissionQuestion)
        self.assertTrue(hasattr(answered_questions[0], "id"))
        self.assertTrue(hasattr(answered_questions[0], "flagged"))

    def test_answer_submission_questions_no_validation_token(self, m):
        del self.submission.validation_token

        with self.assertRaises(RequiredFieldMissing):
            self.submission.answer_submission_questions()

    # submit_events()
    def test_submit_events(self, m):
        register_uris({"quiz": ["get_submission_events", "submit_events"]}, m)

        test_events = self.submission.get_submission_events()

        result = self.submission.submit_events(list(test_events))
        self.assertTrue(result)

    def test_submit_events_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.submission.submit_events([{}])


@requests_mock.Mocker()
class TestQuizExtension(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        self.extension = QuizExtension(
            self.canvas._Canvas__requester,
            {
                "user_id": 1,
                "quiz_id": 1,
                "extra_time": 60,
                "extra_attempts": 3,
                "manually_unlocked": None,
                "end_at": None,
            },
        )

    # __str__()
    def test__str__(self, m):
        string = str(self.extension)
        self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestQuizQuestion(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {"course": ["get_by_id"], "quiz": ["get_by_id", "get_question"]}, m
            )

            self.course = self.canvas.get_course(1)
            self.quiz = self.course.get_quiz(1)
            self.question = self.quiz.get_question(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.question)
        self.assertIsInstance(string, str)

    # delete()
    def test_delete(self, m):
        register_uris({"quiz": ["delete_question"]}, m)

        response = self.question.delete()
        self.assertTrue(response)

    # edit()
    def test_edit(self, m):
        register_uris({"quiz": ["edit_question"]}, m)

        question_dict = {
            "question_name": "Updated Question",
            "question_type": "multiple_choice_question",
            "question_text": "This question has been updated.",
            "points_possible": 100,
            "correct_comments": "Updated correct!",
            "incorrect_comments": "Updated wrong!",
        }

        self.assertEqual(self.question.question_name, "Pick Correct Answer")

        response = self.question.edit(question=question_dict)

        self.assertIsInstance(response, QuizQuestion)
        self.assertIsInstance(self.question, QuizQuestion)
        self.assertEqual(response.question_name, question_dict["question_name"])
        self.assertEqual(self.question.question_name, question_dict["question_name"])


@requests_mock.Mocker()
class TestQuizStatistic(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris(
                {"course": ["get_by_id"], "quiz": ["get_by_id", "get_statistics"]}, m
            )

            self.course = self.canvas.get_course(1)
            self.quiz = self.course.get_quiz(1)
            self.quiz_statistics = self.quiz.get_statistics()
            self.quiz_statistic = self.quiz_statistics[0]

    # __str__()
    def test__str__(self, m):
        string = str(self.quiz_statistic)
        self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestQuizSubmissionEvent(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        self.submission_event = QuizSubmissionEvent(
            self.canvas._Canvas__requester,
            {
                "client_timestamp": "2014-10-08T19:29:58Z",
                "event_type": "question_answered",
                "event_data": {"answer": "42"},
            },
        )

    # __str__()
    def test__str__(self, m):
        string = str(self.submission_event)
        self.assertIsInstance(string, str)


@requests_mock.Mocker()
class TestQuizSubmissionQuestion(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        self.submission_question = QuizSubmissionQuestion(
            self.canvas._Canvas__requester,
            {
                "id": 1,
                "flagged": None,
                "answer": None,
                "quiz_submission_id": 1,
                "validation_token": "this is a token",
                "attempt": 1,
            },
        )

    # __str__()
    def test__str__(self, m):
        string = str(self.submission_question)
        self.assertIsInstance(string, str)

    # flag()
    def test_flag(self, m):
        register_uris({"submission": ["flag_submission_question"]}, m)

        result = self.submission_question.flag()

        self.assertIsInstance(result, bool)
        self.assertTrue(result)
        self.assertTrue(self.submission_question.flagged)

    def test_flag_manual_validation_token(self, m):
        register_uris({"submission": ["flag_submission_question"]}, m)

        del self.submission_question.validation_token

        result = self.submission_question.flag(validation_token="new validation token")

        self.assertIsInstance(result, bool)
        self.assertTrue(result)
        self.assertTrue(self.submission_question.flagged)

    def test_flag_no_validation_token(self, m):
        del self.submission_question.validation_token

        with self.assertRaises(RequiredFieldMissing):
            self.submission_question.flag()

    # unflag()
    def test_unflag(self, m):
        register_uris({"submission": ["unflag_submission_question"]}, m)

        result = self.submission_question.unflag()

        self.assertIsInstance(result, bool)
        self.assertTrue(result)
        self.assertFalse(self.submission_question.flagged)

    def test_unflag_no_validation_token(self, m):
        del self.submission_question.validation_token

        with self.assertRaises(RequiredFieldMissing):
            self.submission_question.unflag()

    def test_unflag_manual_validation_token(self, m):
        register_uris({"submission": ["unflag_submission_question"]}, m)

        del self.submission_question.validation_token

        result = self.submission_question.unflag(
            validation_token="new validation token"
        )

        self.assertIsInstance(result, bool)
        self.assertTrue(result)
        self.assertFalse(self.submission_question.flagged)


@requests_mock.Mocker()
class TestQuizAssignmentOverrideSet(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        self.override_set = QuizAssignmentOverrideSet(
            self.canvas._Canvas__requester,
            {"quiz_id": "1", "due_dates": None, "all_dates": None},
        )

    # __str__()
    def test__str__(self, m):
        string = str(self.override_set)
        self.assertIsInstance(string, str)
