from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import uuid
import warnings

import requests
import requests_mock
from six import text_type
from six.moves.urllib.parse import quote

from canvasapi import Canvas
from canvasapi.assignment import Assignment, AssignmentGroup, AssignmentOverride
from canvasapi.blueprint import BlueprintSubscription
from canvasapi.blueprint import BlueprintTemplate
from canvasapi.course import Course, CourseNickname, Page
from canvasapi.discussion_topic import DiscussionTopic
from canvasapi.grading_standard import GradingStandard
from canvasapi.enrollment import Enrollment
from canvasapi.course_epub_export import CourseEpubExport
from canvasapi.exceptions import ResourceDoesNotExist, RequiredFieldMissing
from canvasapi.external_feed import ExternalFeed
from canvasapi.external_tool import ExternalTool
from canvasapi.feature import Feature, FeatureFlag
from canvasapi.file import File
from canvasapi.folder import Folder
from canvasapi.grading_period import GradingPeriod
from canvasapi.group import Group, GroupCategory
from canvasapi.module import Module
from canvasapi.outcome import OutcomeGroup, OutcomeLink
from canvasapi.outcome_import import OutcomeImport
from canvasapi.paginated_list import PaginatedList
from canvasapi.progress import Progress
from canvasapi.quiz import Quiz, QuizExtension
from canvasapi.rubric import Rubric
from canvasapi.section import Section
from canvasapi.submission import GroupedSubmission, Submission
from canvasapi.tab import Tab
from canvasapi.user import User
from canvasapi.user import UserDisplay
from canvasapi.content_migration import ContentMigration, Migrator
from canvasapi.content_export import ContentExport
from tests import settings
from tests.util import cleanup_file, register_uris


