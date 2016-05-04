import unittest
import settings
import requests

import requests_mock

from util import register_uris
from pycanvas import Canvas
from pycanvas.course import Course, CourseNickname
from pycanvas.enrollment import Enrollment
from pycanvas.exceptions import ResourceDoesNotExist
from pycanvas.quiz import Quiz
from pycanvas.user import User


class TestCourse(unittest.TestCase):
    """
    Tests core Courses functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': [
                'create', 'enroll_user', 'get_by_id', 'get_quiz',
                'get_recent_students', 'get_recent_students_p2', 'get_user',
                'get_user_id_type', 'get_users', 'get_users_p2', 'list_quizzes',
                'list_quizzes2', 'preview_html', 'reset', 'settings', 'update',
                'update_settings'
            ],
            'generic': ['not_found'],
            'quiz': ['get_by_id'],
            'user': ['get_by_id']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        # define custom matchers
        def conclude_matcher(request):
            if (request.path_url == '/api/v1/courses/1' and request.body and
                    'event=conclude' in request.body):
                resp = requests.Response()
                resp.status_code = 200
                resp._content = '{"conclude": true}'
                return resp

        def delete_matcher(request):
            if (request.path_url == '/api/v1/courses/1' and request.body and
                    'event=delete' in request.body):
                resp = requests.Response()
                resp.status_code = 200
                resp._content = '{"delete": true}'
                return resp

        # register custom matchers
        adapter.add_matcher(conclude_matcher)
        adapter.add_matcher(delete_matcher)

        self.course = self.canvas.get_course(1)
        self.quiz = self.course.get_quiz(1)

    # __str__()
    def test__str__(self):
        string = str(self.course)
        assert isinstance(string, str)

    # conclude()
    def test_conclude(self):
        success = self.course.conclude()
        assert success

    # delete()
    def test_delete(self):
        success = self.course.delete()
        assert success

    # update()
    def test_update(self):
        new_name = 'New Name'
        self.course.update(course={'name': new_name})
        assert self.course.name == new_name

    # get_user()
    def test_get_user(self):
        user = self.course.get_user(1)

        assert isinstance(user, User)
        assert hasattr(user, 'name')

    def test_get_user_id_type(self):
        user = self.course.get_user("ab123456", "sis_login_id")

        assert isinstance(user, User)
        assert hasattr(user, 'name')

    # get_users()
    def test_get_users(self):
        users = self.course.get_users()
        user_list = [user for user in users]

        assert len(user_list) == 4
        assert isinstance(user_list[0], User)

    # enroll_user()
    def test_enroll_user(self):
        enrollment_type = 'TeacherEnrollment'
        user = self.canvas.get_user(1)
        enrollment = self.course.enroll_user(user, enrollment_type)

        assert isinstance(enrollment, Enrollment)
        assert hasattr(enrollment, 'type')
        assert enrollment.type == enrollment_type

    # get_recent_students()
    def test_get_recent_students(self):
        students = self.course.get_recent_students()
        student_list = [student for student in students]

        assert len(student_list) == 4
        assert isinstance(student_list[0], User)
        assert hasattr(student_list[0], 'name')

    # preview_html()
    def test_preview_html(self):
        html_str = "<script></script><p>hello</p>"
        prev_html = self.course.preview_html(html_str)

        assert isinstance(prev_html, (str, unicode))
        assert prev_html == "<p>hello</p>"

    # get_settings()
    def test_get_settings(self):
        settings = self.course.get_settings()

        assert isinstance(settings, dict)

    # update_settings()
    def test_update_settings(self):
        settings = self.course.update_settings()

        assert isinstance(settings, dict)
        assert settings['hide_final_grades'] is True

    # reset()
    def test_reset(self):
        course = self.course.reset()

        assert isinstance(course, Course)
        assert hasattr(course, 'name')

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
            self.course.get_quiz(settings.INVALID_ID)

    # list_quizzes()
    def test_list_quizzes(self):
        quizzes = self.course.list_quizzes()
        quiz_list = [quiz for quiz in quizzes]

        assert len(quiz_list) == 4
        assert isinstance(quiz_list[0], Quiz)


class TestCourseNickname(unittest.TestCase):
    """
    Tests core CourseNickname functionality
    """
    @classmethod
    def setUpClass(self):
        requires = {
            'course': [],
            'generic': ['not_found'],
            'user': ['course_nickname', 'remove_nickname']
        }

        adapter = requests_mock.Adapter()
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY, adapter)
        register_uris(settings.BASE_URL, requires, adapter)

        self.nickname = self.canvas.get_course_nickname(1)

    # __str__()
    def test__str__(self):
        string = str(self.nickname)
        assert isinstance(string, str)

    # remove()
    def test_remove(self):
        deleted_nick = self.nickname.remove()

        assert isinstance(deleted_nick, CourseNickname)
        assert hasattr(deleted_nick, 'nickname')
