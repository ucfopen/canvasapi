import unittest
import uuid
import os

import requests_mock

from canvas_api import Canvas
from canvas_api.assignment import Assignment, AssignmentGroup
from canvas_api.course import Course, CourseNickname, Page
from canvas_api.discussion_topic import DiscussionTopic
from canvas_api.enrollment import Enrollment
from canvas_api.exceptions import ResourceDoesNotExist, RequiredFieldMissing
from canvas_api.external_tool import ExternalTool
from canvas_api.group import Group, GroupCategory
from canvas_api.module import Module
from canvas_api.quiz import Quiz
from canvas_api.section import Section
from canvas_api.user import User
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestCourse(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                'course': ['get_by_id', 'get_page'],
                'quiz': ['get_by_id'],
                'user': ['get_by_id']
            }
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.page = self.course.get_page('my-url')
            self.quiz = self.course.get_quiz(1)
            self.user = self.canvas.get_user(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.course)
        self.assertIsInstance(string, str)

    # conclude()
    def test_conclude(self, m):
        register_uris({'course': ['conclude']}, m)

        success = self.course.conclude()
        self.assertTrue(success)

    # delete()
    def test_delete(self, m):
        register_uris({'course': ['delete']}, m)

        success = self.course.delete()
        self.assertTrue(success)

    # update()
    def test_update(self, m):
        register_uris({'course': ['update']}, m)

        new_name = 'New Name'
        self.course.update(course={'name': new_name})
        self.assertEqual(self.course.name, new_name)

    # get_user()
    def test_get_user(self, m):
        register_uris({'course': ['get_user']}, m)

        user = self.course.get_user(1)

        self.assertIsInstance(user, User)
        self.assertTrue(hasattr(user, 'name'))

    def test_get_user_id_type(self, m):
        register_uris({'course': ['get_user_id_type']}, m)

        user = self.course.get_user("SISLOGIN", "sis_login_id")

        self.assertIsInstance(user, User)
        self.assertTrue(hasattr(user, 'name'))

    # get_users()
    def test_get_users(self, m):
        register_uris({'course': ['get_users', 'get_users_p2']}, m)

        users = self.course.get_users()
        user_list = [user for user in users]

        self.assertEqual(len(user_list), 4)
        self.assertIsInstance(user_list[0], User)

    # enroll_user()
    def test_enroll_user(self, m):
        requires = {
            'course': ['enroll_user'],
            'user': ['get_by_id']
        }
        register_uris(requires, m)

        enrollment_type = 'TeacherEnrollment'
        user = self.canvas.get_user(1)
        enrollment = self.course.enroll_user(user, enrollment_type)

        self.assertIsInstance(enrollment, Enrollment)
        self.assertTrue(hasattr(enrollment, 'type'))
        self.assertEqual(enrollment.type, enrollment_type)

    # get_recent_students()
    def test_get_recent_students(self, m):
        recent = {'course': ['get_recent_students', 'get_recent_students_p2']}
        register_uris(recent, m)

        students = self.course.get_recent_students()
        student_list = [student for student in students]

        self.assertEqual(len(student_list), 4)
        self.assertIsInstance(student_list[0], User)
        self.assertTrue(hasattr(student_list[0], 'name'))

    # preview_html()
    def test_preview_html(self, m):
        register_uris({'course': ['preview_html']}, m)

        html_str = "<script></script><p>hello</p>"
        prev_html = self.course.preview_html(html_str)

        self.assertIsInstance(prev_html, (str, unicode))
        self.assertEqual(prev_html, "<p>hello</p>")

    # get_settings()
    def test_get_settings(self, m):
        register_uris({'course': ['settings']}, m)

        settings = self.course.get_settings()

        self.assertIsInstance(settings, dict)

    # update_settings()
    def test_update_settings(self, m):
        register_uris({'course': ['update_settings']}, m)

        settings = self.course.update_settings()

        self.assertIsInstance(settings, dict)
        self.assertTrue(settings['hide_final_grades'])

    # upload()
    def test_upload(self, m):
        register_uris({'course': ['upload', 'upload_final']}, m)

        filename = 'testfile_%s' % uuid.uuid4().hex
        file = open(filename, 'w+')

        response = self.course.upload(file)

        self.assertTrue(response[0])
        self.assertIsInstance(response[1], dict)
        self.assertIn('url', response[1])

        # http://stackoverflow.com/a/10840586
        # Not as stupid as it looks.
        try:
            os.remove(filename)
        except OSError:
            pass

    # reset()
    def test_reset(self, m):
        register_uris({'course': ['reset']}, m)

        course = self.course.reset()

        self.assertIsInstance(course, Course)
        self.assertTrue(hasattr(course, 'name'))

    # create_quiz()
    def test_create_quiz(self, m):
        register_uris({'course': ['create_quiz']}, m)

        title = 'Newer Title'
        new_quiz = self.course.create_quiz({'title': title})

        self.assertIsInstance(new_quiz, Quiz)
        self.assertTrue(hasattr(new_quiz, 'title'))
        self.assertEqual(new_quiz.title, title)
        self.assertTrue(hasattr(new_quiz, 'course_id'))
        self.assertEqual(new_quiz.course_id, self.course.id)

    def test_create_quiz_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.course.create_quiz({})

    # get_quiz()
    def test_get_quiz(self, m):
        register_uris({'course': ['get_quiz']}, m)

        target_quiz = self.course.get_quiz(1)

        self.assertIsInstance(target_quiz, Quiz)
        self.assertTrue(hasattr(target_quiz, 'course_id'))
        self.assertEqual(target_quiz.course_id, self.course.id)

    def test_get_quiz_fail(self, m):
        register_uris({'generic': ['not_found']}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.course.get_quiz(settings.INVALID_ID)

    # get_quizzes()
    def test_get_quizzes(self, m):
        register_uris({'course': ['list_quizzes', 'list_quizzes2']}, m)

        quizzes = self.course.get_quizzes()
        quiz_list = [quiz for quiz in quizzes]

        self.assertEqual(len(quiz_list), 4)
        self.assertIsInstance(quiz_list[0], Quiz)
        self.assertTrue(hasattr(quiz_list[0], 'course_id'))
        self.assertEqual(quiz_list[0].course_id, self.course.id)

    # get_modules()
    def test_get_modules(self, m):
        register_uris({'course': ['list_modules', 'list_modules2']}, m)

        modules = self.course.get_modules()
        module_list = [module for module in modules]

        self.assertEqual(len(module_list), 4)
        self.assertIsInstance(module_list[0], Module)
        self.assertTrue(hasattr(module_list[0], 'course_id'))
        self.assertEqual(module_list[0].course_id, self.course.id)

    # get_module()
    def test_get_module(self, m):
        register_uris({'course': ['get_module_by_id']}, m)

        target_module = self.course.get_module(1)

        self.assertIsInstance(target_module, Module)
        self.assertTrue(hasattr(target_module, 'course_id'))
        self.assertEqual(target_module.course_id, self.course.id)

    # create_module()
    def test_create_module(self, m):
        register_uris({'course': ['create_module']}, m)

        name = 'Name'
        new_module = self.course.create_module(module={'name': name})

        self.assertIsInstance(new_module, Module)
        self.assertTrue(hasattr(new_module, 'name'))
        self.assertTrue(hasattr(new_module, 'course_id'))
        self.assertEqual(new_module.course_id, self.course.id)

    def test_create_module_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.course.create_module(module={})

    # get_enrollments()
    def test_get_enrollments(self, m):
        register_uris({'course': ['list_enrollments', 'list_enrollments_2']}, m)

        enrollments = self.course.get_enrollments()
        enrollment_list = [enrollment for enrollment in enrollments]

        self.assertEqual(len(enrollment_list), 4)
        self.assertIsInstance(enrollment_list[0], Enrollment)

    # get_section
    def test_get_section(self, m):
        register_uris({'course': ['get_section']}, m)

        section = self.course.get_section(1)

        self.assertIsInstance(section, Section)

    # create_assignment()
    def test_create_assignment(self, m):
        register_uris({'course': ['create_assignment']}, m)

        name = 'Newly Created Assignment'

        assignment = self.course.create_assignment(assignment={'name': name})

        self.assertIsInstance(assignment, Assignment)
        self.assertTrue(hasattr(assignment, 'name'))
        self.assertEqual(assignment.name, name)
        self.assertEqual(assignment.id, 5)

    def test_create_assignment_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.course.create_assignment(assignment={})

    # get_assignment()
    def test_get_assignment(self, m):
        register_uris({'course': ['get_assignment_by_id']}, m)

        assignment = self.course.get_assignment('5')

        self.assertIsInstance(assignment, Assignment)
        self.assertTrue(hasattr(assignment, 'name'))

    # get_assignments()
    def test_get_assignments(self, m):
        requires = {'course': ['get_all_assignments', 'get_all_assignments2']}
        register_uris(requires, m)

        assignments = self.course.get_assignments()
        assignment_list = [assignment for assignment in assignments]

        self.assertIsInstance(assignments[0], Assignment)
        self.assertEqual(len(assignment_list), 4)

    # show_front_page()
    def test_show_front_page(self, m):
        register_uris({'course': ['show_front_page']}, m)

        front_page = self.course.show_front_page()

        self.assertIsInstance(front_page, Page)
        self.assertTrue(hasattr(front_page, 'url'))
        self.assertTrue(hasattr(front_page, 'title'))

    # create_front_page()
    def test_edit_front_page(self, m):
        register_uris({'course': ['edit_front_page']}, m)

        new_front_page = self.course.edit_front_page()

        self.assertIsInstance(new_front_page, Page)
        self.assertTrue(hasattr(new_front_page, 'url'))
        self.assertTrue(hasattr(new_front_page, 'title'))

    # get_page()
    def test_get_page(self, m):
        register_uris({'course': ['get_page']}, m)

        url = 'my-url'
        page = self.course.get_page(url)

        self.assertIsInstance(page, Page)

    # get_pages()
    def test_get_pages(self, m):
        register_uris({'course': ['get_pages', 'get_pages2']}, m)

        pages = self.course.get_pages()
        page_list = [page for page in pages]

        self.assertEqual(len(page_list), 4)
        self.assertIsInstance(page_list[0], Page)
        self.assertTrue(hasattr(page_list[0], 'course_id'))
        self.assertEqual(page_list[0].course_id, self.course.id)

    # create_page()
    def test_create_page(self, m):
        register_uris({'course': ['create_page']}, m)

        title = "Newest Page"
        new_page = self.course.create_page(wiki_page={'title': title})

        self.assertIsInstance(new_page, Page)
        self.assertTrue(hasattr(new_page, 'title'))
        self.assertEqual(new_page.title, title)
        self.assertTrue(hasattr(new_page, 'course_id'))
        self.assertEqual(new_page.course_id, self.course.id)

    def test_create_page_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.course.create_page(settings.INVALID_ID)

    # get_external_tool()
    def test_get_external_tool(self, m):
        register_uris({'external_tool': ['get_by_id_course']}, m)

        tool = self.course.get_external_tool(1)

        self.assertIsInstance(tool, ExternalTool)
        self.assertTrue(hasattr(tool, 'name'))

    # get_external_tools()
    def test_get_external_tools(self, m):
        requires = {'course': ['get_external_tools', 'get_external_tools_p2']}
        register_uris(requires, m)

        tools = self.course.get_external_tools()
        tool_list = [tool for tool in tools]

        self.assertIsInstance(tool_list[0], ExternalTool)
        self.assertEqual(len(tool_list), 4)

    def test_list_sections(self, m):
        register_uris({'course': ['list_sections', 'list_sections2']}, m)

        sections = self.course.list_sections()
        section_list = [sect for sect in sections]

        self.assertIsInstance(section_list[0], Section)
        self.assertEqual(len(section_list), 4)

    def test_create_course_section(self, m):
        register_uris({'course': ['create_section']}, m)

        section = self.course.create_course_section()

        self.assertIsInstance(section, Section)

    def test_list_groups(self, m):
        requires = {'course': ['list_groups_context', 'list_groups_context2']}
        register_uris(requires, m)

        groups = self.course.list_groups()
        group_list = [group for group in groups]

        self.assertIsInstance(group_list[0], Group)
        self.assertEqual(len(group_list), 4)

    # create_group_category()
    def test_create_group_category(self, m):
        register_uris({'course': ['create_group_category']}, m)

        name_str = "Test String"
        response = self.course.create_group_category(name=name_str)
        self.assertIsInstance(response, GroupCategory)

    # list_group_categories()
    def test_list_group_categories(self, m):
        register_uris({'course': ['list_group_categories']}, m)

        response = self.course.list_group_categories()
        category_list = [category for category in response]
        self.assertIsInstance(category_list[0], GroupCategory)

    # get_discussion_topic()
    def test_get_discussion_topic(self, m):
        register_uris({'course': ['get_discussion_topic']}, m)

        topic_id = 1
        discussion = self.course.get_discussion_topic(topic_id)
        self.assertIsInstance(discussion, DiscussionTopic)
        self.assertTrue(hasattr(discussion, 'course_id'))
        self.assertEquals(discussion.course_id, 1)

    # get_full_discussion_topic()
    def test_get_full_discussion_topic(self, m):
        register_uris({'course': ['get_full_discussion_topic']}, m)

        topic_id = 1
        discussion = self.course.get_full_discussion_topic(topic_id)
        self.assertIsInstance(discussion, DiscussionTopic)
        self.assertTrue(hasattr(discussion, 'view'))
        self.assertTrue(hasattr(discussion, 'participants'))
        self.assertEquals(discussion.course_id, 1)

    # get_discussion_topics()
    def test_get_discussion_topics(self, m):
        register_uris({'course': ['get_discussion_topics']}, m)

        response = self.course.get_discussion_topics()
        discussion_list = [discussion for discussion in response]
        self.assertIsInstance(discussion_list[0], DiscussionTopic)
        self.assertTrue(hasattr(discussion_list[0], 'course_id'))
        self.assertEquals(2, len(discussion_list))

    # create_discussion_topic()
    def test_create_discussion_topic(self, m):
        register_uris({'course': ['create_discussion_topic']}, m)

        title = "Topic 1"
        discussion = self.course.create_discussion_topic()
        self.assertIsInstance(discussion, DiscussionTopic)
        self.assertTrue(hasattr(discussion, 'course_id'))
        self.assertEquals(title, discussion.title)
        self.assertEquals(discussion.course_id, 1)

    # reorder_pinned_topics()
    def test_reorder_pinned_topics(self, m):
        register_uris({'course': ['reorder_pinned_topics']}, m)

        order = [1, 2, 3]

        discussions = self.course.reorder_pinned_topics(order=order)
        self.assertTrue(discussions)

    def test_reorder_pinned_topics_no_list(self, m):
        register_uris({'course': ['reorder_pinned_topics_no_list']}, m)

        order = "1, 2, 3"

        with self.assertRaises(ValueError):
            self.course.reorder_pinned_topics(order=order)

    # get_assignment_group()
    def test_get_assignment_group(self, m):
        register_uris({'assignment': ['get_assignment_group']}, m)

        response = self.course.get_assignment_group(5)

        self.assertIsInstance(response, AssignmentGroup)
        self.assertTrue(hasattr(response, 'id'))
        self.assertTrue(hasattr(response, 'name'))
        self.assertTrue(hasattr(response, 'course_id'))
        self.assertEqual(response.course_id, 1)

    # list_group_categories()
    def test_list_assignment_groups(self, m):
        register_uris({
            'assignment': ['list_assignment_groups', 'get_assignment_group']
        }, m)

        response = self.course.list_assignment_groups()
        asnt_group_list = [assignment_group for assignment_group in response]
        self.assertIsInstance(asnt_group_list[0], AssignmentGroup)
        self.assertTrue(hasattr(asnt_group_list[0], 'id'))
        self.assertTrue(hasattr(asnt_group_list[0], 'name'))
        self.assertTrue(hasattr(asnt_group_list[0], 'course_id'))
        self.assertEqual(asnt_group_list[0].course_id, 1)

    # create_assignment_group()
    def test_create_assignment_group(self, m):
        register_uris({'assignment': ['create_assignment_group']}, m)

        response = self.course.create_assignment_group()

        self.assertIsInstance(response, AssignmentGroup)
        self.assertTrue(hasattr(response, 'id'))
        self.assertEqual(response.id, 3)

    # create_external_tool()
    def test_create_external_tool(self, m):
        register_uris({'external_tool': ['create_tool_course']}, m)

        response = self.course.create_external_tool(
            name="External Tool - Course",
            privacy_level="public",
            consumer_key="key",
            shared_secret="secret"
        )

        self.assertIsInstance(response, ExternalTool)
        self.assertTrue(hasattr(response, 'id'))
        self.assertEqual(response.id, 20)


@requests_mock.Mocker()
class TestCourseNickname(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({'user': ['course_nickname']}, m)
            self.nickname = self.canvas.get_course_nickname(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.nickname)
        self.assertIsInstance(string, str)

    # remove()
    def test_remove(self, m):
        register_uris({'user': ['remove_nickname']}, m)

        deleted_nick = self.nickname.remove()

        self.assertIsInstance(deleted_nick, CourseNickname)
        self.assertTrue(hasattr(deleted_nick, 'nickname'))