@requests_mock.Mocker()
class TestCourse(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("always", DeprecationWarning)

        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            requires = {
                "course": ["get_assignment_by_id", "get_by_id", "get_page"],
                "quiz": ["get_by_id"],
                "user": ["get_by_id"],
            }
            register_uris(requires, m)

            self.course = self.canvas.get_course(1)
            self.page = self.course.get_page("my-url")
            self.quiz = self.course.get_quiz(1)
            self.user = self.canvas.get_user(1)
            self.assignment = self.course.get_assignment(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.course)
        self.assertIsInstance(string, str)

    # conclude()
    def test_conclude(self, m):
        register_uris({"course": ["conclude"]}, m)

        success = self.course.conclude()
        self.assertTrue(success)

    # create_assignment_overrides()
    def test_create_assignment_overrides(self, m):
        register_uris({"assignment": ["batch_create_assignment_overrides"]}, m)

        override_list = [
            {
                "student_ids": [1, 2, 3],
                "title": "New Assignment Override",
                "assignment_id": 1,
            },
            {
                "assignment_id": 2,
                "student_ids": [1, 2, 3],
                "title": "New Assignment Override 2",
            },
        ]
        created_overrides = self.course.create_assignment_overrides(override_list)
        created_list = [created for created in created_overrides]

        self.assertEqual(len(created_list), 2)
        self.assertIsInstance(created_list[0], AssignmentOverride)
        self.assertIsInstance(created_list[1], AssignmentOverride)

    # delete()
    def test_delete(self, m):
        register_uris({"course": ["delete"]}, m)

        success = self.course.delete()
        self.assertTrue(success)

    # update()
    def test_update(self, m):
        register_uris({"course": ["update"]}, m)

        new_name = "New Name"
        self.course.update(course={"name": new_name})
        self.assertEqual(self.course.name, new_name)

    # update_assignment_overrides()
    def test_update_assignment_overrides(self, m):
        register_uris({"assignment": ["batch_update_assignment_overrides"]}, m)

        override_list = [
            {
                "student_ids": [4, 5, 6],
                "title": "Updated Assignment Override",
                "assignment_id": 1,
            },
            {
                "assignment_id": 2,
                "student_ids": [6, 7],
                "title": "Updated Assignment Override 2",
            },
        ]
        updated_overrides = self.course.update_assignment_overrides(override_list)
        updated_list = [updated for updated in updated_overrides]

        self.assertEqual(len(updated_list), 2)
        self.assertIsInstance(updated_list[0], AssignmentOverride)
        self.assertIsInstance(updated_list[1], AssignmentOverride)

    # get_user()
    def test_get_user(self, m):
        register_uris({"course": ["get_user"]}, m)

        user_by_id = self.course.get_user(1)
        self.assertIsInstance(user_by_id, User)
        self.assertTrue(hasattr(user_by_id, "name"))

        user_by_obj = self.course.get_user(user_by_id)
        self.assertIsInstance(user_by_obj, User)
        self.assertTrue(hasattr(user_by_obj, "name"))

    def test_get_user_id_type(self, m):
        register_uris({"course": ["get_user_id_type"]}, m)

        user = self.course.get_user("LOGINID", "login_id")

        self.assertIsInstance(user, User)
        self.assertTrue(hasattr(user, "name"))

    # get_users()
    def test_get_users(self, m):
        register_uris({"course": ["get_users", "get_users_p2"]}, m)

        users = self.course.get_users()
        user_list = [user for user in users]

        self.assertEqual(len(user_list), 4)
        self.assertIsInstance(user_list[0], User)

    # enroll_user()
    def test_enroll_user(self, m):
        requires = {"course": ["enroll_user"], "user": ["get_by_id"]}
        register_uris(requires, m)

        enrollment_type = "TeacherEnrollment"
        user_by_id = self.canvas.get_user(1)
        enrollment_by_id = self.course.enroll_user(user_by_id, enrollment_type)

        self.assertIsInstance(enrollment_by_id, Enrollment)
        self.assertTrue(hasattr(enrollment_by_id, "type"))
        self.assertEqual(enrollment_by_id.type, enrollment_type)

        user_by_obj = self.canvas.get_user(self.user)
        enrollment_by_obj = self.course.enroll_user(user_by_obj, enrollment_type)

        self.assertIsInstance(enrollment_by_obj, Enrollment)
        self.assertTrue(hasattr(enrollment_by_obj, "type"))
        self.assertEqual(enrollment_by_obj.type, enrollment_type)

    # get_recent_students()
    def test_get_recent_students(self, m):
        recent = {"course": ["get_recent_students", "get_recent_students_p2"]}
        register_uris(recent, m)

        students = self.course.get_recent_students()
        student_list = [student for student in students]

        self.assertEqual(len(student_list), 4)
        self.assertIsInstance(student_list[0], User)
        self.assertTrue(hasattr(student_list[0], "name"))

    # preview_html()
    def test_preview_html(self, m):
        register_uris({"course": ["preview_html"]}, m)

        html_str = "<script></script><p>hello</p>"
        prev_html = self.course.preview_html(html_str)

        self.assertIsInstance(prev_html, text_type)
        self.assertEqual(prev_html, "<p>hello</p>")

    # get_settings()
    def test_get_settings(self, m):
        register_uris({"course": ["settings"]}, m)

        settings = self.course.get_settings()

        self.assertIsInstance(settings, dict)

    # update_settings()
    def test_update_settings(self, m):
        register_uris({"course": ["update_settings"]}, m)

        settings = self.course.update_settings()

        self.assertIsInstance(settings, dict)
        self.assertTrue(settings["hide_final_grades"])

    # upload()
    def test_upload(self, m):
        register_uris({"course": ["upload", "upload_final"]}, m)

        filename = "testfile_course_{}".format(uuid.uuid4().hex)

        try:
            with open(filename, "w+") as file:
                response = self.course.upload(file)

            self.assertTrue(response[0])
            self.assertIsInstance(response[1], dict)
            self.assertIn("url", response[1])
        finally:
            cleanup_file(filename)

    # reset()
    def test_reset(self, m):
        register_uris({"course": ["reset"]}, m)

        course = self.course.reset()

        self.assertIsInstance(course, Course)
        self.assertTrue(hasattr(course, "name"))

    # create_quiz()
    def test_create_quiz(self, m):
        register_uris({"course": ["create_quiz"]}, m)

        title = "Newer Title"
        new_quiz = self.course.create_quiz({"title": title})

        self.assertIsInstance(new_quiz, Quiz)
        self.assertTrue(hasattr(new_quiz, "title"))
        self.assertEqual(new_quiz.title, title)
        self.assertTrue(hasattr(new_quiz, "course_id"))
        self.assertEqual(new_quiz.course_id, self.course.id)

    def test_create_quiz_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.course.create_quiz({})

    # get_quiz()
    def test_get_quiz(self, m):
        register_uris({"course": ["get_quiz"]}, m)

        target_quiz_by_id = self.course.get_quiz(1)

        self.assertIsInstance(target_quiz_by_id, Quiz)
        self.assertTrue(hasattr(target_quiz_by_id, "course_id"))
        self.assertEqual(target_quiz_by_id.course_id, self.course.id)

        target_quiz_by_obj = self.course.get_quiz(target_quiz_by_id)

        self.assertIsInstance(target_quiz_by_obj, Quiz)
        self.assertTrue(hasattr(target_quiz_by_obj, "course_id"))
        self.assertEqual(target_quiz_by_obj.course_id, self.course.id)

    def test_get_quiz_fail(self, m):
        register_uris({"generic": ["not_found"]}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.course.get_quiz(settings.INVALID_ID)

    # get_quizzes()
    def test_get_quizzes(self, m):
        register_uris({"course": ["list_quizzes", "list_quizzes2"]}, m)

        quizzes = self.course.get_quizzes()
        quiz_list = [quiz for quiz in quizzes]

        self.assertEqual(len(quiz_list), 4)
        self.assertIsInstance(quiz_list[0], Quiz)
        self.assertTrue(hasattr(quiz_list[0], "course_id"))
        self.assertEqual(quiz_list[0].course_id, self.course.id)

    # get_modules()
    def test_get_modules(self, m):
        register_uris({"course": ["list_modules", "list_modules2"]}, m)

        modules = self.course.get_modules()
        module_list = [module for module in modules]

        self.assertEqual(len(module_list), 4)
        self.assertIsInstance(module_list[0], Module)
        self.assertTrue(hasattr(module_list[0], "course_id"))
        self.assertEqual(module_list[0].course_id, self.course.id)

    # get_module()
    def test_get_module(self, m):
        register_uris({"course": ["get_module_by_id"]}, m)

        target_module_by_id = self.course.get_module(1)

        self.assertIsInstance(target_module_by_id, Module)
        self.assertTrue(hasattr(target_module_by_id, "course_id"))
        self.assertEqual(target_module_by_id.course_id, self.course.id)

        target_module_by_obj = self.course.get_module(target_module_by_id)

        self.assertIsInstance(target_module_by_obj, Module)
        self.assertTrue(hasattr(target_module_by_obj, "course_id"))
        self.assertEqual(target_module_by_obj.course_id, self.course.id)

    # create_module()
    def test_create_module(self, m):
        register_uris({"course": ["create_module"]}, m)

        name = "Name"
        new_module = self.course.create_module(module={"name": name})

        self.assertIsInstance(new_module, Module)
        self.assertTrue(hasattr(new_module, "name"))
        self.assertTrue(hasattr(new_module, "course_id"))
        self.assertEqual(new_module.course_id, self.course.id)

    def test_create_module_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.course.create_module(module={})

    # get_enrollments()
    def test_get_enrollments(self, m):
        register_uris({"course": ["list_enrollments", "list_enrollments_2"]}, m)

        enrollments = self.course.get_enrollments()
        enrollment_list = [enrollment for enrollment in enrollments]

        self.assertEqual(len(enrollment_list), 4)
        self.assertIsInstance(enrollment_list[0], Enrollment)

    # get_sections()
    def test_get_sections(self, m):
        register_uris({"course": ["get_sections", "get_sections_p2"]}, m)

        sections = self.course.get_sections()
        section_list = [section for section in sections]

        self.assertEqual(len(section_list), 4)
        self.assertIsInstance(section_list[0], Section)

    # get_section
    def test_get_section(self, m):
        register_uris({"course": ["get_section"]}, m)

        section_by_id = self.course.get_section(1)
        self.assertIsInstance(section_by_id, Section)

        section_by_obj = self.course.get_section(section_by_id)
        self.assertIsInstance(section_by_obj, Section)

    # create_assignment()
    def test_create_assignment(self, m):
        register_uris({"course": ["create_assignment"]}, m)

        name = "Newly Created Assignment"

        assignment = self.course.create_assignment(assignment={"name": name})

        self.assertIsInstance(assignment, Assignment)
        self.assertTrue(hasattr(assignment, "name"))
        self.assertEqual(assignment.name, name)
        self.assertEqual(assignment.id, 1)

    def test_create_assignment_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.course.create_assignment(assignment={})

    # get_assignment()
    def test_get_assignment(self, m):
        register_uris({"course": ["get_assignment_by_id"]}, m)

        assignment_by_id = self.course.get_assignment(1)
        self.assertIsInstance(assignment_by_id, Assignment)
        self.assertTrue(hasattr(assignment_by_id, "name"))

        assignment_by_obj = self.course.get_assignment(self.assignment)
        self.assertIsInstance(assignment_by_obj, Assignment)
        self.assertTrue(hasattr(assignment_by_obj, "name"))

    # get_assignment_overrides()
    def test_get_assignment_overrides(self, m):
        register_uris(
            {
                "assignment": [
                    "batch_get_assignment_overrides",
                    "batch_get_assignment_overrides_p2",
                ]
            },
            m,
        )

        bulk_select = [{"id": 1, "assignment_id": 1}, {"id": 20, "assignment_id": 2}]
        overrides = self.course.get_assignment_overrides(bulk_select)

        override_list = [override for override in overrides]

        self.assertEqual(len(override_list), 2)
        self.assertIsInstance(override_list[0], AssignmentOverride)

    # get_assignments()
    def test_get_assignments(self, m):
        requires = {"course": ["get_all_assignments", "get_all_assignments2"]}
        register_uris(requires, m)

        assignments = self.course.get_assignments()
        assignment_list = [assignment for assignment in assignments]

        self.assertIsInstance(assignments[0], Assignment)
        self.assertEqual(len(assignment_list), 4)

    # show_front_page()
    def test_show_front_page(self, m):
        register_uris({"course": ["show_front_page"]}, m)

        front_page = self.course.show_front_page()

        self.assertIsInstance(front_page, Page)
        self.assertTrue(hasattr(front_page, "url"))
        self.assertTrue(hasattr(front_page, "title"))

    # create_front_page()
    def test_edit_front_page(self, m):
        register_uris({"course": ["edit_front_page"]}, m)

        new_front_page = self.course.edit_front_page()

        self.assertIsInstance(new_front_page, Page)
        self.assertTrue(hasattr(new_front_page, "url"))
        self.assertTrue(hasattr(new_front_page, "title"))

    # get_page()
    def test_get_page(self, m):
        register_uris({"course": ["get_page"]}, m)

        url = "my-url"
        page = self.course.get_page(url)

        self.assertIsInstance(page, Page)

    # get_pages()
    def test_get_pages(self, m):
        register_uris({"course": ["get_pages", "get_pages2"]}, m)

        pages = self.course.get_pages()
        page_list = [page for page in pages]

        self.assertEqual(len(page_list), 4)
        self.assertIsInstance(page_list[0], Page)
        self.assertTrue(hasattr(page_list[0], "course_id"))
        self.assertEqual(page_list[0].course_id, self.course.id)

    # create_page()
    def test_create_page(self, m):
        register_uris({"course": ["create_page"]}, m)

        title = "Newest Page"
        new_page = self.course.create_page(wiki_page={"title": title})

        self.assertIsInstance(new_page, Page)
        self.assertTrue(hasattr(new_page, "title"))
        self.assertEqual(new_page.title, title)
        self.assertTrue(hasattr(new_page, "course_id"))
        self.assertEqual(new_page.course_id, self.course.id)

    def test_create_page_fail(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.course.create_page(settings.INVALID_ID)

    # get_external_tool()
    def test_get_external_tool(self, m):
        register_uris({"external_tool": ["get_by_id_course"]}, m)

        tool_by_id = self.course.get_external_tool(1)
        self.assertIsInstance(tool_by_id, ExternalTool)
        self.assertTrue(hasattr(tool_by_id, "name"))

        tool_by_obj = self.course.get_external_tool(tool_by_id)
        self.assertIsInstance(tool_by_obj, ExternalTool)
        self.assertTrue(hasattr(tool_by_obj, "name"))

    # get_external_tools()
    def test_get_external_tools(self, m):
        requires = {"course": ["get_external_tools", "get_external_tools_p2"]}
        register_uris(requires, m)

        tools = self.course.get_external_tools()
        tool_list = [tool for tool in tools]

        self.assertIsInstance(tool_list[0], ExternalTool)
        self.assertEqual(len(tool_list), 4)

    def test_list_sections(self, m):
        register_uris({"course": ["get_sections", "get_sections_p2"]}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            sections = self.course.list_sections()
            section_list = [sect for sect in sections]

            self.assertEqual(len(section_list), 4)
            self.assertIsInstance(section_list[0], Section)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    def test_create_course_section(self, m):
        register_uris({"course": ["create_section"]}, m)

        section = self.course.create_course_section()

        self.assertIsInstance(section, Section)

    # list_groups()
    def test_list_groups(self, m):
        requires = {"course": ["list_groups_context", "list_groups_context2"]}
        register_uris(requires, m)

        with warnings.catch_warnings(record=True) as warning_list:
            groups = self.course.list_groups()
            group_list = [group for group in groups]

            self.assertIsInstance(group_list[0], Group)
            self.assertEqual(len(group_list), 4)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_groups()
    def test_get_groups(self, m):
        requires = {"course": ["list_groups_context", "list_groups_context2"]}
        register_uris(requires, m)

        groups = self.course.get_groups()
        group_list = [group for group in groups]

        self.assertIsInstance(group_list[0], Group)
        self.assertEqual(len(group_list), 4)

    # create_group_category()
    def test_create_group_category(self, m):
        register_uris({"course": ["create_group_category"]}, m)

        name_str = "Test String"
        response = self.course.create_group_category(name=name_str)
        self.assertIsInstance(response, GroupCategory)

    # list_group_categories()
    def test_list_group_categories(self, m):
        register_uris({"course": ["list_group_categories"]}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            response = self.course.list_group_categories()
            category_list = [category for category in response]
            self.assertIsInstance(category_list[0], GroupCategory)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_group_categories()
    def test_get_group_categories(self, m):
        register_uris({"course": ["list_group_categories"]}, m)

        response = self.course.get_group_categories()
        category_list = [category for category in response]
        self.assertIsInstance(category_list[0], GroupCategory)

    # get_discussion_topic()
    def test_get_discussion_topic(self, m):
        register_uris({"course": ["get_discussion_topic"]}, m)

        topic_id = 1
        discussion_by_id = self.course.get_discussion_topic(topic_id)
        self.assertIsInstance(discussion_by_id, DiscussionTopic)
        self.assertTrue(hasattr(discussion_by_id, "course_id"))
        self.assertEqual(discussion_by_id.course_id, 1)

        discussion_by_obj = self.course.get_discussion_topic(discussion_by_id)
        self.assertIsInstance(discussion_by_obj, DiscussionTopic)
        self.assertTrue(hasattr(discussion_by_obj, "course_id"))
        self.assertEqual(discussion_by_obj.course_id, 1)

    # get_file()
    def test_get_file(self, m):
        register_uris({"course": ["get_file"]}, m)

        file_by_id = self.course.get_file(1)
        self.assertIsInstance(file_by_id, File)
        self.assertEqual(file_by_id.display_name, "Course_File.docx")
        self.assertEqual(file_by_id.size, 2048)

        file_by_obj = self.course.get_file(file_by_id)
        self.assertIsInstance(file_by_obj, File)
        self.assertEqual(file_by_obj.display_name, "Course_File.docx")
        self.assertEqual(file_by_obj.size, 2048)

    # get_full_discussion_topic()
    def test_get_full_discussion_topic(self, m):
        register_uris(
            {"course": ["get_discussion_topics", "get_full_discussion_topic"]}, m
        )

        topic_id = 1
        discussion_by_id = self.course.get_full_discussion_topic(topic_id)
        self.assertIsInstance(discussion_by_id, dict)
        self.assertIn("view", discussion_by_id)
        self.assertIn("participants", discussion_by_id)
        self.assertIn("id", discussion_by_id)
        self.assertEqual(discussion_by_id["id"], topic_id)

        discussion_topics = self.course.get_discussion_topics()
        discussion_by_obj = self.course.get_full_discussion_topic(discussion_topics[0])
        self.assertIsInstance(discussion_by_obj, dict)
        self.assertIn("view", discussion_by_obj)
        self.assertIn("participants", discussion_by_obj)
        self.assertIn("id", discussion_by_obj)
        self.assertEqual(discussion_by_obj["id"], topic_id)

    # get_discussion_topics()
    def test_get_discussion_topics(self, m):
        register_uris({"course": ["get_discussion_topics"]}, m)

        response = self.course.get_discussion_topics()
        discussion_list = [discussion for discussion in response]
        self.assertIsInstance(discussion_list[0], DiscussionTopic)
        self.assertTrue(hasattr(discussion_list[0], "course_id"))
        self.assertEqual(2, len(discussion_list))

    # create_discussion_topic()
    def test_create_discussion_topic(self, m):
        register_uris({"course": ["create_discussion_topic"]}, m)

        title = "Topic 1"
        discussion = self.course.create_discussion_topic()
        self.assertIsInstance(discussion, DiscussionTopic)
        self.assertTrue(hasattr(discussion, "course_id"))
        self.assertEqual(title, discussion.title)
        self.assertEqual(discussion.course_id, 1)

    # reorder_pinned_topics()
    def test_reorder_pinned_topics(self, m):
        # Custom matcher to test that params are set correctly
        def custom_matcher(request):
            match_text = "1,2,3"
            if request.text == "order={}".format(quote(match_text)):
                resp = requests.Response()
                resp._content = b'{"reorder": true, "order": [1, 2, 3]}'
                resp.status_code = 200
                return resp

        m.add_matcher(custom_matcher)

        order = [1, 2, 3]
        discussions = self.course.reorder_pinned_topics(order=order)
        self.assertTrue(discussions)

    def test_reorder_pinned_topics_tuple(self, m):
        register_uris({"course": ["reorder_pinned_topics"]}, m)

        order = (1, 2, 3)
        discussions = self.course.reorder_pinned_topics(order=order)
        self.assertTrue(discussions)

    def test_reorder_pinned_topics_comma_separated_string(self, m):
        register_uris({"course": ["reorder_pinned_topics"]}, m)

        order = "1,2,3"
        discussions = self.course.reorder_pinned_topics(order=order)
        self.assertTrue(discussions)

    def test_reorder_pinned_topics_invalid_input(self, m):
        order = "invalid string"
        with self.assertRaises(ValueError):
            self.course.reorder_pinned_topics(order=order)

    # get_assignment_group()
    def test_get_assignment_group(self, m):
        register_uris({"assignment": ["get_assignment_group"]}, m)

        assignment_group_by_id = self.course.get_assignment_group(5)

        self.assertIsInstance(assignment_group_by_id, AssignmentGroup)
        self.assertTrue(hasattr(assignment_group_by_id, "id"))
        self.assertTrue(hasattr(assignment_group_by_id, "name"))
        self.assertTrue(hasattr(assignment_group_by_id, "course_id"))
        self.assertEqual(assignment_group_by_id.course_id, 1)

        assignment_group_by_obj = self.course.get_assignment_group(
            assignment_group_by_id
        )

        self.assertIsInstance(assignment_group_by_obj, AssignmentGroup)
        self.assertTrue(hasattr(assignment_group_by_obj, "id"))
        self.assertTrue(hasattr(assignment_group_by_obj, "name"))
        self.assertTrue(hasattr(assignment_group_by_obj, "course_id"))
        self.assertEqual(assignment_group_by_obj.course_id, 1)

    # list_assignment_groups()
    def test_list_assignment_groups(self, m):
        register_uris(
            {"assignment": ["list_assignment_groups", "get_assignment_group"]}, m
        )

        with warnings.catch_warnings(record=True) as warning_list:
            response = self.course.list_assignment_groups()
            asnt_group_list = [assignment_group for assignment_group in response]
            self.assertIsInstance(asnt_group_list[0], AssignmentGroup)
            self.assertTrue(hasattr(asnt_group_list[0], "id"))
            self.assertTrue(hasattr(asnt_group_list[0], "name"))
            self.assertTrue(hasattr(asnt_group_list[0], "course_id"))
            self.assertEqual(asnt_group_list[0].course_id, 1)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_assignment_groups()
    def test_get_assignment_groups(self, m):
        register_uris(
            {"assignment": ["list_assignment_groups", "get_assignment_group"]}, m
        )

        response = self.course.get_assignment_groups()
        asnt_group_list = [assignment_group for assignment_group in response]
        self.assertIsInstance(asnt_group_list[0], AssignmentGroup)
        self.assertTrue(hasattr(asnt_group_list[0], "id"))
        self.assertTrue(hasattr(asnt_group_list[0], "name"))
        self.assertTrue(hasattr(asnt_group_list[0], "course_id"))
        self.assertEqual(asnt_group_list[0].course_id, 1)

    # create_assignment_group()
    def test_create_assignment_group(self, m):
        register_uris({"assignment": ["create_assignment_group"]}, m)

        response = self.course.create_assignment_group()

        self.assertIsInstance(response, AssignmentGroup)
        self.assertTrue(hasattr(response, "id"))
        self.assertEqual(response.id, 3)

    # create_external_tool()
    def test_create_external_tool(self, m):
        register_uris({"external_tool": ["create_tool_course"]}, m)

        response = self.course.create_external_tool(
            name="External Tool - Course",
            privacy_level="public",
            consumer_key="key",
            shared_secret="secret",
        )

        self.assertIsInstance(response, ExternalTool)
        self.assertTrue(hasattr(response, "id"))
        self.assertEqual(response.id, 20)

    # get_collaborations
    def test_get_collaborations(self, m):
        register_uris({"course": ["get_collaborations"]}, m)

        from canvasapi.collaboration import Collaboration

        collab_list = self.course.get_collaborations()

        self.assertIsInstance(collab_list, PaginatedList)
        self.assertIsInstance(collab_list[0], Collaboration)
        self.assertIsInstance(collab_list[1], Collaboration)
        self.assertEqual(collab_list[0].id, 1)
        self.assertEqual(collab_list[1].id, 2)
        self.assertEqual(collab_list[0].document_id, "oinwoenfe8w8ef_onweufe89fef")
        self.assertEqual(collab_list[1].document_id, "oinwoenfe8w8ef_onweufe89zzz")

    # get_course_level_participation_data()
    def test_get_course_level_participation_data(self, m):
        register_uris({"course": ["get_course_level_participation_data"]}, m)

        response = self.course.get_course_level_participation_data()

        self.assertIsInstance(response, list)

    # get_course_level_assignment_data()
    def test_get_course_level_assignment_data(self, m):
        register_uris({"course": ["get_course_level_assignment_data"]}, m)

        response = self.course.get_course_level_assignment_data()

        self.assertIsInstance(response, list)

    # get_course_level_student_summary_data()
    def test_get_course_level_student_summary_data(self, m):
        register_uris({"course": ["get_course_level_student_summary_data"]}, m)

        response = self.course.get_course_level_student_summary_data()

        self.assertIsInstance(response, list)

    # get_user_in_a_course_level_participation_data()
    def test_get_user_in_a_course_level_participation_data(self, m):
        register_uris({"course": ["get_user_in_a_course_level_participation_data"]}, m)

        response = self.course.get_user_in_a_course_level_participation_data(1)
        self.assertIsInstance(response, list)

        response = self.course.get_user_in_a_course_level_participation_data(self.user)
        self.assertIsInstance(response, list)

    # get_user_in_a_course_level_assignment_data()
    def test_get_user_in_a_course_level_assignment_data(self, m):
        register_uris({"course": ["get_user_in_a_course_level_assignment_data"]}, m)

        response = self.course.get_user_in_a_course_level_assignment_data(1)
        self.assertIsInstance(response, list)

        response = self.course.get_user_in_a_course_level_assignment_data(self.user)
        self.assertIsInstance(response, list)

    # get_user_in_a_course_level_messaging_data()
    def test_get_user_in_a_course_level_messaging_data(self, m):
        register_uris({"course": ["get_user_in_a_course_level_messaging_data"]}, m)

        response = self.course.get_user_in_a_course_level_messaging_data(1)
        self.assertIsInstance(response, list)

        response = self.course.get_user_in_a_course_level_messaging_data(self.user)
        self.assertIsInstance(response, list)

    # submit_assignment()
    def test_submit_assignment(self, m):
        register_uris({"assignment": ["submit"]}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            assignment_id = 1
            sub_type = "online_upload"
            sub_dict = {"submission_type": sub_type}
            submission_by_id = self.course.submit_assignment(assignment_id, sub_dict)

            self.assertIsInstance(submission_by_id, Submission)
            self.assertTrue(hasattr(submission_by_id, "submission_type"))
            self.assertEqual(submission_by_id.submission_type, sub_type)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

        with warnings.catch_warnings(record=True) as warning_list:
            submission_by_obj = self.course.submit_assignment(self.assignment, sub_dict)

            self.assertIsInstance(submission_by_obj, Submission)
            self.assertTrue(hasattr(submission_by_obj, "submission_type"))
            self.assertEqual(submission_by_obj.submission_type, sub_type)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    def test_submit_assignment_fail(self, m):
        with warnings.catch_warnings(record=True) as warning_list:
            with self.assertRaises(RequiredFieldMissing):
                self.course.submit_assignment(1, {})

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # list_submissions()
    def test_list_submissions(self, m):
        register_uris({"submission": ["list_submissions"]}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            assignment_id = 1
            submissions_by_id = self.course.list_submissions(assignment_id)
            submission_list_by_id = [submission for submission in submissions_by_id]

            self.assertEqual(len(submission_list_by_id), 2)
            self.assertIsInstance(submission_list_by_id[0], Submission)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

        with warnings.catch_warnings(record=True) as warning_list:
            submissions_by_obj = self.course.list_submissions(self.assignment)
            submission_list_by_obj = [submission for submission in submissions_by_obj]

            self.assertEqual(len(submission_list_by_obj), 2)
            self.assertIsInstance(submission_list_by_obj[0], Submission)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # list_multiple_submission()
    def test_list_multiple_submissions(self, m):
        register_uris({"course": ["list_multiple_submissions"]}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            submissions = self.course.list_multiple_submissions()
            submission_list = [submission for submission in submissions]

            self.assertEqual(len(submission_list), 2)
            self.assertIsInstance(submission_list[0], Submission)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_multiple_submission()
    def test_get_multiple_submissions(self, m):
        register_uris({"course": ["list_multiple_submissions"]}, m)

        submissions = self.course.get_multiple_submissions()
        submission_list = [submission for submission in submissions]

        self.assertEqual(len(submission_list), 2)
        self.assertIsInstance(submission_list[0], Submission)

    def test_get_multiple_submissions_grouped_true(self, m):
        register_uris({"course": ["list_multiple_submissions_grouped"]}, m)

        submissions = self.course.get_multiple_submissions(grouped=True)
        submission_list = [submission for submission in submissions]

        self.assertEqual(len(submission_list), 2)
        self.assertIsInstance(submission_list[0], GroupedSubmission)

    def test_get_multiple_submissions_grouped_false(self, m):
        register_uris({"course": ["list_multiple_submissions"]}, m)

        submissions = self.course.get_multiple_submissions(grouped=False)
        submission_list = [submission for submission in submissions]

        self.assertEqual(len(submission_list), 2)
        self.assertIsInstance(submission_list[0], Submission)

    def test_get_multiple_submissions_grouped_invalid(self, m):
        with self.assertRaises(ValueError) as cm:
            self.course.get_multiple_submissions(grouped="blargh")

        self.assertIn("Parameter `grouped` must", cm.exception.args[0])

    # get_submission()
    def test_get_submission(self, m):
        register_uris(
            {"course": ["get_assignment_by_id"], "submission": ["get_by_id_course"]}, m
        )

        assignment_for_id = 1
        user_id = 1

        with warnings.catch_warnings(record=True) as warning_list:
            submission_by_id = self.course.get_submission(assignment_for_id, user_id)
            self.assertIsInstance(submission_by_id, Submission)
            self.assertTrue(hasattr(submission_by_id, "submission_type"))

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

        with warnings.catch_warnings(record=True) as warning_list:
            assignment_for_obj = self.course.get_assignment(1)
            submission_by_obj = self.course.get_submission(
                assignment_for_obj, self.user
            )
            self.assertIsInstance(submission_by_obj, Submission)
            self.assertTrue(hasattr(submission_by_obj, "submission_type"))

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # update_submission()
    def test_update_submission(self, m):
        register_uris(
            {
                "course": ["get_assignment_by_id"],
                "submission": ["edit", "get_by_id_course"],
            },
            m,
        )

        assignment_for_id = 1
        user_id = 1
        with warnings.catch_warnings(record=True) as warning_list:
            submission = self.course.update_submission(
                assignment_for_id, user_id, submission={"excuse": True}
            )
            self.assertIsInstance(submission, Submission)
            self.assertTrue(hasattr(submission, "excused"))

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

        assignment_for_obj = self.course.get_assignment(1)
        with warnings.catch_warnings(record=True) as warning_list:
            submission = self.course.update_submission(
                assignment_for_obj, self.user, submission={"excuse": True}
            )
            self.assertIsInstance(submission, Submission)
            self.assertTrue(hasattr(submission, "excused"))

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # list_gradeable_students()
    def test_list_gradeable_students(self, m):
        register_uris(
            {"course": ["get_assignment_by_id", "list_gradeable_students"]}, m
        )

        assignment_for_id = 1
        with warnings.catch_warnings(record=True) as warning_list:
            students_by_id = self.course.list_gradeable_students(assignment_for_id)
            student_list_by_id = [student for student in students_by_id]

            self.assertEqual(len(student_list_by_id), 2)
            self.assertIsInstance(student_list_by_id[0], UserDisplay)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

        assignment_for_obj = self.course.get_assignment(1)
        with warnings.catch_warnings(record=True) as warning_list:
            students_by_id = self.course.list_gradeable_students(assignment_for_obj)
            student_list_by_id = [student for student in students_by_id]

            self.assertEqual(len(student_list_by_id), 2)
            self.assertIsInstance(student_list_by_id[0], UserDisplay)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # mark_submission_as_read
    def test_mark_submission_as_read(self, m):
        register_uris(
            {"course": ["get_assignment_by_id", "mark_submission_as_read"]}, m
        )

        assignment_for_id = 1
        user_for_id = 1
        with warnings.catch_warnings(record=True) as warning_list:
            submission_by_id = self.course.mark_submission_as_read(
                assignment_for_id, user_for_id
            )
            self.assertTrue(submission_by_id)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

        assignment_for_obj = self.course.get_assignment(1)
        with warnings.catch_warnings(record=True) as warning_list:
            submission_by_obj = self.course.mark_submission_as_read(
                assignment_for_obj, self.user
            )
            self.assertTrue(submission_by_obj)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # mark_submission_as_unread
    def test_mark_submission_as_unread(self, m):
        register_uris(
            {"course": ["get_assignment_by_id", "mark_submission_as_unread"]}, m
        )

        assignment_for_id = 1
        user_for_id = 1

        with warnings.catch_warnings(record=True) as warning_list:
            submission_by_id = self.course.mark_submission_as_unread(
                assignment_for_id, user_for_id
            )
            self.assertTrue(submission_by_id)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

        assignment_for_obj = self.course.get_assignment(1)
        with warnings.catch_warnings(record=True) as warning_list:
            submission_by_obj = self.course.mark_submission_as_unread(
                assignment_for_obj, self.user
            )
            self.assertTrue(submission_by_obj)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # list_external_feeds()
    def test_list_external_feeds(self, m):
        register_uris({"course": ["list_external_feeds"]}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            feeds = self.course.list_external_feeds()
            feed_list = [feed for feed in feeds]
            self.assertEqual(len(feed_list), 2)
            self.assertTrue(hasattr(feed_list[0], "url"))
            self.assertIsInstance(feed_list[0], ExternalFeed)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_external_feeds()
    def test_get_external_feeds(self, m):
        register_uris({"course": ["list_external_feeds"]}, m)

        feeds = self.course.get_external_feeds()
        feed_list = [feed for feed in feeds]
        self.assertEqual(len(feed_list), 2)
        self.assertTrue(hasattr(feed_list[0], "url"))
        self.assertIsInstance(feed_list[0], ExternalFeed)

    # create_external_feed()
    def test_create_external_feed(self, m):
        register_uris({"course": ["create_external_feed"]}, m)

        url_str = "https://example.com/myblog.rss"
        response = self.course.create_external_feed(url=url_str)
        self.assertIsInstance(response, ExternalFeed)

    # delete_external_feed()
    def test_delete_external_feed(self, m):
        register_uris({"course": ["delete_external_feed"]}, m)

        ef_id = 1
        deleted_ef_by_id = self.course.delete_external_feed(ef_id)
        self.assertIsInstance(deleted_ef_by_id, ExternalFeed)
        self.assertTrue(hasattr(deleted_ef_by_id, "url"))
        self.assertEqual(deleted_ef_by_id.display_name, "My Blog")

        deleted_ef_by_obj = self.course.delete_external_feed(deleted_ef_by_id)
        self.assertIsInstance(deleted_ef_by_obj, ExternalFeed)
        self.assertTrue(hasattr(deleted_ef_by_obj, "url"))
        self.assertEqual(deleted_ef_by_obj.display_name, "My Blog")

    # list_files()
    def test_list_files(self, m):
        register_uris({"course": ["list_course_files", "list_course_files2"]}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            files = self.course.list_files()
            file_list = [file for file in files]
            self.assertEqual(len(file_list), 4)
            self.assertIsInstance(file_list[0], File)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_files()
    def test_get_files(self, m):
        register_uris({"course": ["list_course_files", "list_course_files2"]}, m)

        files = self.course.get_files()
        file_list = [file for file in files]
        self.assertEqual(len(file_list), 4)
        self.assertIsInstance(file_list[0], File)

    # get_folder()
    def test_get_folder(self, m):
        register_uris({"course": ["get_folder"]}, m)

        folder_by_id = self.course.get_folder(1)
        self.assertEqual(folder_by_id.name, "Folder 1")
        self.assertIsInstance(folder_by_id, Folder)

        folder_by_obj = self.course.get_folder(folder_by_id)
        self.assertEqual(folder_by_obj.name, "Folder 1")
        self.assertIsInstance(folder_by_obj, Folder)

    # list_folders()
    def test_list_folders(self, m):
        register_uris({"course": ["list_folders"]}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            folders = self.course.list_folders()
            folder_list = [folder for folder in folders]
            self.assertEqual(len(folder_list), 2)
            self.assertIsInstance(folder_list[0], Folder)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_folders()
    def test_get_folders(self, m):
        register_uris({"course": ["list_folders"]}, m)

        folders = self.course.get_folders()
        folder_list = [folder for folder in folders]
        self.assertEqual(len(folder_list), 2)
        self.assertIsInstance(folder_list[0], Folder)

    # create_folder()
    def test_create_folder(self, m):
        register_uris({"course": ["create_folder"]}, m)

        name_str = "Test String"
        response = self.course.create_folder(name=name_str)
        self.assertIsInstance(response, Folder)

    # list_tabs()
    def test_list_tabs(self, m):
        register_uris({"course": ["list_tabs"]}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            tabs = self.course.list_tabs()
            tab_list = [tab for tab in tabs]
            self.assertEqual(len(tab_list), 2)
            self.assertIsInstance(tab_list[0], Tab)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_tabs()
    def test_get_tabs(self, m):
        register_uris({"course": ["list_tabs"]}, m)

        tabs = self.course.get_tabs()
        tab_list = [tab for tab in tabs]
        self.assertEqual(len(tab_list), 2)
        self.assertIsInstance(tab_list[0], Tab)

    # update_tab()
    def test_update_tab(self, m):
        register_uris({"course": ["update_tab"]}, m)

        tab_id = "pages"
        new_position = 3

        with warnings.catch_warnings(record=True) as warning_list:
            tab = self.course.update_tab(tab_id, position=new_position)

            self.assertIsInstance(tab, Tab)
            self.assertEqual(tab.position, 3)

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_rubric
    def test_get_rubric(self, m):
        register_uris({"course": ["get_rubric_single"]}, m)

        rubric_id = 1
        rubric = self.course.get_rubric(rubric_id)

        self.assertIsInstance(rubric, Rubric)
        self.assertEqual(rubric.id, rubric_id)
        self.assertEqual(rubric.title, "Course Rubric 1")

    # list_rubrics
    def test_list_rubrics(self, m):
        register_uris({"course": ["get_rubric_multiple"]}, m)

        with warnings.catch_warnings(record=True) as warning_list:
            rubrics = self.course.list_rubrics()

            self.assertEqual(len(list(rubrics)), 2)

            self.assertIsInstance(rubrics[0], Rubric)
            self.assertEqual(rubrics[0].id, 1)
            self.assertEqual(rubrics[0].title, "Course Rubric 1")
            self.assertIsInstance(rubrics[1], Rubric)
            self.assertEqual(rubrics[1].id, 2)
            self.assertEqual(rubrics[1].title, "Course Rubric 2")

            self.assertEqual(len(warning_list), 1)
            self.assertEqual(warning_list[-1].category, DeprecationWarning)

    # get_rubrics
    def test_get_rubrics(self, m):
        register_uris({"course": ["get_rubric_multiple"]}, m)

        rubrics = self.course.get_rubrics()

        self.assertEqual(len(list(rubrics)), 2)

        self.assertIsInstance(rubrics[0], Rubric)
        self.assertEqual(rubrics[0].id, 1)
        self.assertEqual(rubrics[0].title, "Course Rubric 1")
        self.assertIsInstance(rubrics[1], Rubric)
        self.assertEqual(rubrics[1].id, 2)
        self.assertEqual(rubrics[1].title, "Course Rubric 2")

    # get_root_outcome_group()
    def test_get_root_outcome_group(self, m):
        register_uris({"outcome": ["course_root_outcome_group"]}, m)

        outcome_group = self.course.get_root_outcome_group()

        self.assertIsInstance(outcome_group, OutcomeGroup)
        self.assertEqual(outcome_group.id, 1)
        self.assertEqual(outcome_group.title, "ROOT")

    # get_outcome_group()
    def test_get_outcome_group(self, m):
        register_uris({"outcome": ["course_get_outcome_group"]}, m)

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
        register_uris({"outcome": ["course_outcome_groups_in_context"]}, m)

        outcome_group_list = self.course.get_outcome_groups_in_context()

        self.assertIsInstance(outcome_group_list[0], OutcomeGroup)
        self.assertEqual(outcome_group_list[0].id, 1)
        self.assertEqual(outcome_group_list[0].title, "ROOT")

    # get_all_outcome_links_in_context()
    def test_get_outcome_links_in_context(self, m):
        register_uris({"outcome": ["course_outcome_links_in_context"]}, m)

        outcome_link_list = self.course.get_all_outcome_links_in_context()

        self.assertIsInstance(outcome_link_list[0], OutcomeLink)
        self.assertEqual(outcome_link_list[0].outcome_group["id"], 2)
        self.assertEqual(outcome_link_list[0].outcome_group["title"], "test outcome")

    # get_outcome_results()
    def test_get_outcome_results(self, m):
        register_uris({"outcome": ["course_get_outcome_results"]}, m)

        result = self.course.get_outcome_results()

        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["outcome_results"], list)

    # get_outcome_result_rollups()
    def test_get_outcome_result_rollups(self, m):
        register_uris({"outcome": ["course_get_outcome_result_rollups"]}, m)

        result = self.course.get_outcome_result_rollups()

        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["rollups"], list)

    # add_grading_standards()
    def test_add_grading_standards(self, m):
        register_uris({"course": ["add_grading_standards"]}, m)

        title = "Grading Standard 1"
        grading_scheme = []
        grading_scheme.append({"name": "A", "value": 90})
        grading_scheme.append({"name": "B", "value": 80})
        grading_scheme.append({"name": "C", "value": 70})

        response = self.course.add_grading_standards(title, grading_scheme)

        self.assertIsInstance(response, GradingStandard)
        self.assertTrue(hasattr(response, "title"))
        self.assertEqual(title, response.title)
        self.assertTrue(hasattr(response, "grading_scheme"))
        self.assertEqual(response.grading_scheme[0].get("name"), "A")
        self.assertEqual(response.grading_scheme[0].get("value"), 0.9)

    # add_grading_standards()
    def test_add_grading_standards_empty_list(self, m):
        register_uris({"course": ["add_grading_standards"]}, m)
        with self.assertRaises(ValueError):
            self.course.add_grading_standards("title", [])

    def test_add_grading_standards_non_dict_list(self, m):
        register_uris({"course": ["add_grading_standards"]}, m)
        with self.assertRaises(ValueError):
            self.course.add_grading_standards("title", [1, 2, 3])

    def test_add_grading_standards_missing_value_key(self, m):
        register_uris({"course": ["add_grading_standards"]}, m)
        with self.assertRaises(ValueError):
            self.course.add_grading_standards("title", [{"name": "test"}])

    def test_add_grading_standards_missing_name_key(self, m):
        register_uris({"course": ["add_grading_standards"]}, m)
        with self.assertRaises(ValueError):
            self.course.add_grading_standards("title", [{"value": 2}])

    # get_grading_standards()
    def test_get_grading_standards(self, m):
        register_uris({"course": ["get_grading_standards"]}, m)

        standards = self.course.get_grading_standards()
        standard_list = [standard for standard in standards]
        self.assertEqual(len(standard_list), 2)
        self.assertIsInstance(standard_list[0], GradingStandard)
        self.assertIsInstance(standard_list[1], GradingStandard)

    # get_single_grading_standards()
    def test_get_single_grading_standard(self, m):
        register_uris({"course": ["get_single_grading_standard"]}, m)

        response = self.course.get_single_grading_standard(1)

        self.assertIsInstance(response, GradingStandard)
        self.assertTrue(hasattr(response, "id"))
        self.assertEqual(1, response.id)
        self.assertTrue(hasattr(response, "title"))
        self.assertEqual("Grading Standard 1", response.title)
        self.assertTrue(hasattr(response, "grading_scheme"))
        self.assertEqual(response.grading_scheme[0].get("name"), "A")
        self.assertEqual(response.grading_scheme[0].get("value"), 0.9)

    # create_content_migration
    def test_create_content_migration(self, m):
        register_uris({"course": ["create_content_migration"]}, m)

        content_migration = self.course.create_content_migration("dummy_importer")

        self.assertIsInstance(content_migration, ContentMigration)
        self.assertTrue(hasattr(content_migration, "migration_type"))

    def test_create_content_migration_migrator(self, m):
        register_uris(
            {"course": ["create_content_migration", "get_migration_systems_multiple"]},
            m,
        )

        migrators = self.course.get_migration_systems()
        content_migration = self.course.create_content_migration(migrators[0])

        self.assertIsInstance(content_migration, ContentMigration)
        self.assertTrue(hasattr(content_migration, "migration_type"))

    def test_create_content_migration_bad_migration_type(self, m):
        register_uris({"course": ["create_content_migration"]}, m)

        with self.assertRaises(TypeError):
            self.course.create_content_migration(1)

    # get_content_migration
    def test_get_content_migration(self, m):
        register_uris({"course": ["get_content_migration_single"]}, m)

        content_migration = self.course.get_content_migration(1)

        self.assertIsInstance(content_migration, ContentMigration)
        self.assertTrue(hasattr(content_migration, "migration_type"))

    # get_content_migrations
    def test_get_content_migrations(self, m):
        register_uris({"course": ["get_content_migration_multiple"]}, m)

        content_migrations = self.course.get_content_migrations()

        self.assertEqual(len(list(content_migrations)), 2)

        self.assertIsInstance(content_migrations[0], ContentMigration)
        self.assertEqual(content_migrations[0].id, 1)
        self.assertEqual(content_migrations[0].migration_type, "dummy_importer")
        self.assertIsInstance(content_migrations[1], ContentMigration)
        self.assertEqual(content_migrations[1].id, 2)
        self.assertEqual(content_migrations[1].migration_type, "dummy_importer")

    # get_migration_systems
    def test_get_migration_systems(self, m):
        register_uris({"course": ["get_migration_systems_multiple"]}, m)

        migration_systems = self.course.get_migration_systems()

        self.assertEqual(len(list(migration_systems)), 2)

        self.assertIsInstance(migration_systems[0], Migrator)
        self.assertEqual(migration_systems[0].type, "dummy_importer")
        self.assertEqual(migration_systems[0].requires_file_upload, True)
        self.assertEqual(migration_systems[0].name, "Dummy Importer 01")
        self.assertIsInstance(migration_systems[1], Migrator)
        self.assertEqual(migration_systems[1].type, "dummy_importer_02")
        self.assertEqual(migration_systems[1].requires_file_upload, False)
        self.assertEqual(migration_systems[1].name, "Dummy Importer 02")

    # set_quiz_extensions
    def test_set_quiz_extensions(self, m):
        register_uris({"course": ["set_quiz_extensions"]}, m)

        extension = self.course.set_quiz_extensions(
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
            self.course.set_quiz_extensions({"user_id": 1, "extra_time": 60})

    def test_set_extensions_empty_list(self, m):
        with self.assertRaises(ValueError):
            self.course.set_quiz_extensions([])

    def test_set_extensions_non_dicts(self, m):
        with self.assertRaises(ValueError):
            self.course.set_quiz_extensions([("user_id", 1), ("extra_time", 60)])

    def test_set_extensions_missing_key(self, m):
        with self.assertRaises(RequiredFieldMissing):
            self.course.set_quiz_extensions([{"extra_time": 60, "extra_attempts": 3}])

    # submissions_bulk_update()
    def test_submissions_bulk_update(self, m):
        register_uris({"course": ["update_submissions"]}, m)
        register_uris({"progress": ["course_progress"]}, m)
        progress = self.course.submissions_bulk_update(
            grade_data={"1": {"1": {"posted_grade": 97}, "2": {"posted_grade": 98}}}
        )
        self.assertIsInstance(progress, Progress)
        self.assertTrue(progress.context_type == "Course")
        progress = progress.query()
        self.assertTrue(progress.context_type == "Course")

    # get_blueprint()
    def test_get_blueprint(self, m):
        register_uris({"course": ["get_blueprint"]}, m)
        blueprint = self.course.get_blueprint(1)
        self.assertIsInstance(blueprint, BlueprintTemplate)
        self.assertEqual(blueprint.course_id, 1)

    def test_get_blueprint_default(self, m):
        register_uris({"course": ["get_blueprint_default"]}, m)
        blueprint_default = self.course.get_blueprint()
        self.assertIsInstance(blueprint_default, BlueprintTemplate)
        self.assertEqual(blueprint_default.course_id, 1)

    # list_blueprint_subscriptions()
    def test_list_blueprint_subscriptions(self, m):
        register_uris({"course": ["list_blueprint_subscriptions"]}, m)
        blueprint_subscriptions = self.course.list_blueprint_subscriptions()
        self.assertIsInstance(blueprint_subscriptions, PaginatedList)
        self.assertIsInstance(blueprint_subscriptions[0], BlueprintSubscription)
        self.assertEqual(blueprint_subscriptions[0].id, 10)
        self.assertEqual(blueprint_subscriptions[0].template_id, 2)
        self.assertEqual(blueprint_subscriptions[0].blueprint_course.get("id"), 1)

    # get_outcome_import_status()
    def test_get_outcome_import_status(self, m):
        register_uris({"course": ["get_outcome_import_status"]}, m)
        outcome_import = self.course.get_outcome_import_status(1)

        self.assertIsInstance(outcome_import, OutcomeImport)
        self.assertEqual(outcome_import.id, 1)
        self.assertEqual(outcome_import.workflow_state, "succeeded")
        self.assertEqual(outcome_import.progress, "100")

    def test_get_outcome_import_status_latest(self, m):
        register_uris({"course": ["get_outcome_import_status_latest"]}, m)
        outcome_import = self.course.get_outcome_import_status("latest")

        self.assertIsInstance(outcome_import, OutcomeImport)
        self.assertEqual(outcome_import.id, 1)
        self.assertEqual(outcome_import.workflow_state, "succeeded")
        self.assertEqual(outcome_import.progress, "100")

    # import_outcome()
    def test_import_outcome_filepath(self, m):
        import os

        register_uris({"course": ["import_outcome"]}, m)

        filepath = os.path.join("tests", "fixtures", "test_import_outcome.csv")

        outcome_import = self.course.import_outcome(filepath)

        self.assertTrue(isinstance(outcome_import, OutcomeImport))
        self.assertTrue(hasattr(outcome_import, "course_id"))
        self.assertTrue(hasattr(outcome_import, "data"))
        self.assertEqual(outcome_import.id, 1)
        self.assertEqual(outcome_import.data["import_type"], "instructure_csv")

    def test_import_outcome_binary(self, m):
        import os

        register_uris({"course": ["import_outcome"]}, m)

        filepath = os.path.join("tests", "fixtures", "test_import_outcome.csv")

        with open(filepath, "rb") as f:
            outcome_import = self.course.import_outcome(f)

        self.assertTrue(isinstance(outcome_import, OutcomeImport))
        self.assertTrue(hasattr(outcome_import, "course_id"))
        self.assertTrue(hasattr(outcome_import, "data"))
        self.assertEqual(outcome_import.id, 1)
        self.assertEqual(outcome_import.data["import_type"], "instructure_csv")

    def test_import_outcome_id(self, m):

        register_uris({"course": ["import_outcome"]}, m)

        outcome_import = self.course.import_outcome(1)

        self.assertTrue(isinstance(outcome_import, OutcomeImport))
        self.assertTrue(hasattr(outcome_import, "course_id"))
        self.assertTrue(hasattr(outcome_import, "data"))
        self.assertEqual(outcome_import.id, 1)
        self.assertEqual(outcome_import.data["import_type"], "instructure_csv")

    def test_import_outcome_ioerror(self, m):
        f = "!@#$%^&*()_+QWERTYUIOP{}|"

        with self.assertRaises(IOError):
            self.course.import_outcome(f)

    # get_epub_export
    def test_get_epub_export(self, m):
        register_uris({"course": ["get_epub_export"]}, m)

        response = self.course.get_epub_export(1)

        self.assertIsInstance(response, CourseEpubExport)
        self.assertEqual(response.id, 1)
        self.assertEqual(response.name, "course1")

        self.assertTrue(hasattr(response, "epub_export"))
        epub1 = response.epub_export

        self.assertEqual(epub1["id"], 1)
        self.assertEqual(epub1["workflow_state"], "exported")

    # create_epub_export
    def test_create_epub_export(self, m):
        register_uris({"course": ["create_epub_export"]}, m)

        response = self.course.create_epub_export()

        self.assertIsInstance(response, CourseEpubExport)
        self.assertEqual(response.id, 1)
        self.assertEqual(response.name, "course1")

        self.assertTrue(hasattr(response, "epub_export"))
        epub1 = response.epub_export

        self.assertEqual(epub1["id"], 1)
        self.assertEqual(epub1["workflow_state"], "exported")

    # list_grading_periods()
    def test_get_grading_periods(self, m):
        register_uris({"course": ["get_grading_periods"]}, m)

        response = self.course.get_grading_periods()

        self.assertIsInstance(response, PaginatedList)
        self.assertIsInstance(response[0], GradingPeriod)
        self.assertIsInstance(response[1], GradingPeriod)
        self.assertEqual(response[0].id, 1)
        self.assertEqual(response[1].id, 2)
        self.assertEqual(response[0].title, "Grading period 1")
        self.assertEqual(response[1].title, "Grading period 2")

    # get_grading_period()
    def test_get_grading_period(self, m):
        register_uris({"course": ["get_grading_period"]}, m)

        grading_period_id = 1
        response = self.course.get_grading_period(grading_period_id)

        self.assertIsInstance(response, GradingPeriod)
        self.assertEqual(response.id, grading_period_id)
        self.assertEqual(response.title, "Grading period 1")

    # get_content_exports()
    def test_list_content_exports(self, m):
        register_uris({"course": ["multiple_content_exports"]}, m)

        content_exports = self.course.get_content_exports()
        content_export_list = [content_export for content_export in content_exports]

        self.assertEqual(len(content_export_list), 2)
        self.assertEqual(content_export_list[0].id, 2)
        self.assertEqual(content_export_list[1].export_type, "b")
        self.assertIsInstance(content_export_list[0], ContentExport)

    # get_content_export()
    def test_show_content_export(self, m):
        register_uris({"course": ["single_content_export"]}, m)

        content_export = self.course.get_content_export(11)

        self.assertTrue(hasattr(content_export, "export_type"))
        self.assertIsInstance(content_export, ContentExport)

    # export_content()
    def test_export_content(self, m):
        register_uris({"course": ["export_content"]}, m)

        content_export = self.course.export_content("d")

        self.assertIsInstance(content_export, ContentExport)
        self.assertTrue(hasattr(content_export, "export_type"))

    # get_enabled_features()
    def test_get__enabled_features(self, m):
        register_uris({"course": ["get_enabled_features"]}, m)

        enabled_features = self.course.get_enabled_features()

        self.assertIsInstance(enabled_features, PaginatedList)
        self.assertIsInstance(enabled_features[0], Feature)

    # get_feature_flag()
    def test_get_feature_flag(self, m):
        register_uris({"course": ["get_features", "get_feature_flag"]}, m)

        feature = self.course.get_features()[0]

        feature_flag = self.course.get_feature_flag(feature)

        self.assertIsInstance(feature_flag, FeatureFlag)
        self.assertEqual(feature_flag.feature, "epub_export")

    # get_features()
    def test_get_features(self, m):
        register_uris({"course": ["get_features"]}, m)

        features = self.course.get_features()

        self.assertIsInstance(features, PaginatedList)
        self.assertIsInstance(features[0], Feature)

    # create_rubric()
    def test_create_rubric_no_association(self, m):
        register_uris({"course": ["create_rubric"]}, m)

        rubric = self.course.create_rubric()

        self.assertIsInstance(rubric, dict)
        self.assertEqual(rubric["rubric"].title, "Course Rubric 1")
        self.assertEqual(rubric["rubric"].id, 1)

    def test_create_rubric_with_association(self, m):
        register_uris({"course": ["create_rubric_with_association"]}, m)

        rubric = self.course.create_rubric()

        self.assertIsInstance(rubric, dict)
        self.assertEqual(rubric["rubric"].title, "Course Rubric 1")
        self.assertEqual(rubric["rubric"].id, 1)

        self.assertEqual(rubric["rubric_association"].id, 1)
        self.assertEqual(rubric["rubric_association"].rubric_id, 1)
        self.assertEqual(rubric["rubric_association"].association_type, "Course")


@requests_mock.Mocker()
class TestCourseNickname(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)

        with requests_mock.Mocker() as m:
            register_uris({"user": ["course_nickname"]}, m)
            self.nickname = self.canvas.get_course_nickname(1)

    # __str__()
    def test__str__(self, m):
        string = str(self.nickname)
        self.assertIsInstance(string, str)

    # remove()
    def test_remove(self, m):
        register_uris({"user": ["remove_nickname"]}, m)

        deleted_nick = self.nickname.remove()

        self.assertIsInstance(deleted_nick, CourseNickname)
        self.assertTrue(hasattr(deleted_nick, "nickname"))
