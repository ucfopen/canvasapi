from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import uuid
import warnings

import requests
import requests_mock
from six import text_type
from six.moves.urllib.parse import quote

from canvasapi import Canvas
from canvasapi.assignment import Assignment, AssignmentGroup
from canvasapi.course import Course, CourseNickname, Page
from canvasapi.discussion_topic import DiscussionTopic
from canvasapi.enrollment import Enrollment
from canvasapi.exceptions import ResourceDoesNotExist, RequiredFieldMissing
from canvasapi.external_feed import ExternalFeed
from canvasapi.external_tool import ExternalTool
from canvasapi.file import File
from canvasapi.folder import Folder
from canvasapi.group import Group, GroupCategory
from canvasapi.module import Module
from canvasapi.outcome import OutcomeGroup, OutcomeLink
from canvasapi.quiz import Quiz
from canvasapi.section import Section
from canvasapi.tab import Tab
from canvasapi.user import User
from canvasapi.submission import Submission
from canvasapi.user import UserDisplay
from tests import settings
from tests.util import cleanup_file, register_uris


@requests_mock.Mocker()
class TestCourse(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                'course': ['get_assignment_by_id', 'get_by_id', 'get_page'],
                'quiz': ['get_by_id'],
                'user': ['get_by_id']
            }
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.page = self.course.get_page('my-url')
            self.quiz = self.course.get_quiz(1)
            self.user = self.canvas.get_user(1)
            self.assignment = self.course.get_assignment('5')

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

        user_by_id = self.course.get_user(1)
        self.assertIsInstance(user_by_id, User)
        self.assertTrue(hasattr(user_by_id, 'name'))

        user_by_obj = self.course.get_user(user_by_id)
        self.assertIsInstance(user_by_obj, User)
        self.assertTrue(hasattr(user_by_obj, 'name'))

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

        self.assertIsInstance(prev_html, text_type)
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

        filename = 'testfile_course_{}'.format(uuid.uuid4().hex)
        with open(filename, 'w+') as file:
            response = self.course.upload(file)

        self.assertTrue(response[0])
        self.assertIsInstance(response[1], dict)
        self.assertIn('url', response[1])

        cleanup_file(filename)

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

        target_quiz_by_id = self.course.get_quiz(1)

        self.assertIsInstance(target_quiz_by_id, Quiz)
        self.assertTrue(hasattr(target_quiz_by_id, 'course_id'))
        self.assertEqual(target_quiz_by_id.course_id, self.course.id)

        target_quiz_by_obj = self.course.get_quiz(target_quiz_by_id)

        self.assertIsInstance(target_quiz_by_obj, Quiz)
        self.assertTrue(hasattr(target_quiz_by_obj, 'course_id'))
        self.assertEqual(target_quiz_by_obj.course_id, self.course.id)

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

        target_module_by_id = self.course.get_module(1)

        self.assertIsInstance(target_module_by_id, Module)
        self.assertTrue(hasattr(target_module_by_id, 'course_id'))
        self.assertEqual(target_module_by_id.course_id, self.course.id)

        target_module_by_obj = self.course.get_module(target_module_by_id)

        self.assertIsInstance(target_module_by_obj, Module)
        self.assertTrue(hasattr(target_module_by_obj, 'course_id'))
        self.assertEqual(target_module_by_obj.course_id, self.course.id)

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

        section_by_id = self.course.get_section(1)
        self.assertIsInstance(section_by_id, Section)

        section_by_obj = self.course.get_section(section_by_id)
        self.assertIsInstance(section_by_obj, Section)

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

        assignment_by_id = self.course.get_assignment('5')
        self.assertIsInstance(assignment_by_id, Assignment)
        self.assertTrue(hasattr(assignment_by_id, 'name'))

        assignment_by_obj = self.course.get_assignment(self.assignment)
        self.assertIsInstance(assignment_by_obj, Assignment)
        self.assertTrue(hasattr(assignment_by_obj, 'name'))

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

        tool_by_id = self.course.get_external_tool(1)
        self.assertIsInstance(tool_by_id, ExternalTool)
        self.assertTrue(hasattr(tool_by_id, 'name'))

        tool_by_obj = self.course.get_external_tool(tool_by_id)
        self.assertIsInstance(tool_by_obj, ExternalTool)
        self.assertTrue(hasattr(tool_by_obj, 'name'))

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
        discussion_by_id = self.course.get_discussion_topic(topic_id)
        self.assertIsInstance(discussion_by_id, DiscussionTopic)
        self.assertTrue(hasattr(discussion_by_id, 'course_id'))
        self.assertEqual(discussion_by_id.course_id, 1)

        discussion_by_obj = self.course.get_discussion_topic(discussion_by_id)
        self.assertIsInstance(discussion_by_obj, DiscussionTopic)
        self.assertTrue(hasattr(discussion_by_obj, 'course_id'))
        self.assertEqual(discussion_by_obj.course_id, 1)

    # get_file()
    def test_get_file(self, m):
        register_uris({'course': ['get_file']}, m)

        file_by_id = self.course.get_file(1)
        self.assertIsInstance(file_by_id, File)
        self.assertEqual(file_by_id.display_name, 'Course_File.docx')
        self.assertEqual(file_by_id.size, 2048)

        file_by_obj = self.course.get_file(file_by_id)
        self.assertIsInstance(file_by_obj, File)
        self.assertEqual(file_by_obj.display_name, 'Course_File.docx')
        self.assertEqual(file_by_obj.size, 2048)

    # get_full_discussion_topic()
    def test_get_full_discussion_topic(self, m):
        register_uris(
            {
                'course': [
                    'get_discussion_topics',
                    'get_full_discussion_topic'
                ]
            }, m)

        topic_id = 1
        discussion_by_id = self.course.get_full_discussion_topic(topic_id)
        self.assertIsInstance(discussion_by_id, dict)
        self.assertIn('view', discussion_by_id)
        self.assertIn('participants', discussion_by_id)
        self.assertIn('id', discussion_by_id)
        self.assertEqual(discussion_by_id['id'], topic_id)

        discussion_topics = self.course.get_discussion_topics()
        discussion_by_obj = self.course.get_full_discussion_topic(discussion_topics[0])
        self.assertIsInstance(discussion_by_obj, dict)
        self.assertIn('view', discussion_by_obj)
        self.assertIn('participants', discussion_by_obj)
        self.assertIn('id', discussion_by_obj)
        self.assertEqual(discussion_by_obj['id'], topic_id)

    # get_discussion_topics()
    def test_get_discussion_topics(self, m):
        register_uris({'course': ['get_discussion_topics']}, m)

        response = self.course.get_discussion_topics()
        discussion_list = [discussion for discussion in response]
        self.assertIsInstance(discussion_list[0], DiscussionTopic)
        self.assertTrue(hasattr(discussion_list[0], 'course_id'))
        self.assertEqual(2, len(discussion_list))

    # create_discussion_topic()
    def test_create_discussion_topic(self, m):
        register_uris({'course': ['create_discussion_topic']}, m)

        title = "Topic 1"
        discussion = self.course.create_discussion_topic()
        self.assertIsInstance(discussion, DiscussionTopic)
        self.assertTrue(hasattr(discussion, 'course_id'))
        self.assertEqual(title, discussion.title)
        self.assertEqual(discussion.course_id, 1)

    # reorder_pinned_topics()
    def test_reorder_pinned_topics(self, m):
        # Custom matcher to test that params are set correctly
        def custom_matcher(request):
            match_text = '1,2,3'
            if request.text == 'order={}'.format(quote(match_text)):
                resp = requests.Response()
                resp._content = b'{"reorder": true, "order": [1, 2, 3]}'
                resp.status_code = 200
                return resp

        m.add_matcher(custom_matcher)

        order = [1, 2, 3]
        discussions = self.course.reorder_pinned_topics(order=order)
        self.assertTrue(discussions)

    def test_reorder_pinned_topics_tuple(self, m):
        register_uris({'course': ['reorder_pinned_topics']}, m)

        order = (1, 2, 3)
        discussions = self.course.reorder_pinned_topics(order=order)
        self.assertTrue(discussions)

    def test_reorder_pinned_topics_comma_separated_string(self, m):
        register_uris({'course': ['reorder_pinned_topics']}, m)

        order = "1,2,3"
        discussions = self.course.reorder_pinned_topics(order=order)
        self.assertTrue(discussions)

    def test_reorder_pinned_topics_invalid_input(self, m):
        order = "invalid string"
        with self.assertRaises(ValueError):
            self.course.reorder_pinned_topics(order=order)

    # get_assignment_group()
    def test_get_assignment_group(self, m):
        register_uris({'assignment': ['get_assignment_group']}, m)

        assignment_group_by_id = self.course.get_assignment_group(5)

        self.assertIsInstance(assignment_group_by_id, AssignmentGroup)
        self.assertTrue(hasattr(assignment_group_by_id, 'id'))
        self.assertTrue(hasattr(assignment_group_by_id, 'name'))
        self.assertTrue(hasattr(assignment_group_by_id, 'course_id'))
        self.assertEqual(assignment_group_by_id.course_id, 1)

        assignment_group_by_obj = self.course.get_assignment_group(assignment_group_by_id)

        self.assertIsInstance(assignment_group_by_obj, AssignmentGroup)
        self.assertTrue(hasattr(assignment_group_by_obj, 'id'))
        self.assertTrue(hasattr(assignment_group_by_obj, 'name'))
        self.assertTrue(hasattr(assignment_group_by_obj, 'course_id'))
        self.assertEqual(assignment_group_by_obj.course_id, 1)

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

    # get_course_level_participation_data()
    def test_get_course_level_participation_data(self, m):
        register_uris({'course': ['get_course_level_participation_data']}, m)

        response = self.course.get_course_level_participation_data()

        self.assertIsInstance(response, list)

    # get_course_level_assignment_data()
    def test_get_course_level_assignment_data(self, m):
        register_uris({'course': ['get_course_level_assignment_data']}, m)

        response = self.course.get_course_level_assignment_data()

        self.assertIsInstance(response, list)

    # get_course_level_student_summary_data()
    def test_get_course_level_student_summary_data(self, m):
        register_uris({'course': ['get_course_level_student_summary_data']}, m)

        response = self.course.get_course_level_student_summary_data()

        self.assertIsInstance(response, list)

    # get_user_in_a_course_level_participation_data()
    def test_get_user_in_a_course_level_participation_data(self, m):
        register_uris({'course': ['get_user_in_a_course_level_participation_data']}, m)

        response = self.course.get_user_in_a_course_level_participation_data(1)
        self.assertIsInstance(response, list)

        response = self.course.get_user_in_a_course_level_participation_data(self.user)
        self.assertIsInstance(response, list)

    # get_user_in_a_course_level_assignment_data()
    def test_get_user_in_a_course_level_assignment_data(self, m):
        register_uris({'course': ['get_user_in_a_course_level_assignment_data']}, m)

        response = self.course.get_user_in_a_course_level_assignment_data(1)
        self.assertIsInstance(response, list)

        response = self.course.get_user_in_a_course_level_assignment_data(self.user)
        self.assertIsInstance(response, list)

    # get_user_in_a_course_level_messaging_data()
    def test_get_user_in_a_course_level_messaging_data(self, m):
        register_uris({'course': ['get_user_in_a_course_level_messaging_data']}, m)

        response = self.course.get_user_in_a_course_level_messaging_data(1)
        self.assertIsInstance(response, list)

        response = self.course.get_user_in_a_course_level_messaging_data(self.user)
        self.assertIsInstance(response, list)

    # submit_assignment()
    def test_submit_assignment(self, m):
        register_uris({'course': ['submit_assignment', 'submit_assignment_2']}, m)

        assignment_id = 1
        sub_type = "online_upload"
        sub_dict = {'submission_type': sub_type}
        submission_by_id = self.course.submit_assignment(assignment_id, sub_dict)

        self.assertIsInstance(submission_by_id, Submission)
        self.assertTrue(hasattr(submission_by_id, 'submission_type'))
        self.assertEqual(submission_by_id.submission_type, sub_type)

        submission_by_obj = self.course.submit_assignment(self.assignment, sub_dict)

        self.assertIsInstance(submission_by_obj, Submission)
        self.assertTrue(hasattr(submission_by_obj, 'submission_type'))
        self.assertEqual(submission_by_obj.submission_type, sub_type)

    def test_subit_assignment_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.course.submit_assignment(1, {})

    # list_submissions()
    def test_list_submissions(self, m):
        register_uris({'course': ['list_submissions']}, m)

        assignment_id = 1
        submissions = self.course.list_submissions(assignment_id)
        submission_list = [submission for submission in submissions]

        self.assertEqual(len(submission_list), 2)
        self.assertIsInstance(submission_list[0], Submission)

    # list_multiple_submission()
    def test_list_multiple_submissions(self, m):
        register_uris({'course': ['list_multiple_submissions']}, m)

        submissions = self.course.list_multiple_submissions()
        submission_list = [submission for submission in submissions]

        self.assertEqual(len(submission_list), 2)
        self.assertIsInstance(submission_list[0], Submission)

    def test_list_multiple_submissions_grouped_param(self, m):
        register_uris({'course': ['list_multiple_submissions']}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter('always')
            submissions = self.course.list_multiple_submissions(grouped=True)
            submission_list = [submission for submission in submissions]

            # Ensure using the `grouped` param raises a warning
            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, UserWarning)
            self.assertEqual(
                text_type(warning_list[-1].message),
                'The `grouped` parameter must be empty. Removing kwarg `grouped`.'
            )

            self.assertEqual(len(submission_list), 2)
            self.assertIsInstance(submission_list[0], Submission)

    # get_submission()
    def test_get_submission(self, m):
        register_uris({'course': ['get_assignment_by_id_2', 'get_submission']}, m)

        assignment_for_id = 1
        user_id = 1
        submission_by_id = self.course.get_submission(assignment_for_id, user_id)
        self.assertIsInstance(submission_by_id, Submission)
        self.assertTrue(hasattr(submission_by_id, 'submission_type'))

        assignment_for_obj = self.course.get_assignment(1)
        submission_by_obj = self.course.get_submission(assignment_for_obj, self.user)
        self.assertIsInstance(submission_by_obj, Submission)
        self.assertTrue(hasattr(submission_by_obj, 'submission_type'))

    # update_submission()
    def test_update_submission(self, m):
        register_uris({'course': ['get_assignment_by_id_2', 'update_submission', 'get_submission']}, m)

        assignment_for_id = 1
        user_id = 1
        submission = self.course.update_submission(
            assignment_for_id,
            user_id,
            submission={'excuse': True}
        )

        self.assertIsInstance(submission, Submission)
        self.assertTrue(hasattr(submission, 'excused'))


        assignment_for_obj = self.course.get_assignment(1)
        submission = self.course.update_submission(
            assignment_for_obj,
            self.user,
            submission={'excuse': True}
        )

        self.assertIsInstance(submission, Submission)
        self.assertTrue(hasattr(submission, 'excused'))

    # list_gradeable_students()
    def test_list_gradeable_students(self, m):
        register_uris({'course': ['get_assignment_by_id_2', 'list_gradeable_students']}, m)

        assignment_for_id = 1
        students_by_id = self.course.list_gradeable_students(assignment_for_id)
        student_list_by_id = [student for student in students_by_id]

        self.assertEqual(len(student_list_by_id), 2)
        self.assertIsInstance(student_list_by_id[0], UserDisplay)

        assignment_for_obj = self.course.get_assignment(1)
        students_by_id = self.course.list_gradeable_students(assignment_for_obj)
        student_list_by_id = [student for student in students_by_id]

        self.assertEqual(len(student_list_by_id), 2)
        self.assertIsInstance(student_list_by_id[0], UserDisplay)

    # mark_submission_as_read
    def test_mark_submission_as_read(self, m):
        register_uris({'course': ['get_assignment_by_id_2', 'mark_submission_as_read']}, m)

        assignment_for_id = 1
        user_for_id = 1
        submission_by_id = self.course.mark_submission_as_read(assignment_for_id, user_for_id)
        self.assertTrue(submission_by_id)

        assignment_for_obj = self.course.get_assignment(1)
        submission_by_obj = self.course.mark_submission_as_read(assignment_for_obj, self.user)
        self.assertTrue(submission_by_obj)

    # mark_submission_as_unread
    def test_mark_submission_as_unread(self, m):
        register_uris({'course': ['get_assignment_by_id_2', 'mark_submission_as_unread']}, m)

        assignment_for_id = 1
        user_for_id = 1
        submission_by_id = self.course.mark_submission_as_unread(assignment_for_id, user_for_id)
        self.assertTrue(submission_by_id)

        assignment_for_obj = self.course.get_assignment(1)
        submission_by_obj = self.course.mark_submission_as_unread(assignment_for_obj, self.user)
        self.assertTrue(submission_by_obj)

    # list_external_feeds()
    def test_list_external_feeds(self, m):
        register_uris({'course': ['list_external_feeds']}, m)

        feeds = self.course.list_external_feeds()
        feed_list = [feed for feed in feeds]
        self.assertEqual(len(feed_list), 2)
        self.assertTrue(hasattr(feed_list[0], 'url'))
        self.assertIsInstance(feed_list[0], ExternalFeed)

    # create_external_feed()
    def test_create_external_feed(self, m):
        register_uris({'course': ['create_external_feed']}, m)

        url_str = "http://example.com/myblog.rss"
        response = self.course.create_external_feed(url=url_str)
        self.assertIsInstance(response, ExternalFeed)

    # delete_external_feed()
    def test_delete_external_feed(self, m):
        register_uris({'course': ['delete_external_feed']}, m)

        ef_id = 1
        deleted_ef_by_id = self.course.delete_external_feed(ef_id)
        self.assertIsInstance(deleted_ef_by_id, ExternalFeed)
        self.assertTrue(hasattr(deleted_ef_by_id, 'url'))
        self.assertEqual(deleted_ef_by_id.display_name, "My Blog")

        deleted_ef_by_obj = self.course.delete_external_feed(deleted_ef_by_id)
        self.assertIsInstance(deleted_ef_by_obj, ExternalFeed)
        self.assertTrue(hasattr(deleted_ef_by_obj, 'url'))
        self.assertEqual(deleted_ef_by_obj.display_name, "My Blog")

    # list_files()
    def test_course_files(self, m):
        register_uris({'course': ['list_course_files', 'list_course_files2']}, m)

        files = self.course.list_files()
        file_list = [file for file in files]
        self.assertEqual(len(file_list), 4)
        self.assertIsInstance(file_list[0], File)

    # get_folder()
    def test_get_folder(self, m):
        register_uris({'course': ['get_folder']}, m)

        folder_by_id = self.course.get_folder(1)
        self.assertEqual(folder_by_id.name, "Folder 1")
        self.assertIsInstance(folder_by_id, Folder)

        folder_by_obj = self.course.get_folder(folder_by_id)
        self.assertEqual(folder_by_obj.name, "Folder 1")
        self.assertIsInstance(folder_by_obj, Folder)

    # list_folders()
    def test_list_folders(self, m):
        register_uris({'course': ['list_folders']}, m)

        folders = self.course.list_folders()
        folder_list = [folder for folder in folders]
        self.assertEqual(len(folder_list), 2)
        self.assertIsInstance(folder_list[0], Folder)

    # create_folder()
    def test_create_folder(self, m):
        register_uris({'course': ['create_folder']}, m)

        name_str = "Test String"
        response = self.course.create_folder(name=name_str)
        self.assertIsInstance(response, Folder)

    # list_tabs()
    def test_list_tabs(self, m):
        register_uris({'course': ['list_tabs']}, m)

        tabs = self.course.list_tabs()
        tab_list = [tab for tab in tabs]
        self.assertEqual(len(tab_list), 2)
        self.assertIsInstance(tab_list[0], Tab)

    # update_tab()
    def test_update_tab(self, m):
        register_uris({'course': ['update_tab']}, m)

        tab_id = "pages"
        new_position = 3
        tab = self.course.update_tab(tab_id, position=new_position)

        self.assertIsInstance(tab, Tab)
        self.assertEqual(tab.position, 3)

    # get_root_outcome_group()
    def test_get_root_outcome_group(self, m):
        register_uris({'outcome': ['course_root_outcome_group']}, m)

        outcome_group = self.course.get_root_outcome_group()

        self.assertIsInstance(outcome_group, OutcomeGroup)
        self.assertEqual(outcome_group.id, 1)
        self.assertEqual(outcome_group.title, "ROOT")

    # get_outcome_group()
    def test_get_outcome_group(self, m):
        register_uris({'outcome': ['course_get_outcome_group']}, m)

        outcome_group_by_id = self.course.get_outcome_group(1)
        self.assertIsInstance(outcome_group_by_id, OutcomeGroup)
        self.assertEqual(outcome_group_by_id.id, 1)
        self.assertEqual(outcome_group_by_id.title, "Course outcome group title")

        outcome_group_by_obj = self.course.get_outcome_group(outcome_group_by_id)
        self.assertIsInstance(outcome_group_by_obj, OutcomeGroup)
        self.assertEqual(outcome_group_by_obj.id, 1)
        self.assertEqual(outcome_group_by_obj.title, "Course outcome group title")

    # get_outcome_groups_in_context()
    def test_get_outcome_groups_in_context(self, m):
        register_uris({'outcome': ['course_outcome_groups_in_context']}, m)

        outcome_group_list = self.course.get_outcome_groups_in_context()

        self.assertIsInstance(outcome_group_list[0], OutcomeGroup)
        self.assertEqual(outcome_group_list[0].id, 1)
        self.assertEqual(outcome_group_list[0].title, "ROOT")

    # get_all_outcome_links_in_context()
    def test_get_outcome_links_in_context(self, m):
        register_uris({'outcome': ['course_outcome_links_in_context']}, m)

        outcome_link_list = self.course.get_all_outcome_links_in_context()

        self.assertIsInstance(outcome_link_list[0], OutcomeLink)
        self.assertEqual(outcome_link_list[0].outcome_group['id'], 2)
        self.assertEqual(outcome_link_list[0].outcome_group['title'], "test outcome")

    # get_outcome_results()
    def test_get_outcome_results(self, m):
        register_uris({'outcome': ['course_get_outcome_results']}, m)

        result = self.course.get_outcome_results()

        self.assertIsInstance(result, dict)
        self.assertIsInstance(result['outcome_results'], list)

    # get_outcome_result_rollups()
    def test_get_outcome_result_rollups(self, m):
        register_uris({'outcome': ['course_get_outcome_result_rollups']}, m)

        result = self.course.get_outcome_result_rollups()

        self.assertIsInstance(result, dict)
        self.assertIsInstance(result['rollups'], list)


@requests_mock.Mocker()
class TestCourseNickname(unittest.TestCase):

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
