import unittest
import settings
import requests_mock

from util import register_uris
from pycanvas.course import Course
from pycanvas.quiz import Quiz
from pycanvas.assignment import Assignment
from pycanvas.exceptions import ResourceDoesNotExist
from pycanvas import Canvas

INVALID_ID = 9001


class TestCourse(unittest.TestCase):
    """
    Tests Courses functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': [
                'create', 'get_by_id', 'get_quiz', 'list_quizzes', 'list_quizzes2',
                'create_assignment', 'get_assignment_by_id', 'get_all_assignments',
                'get_all_assignments2'
            ],
            'generic': ['not_found'],
            'quiz': ['get_by_id']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.course = self.canvas.get_course(1)
        self.quiz = self.course.get_quiz(1)

    # create_quiz()
    def test_create_quiz(self):
        title = 'Newer Title'
        new_quiz = self.course.create_quiz(self.course.id, quiz={'title': title})

        assert isinstance(new_quiz, Quiz)
        assert hasattr(new_quiz, 'title')
        assert new_quiz.title == title

    # get_quiz()
    def test_get_quiz(self):
        target_quiz = self.course.get_quiz(1)

        assert isinstance(target_quiz, Quiz)

    def test_get_quiz_fail(self):
        with self.assertRaises(ResourceDoesNotExist):
            self.course.get_quiz(INVALID_ID)

    # list_quizzes()
    def test_list_quizzes(self):
        quizzes = self.course.list_quizzes()
        quiz_list = [quiz for quiz in quizzes]

        assert len(quiz_list) == 4
        assert isinstance(quiz_list[0], Quiz)

    # create_assignment()
    def test_create_assignment(self):
        name = 'Newly Created Assignment'

        assignment_dict = {
            'name': name
        }

        assignment = self.course.create_assignment(assignment=assignment_dict)

        assert isinstance(assignment, Assignment)
        assert hasattr(assignment, 'name')
        assert assignment.name == name
        assert assignment.id == 5

    # get_assignment()
    def test_get_assignment(self):
        assignment = self.course.get_assignment('5')

        assert isinstance(assignment, Assignment)
        assert hasattr(assignment, 'name')

    # get_assignments()
    def test_get_assignments(self):
        assignments = self.course.get_assignments()
        assignment_list = [assignment for assignment in assignments]

        assert isinstance(assignments[0], Assignment)
        assert len(assignment_list) == 4
