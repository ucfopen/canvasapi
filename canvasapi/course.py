import warnings

from canvasapi.assignment import Assignment, AssignmentGroup
from canvasapi.blueprint import BlueprintSubscription
from canvasapi.canvas_object import CanvasObject
from canvasapi.collaboration import Collaboration
from canvasapi.course_epub_export import CourseEpubExport
from canvasapi.custom_gradebook_columns import CustomGradebookColumn
from canvasapi.discussion_topic import DiscussionTopic
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.feature import Feature, FeatureFlag
from canvasapi.folder import Folder
from canvasapi.gradebook_history import (
    Day,
    Grader,
    SubmissionHistory,
    SubmissionVersion,
)
from canvasapi.grading_period import GradingPeriod
from canvasapi.grading_standard import GradingStandard
from canvasapi.license import License
from canvasapi.outcome_import import OutcomeImport
from canvasapi.page import Page
from canvasapi.paginated_list import PaginatedList
from canvasapi.progress import Progress
from canvasapi.quiz import QuizExtension
from canvasapi.rubric import Rubric, RubricAssociation
from canvasapi.submission import GroupedSubmission, Submission
from canvasapi.tab import Tab
from canvasapi.todo import Todo
from canvasapi.upload import FileOrPathLike, Uploader
from canvasapi.usage_rights import UsageRights
from canvasapi.util import (
    combine_kwargs,
    file_or_path,
    is_multivalued,
    normalize_bool,
    obj_or_id,
    obj_or_str,
)


class Course(CanvasObject):
    def __str__(self):
        return "{} {} ({})".format(self.course_code, self.name, self.id)

    def add_grading_standards(self, title, grading_scheme_entry, **kwargs):
        """
        Create a new grading standard for the course.

        :calls: `POST /api/v1/courses/:course_id/grading_standards \
        <https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.create>`_

        :param title: The title for the Grading Standard
        :type title: str
        :param grading_scheme: A list of dictionaries containing keys for "name" and "value"
        :type grading_scheme: list of dict
        :rtype: :class:`canvasapi.grading_standards.GradingStandard`
        """
        if not isinstance(grading_scheme_entry, list) or len(grading_scheme_entry) <= 0:
            raise ValueError("Param `grading_scheme_entry` must be a non-empty list.")

        for entry in grading_scheme_entry:
            if not isinstance(entry, dict):
                raise ValueError("grading_scheme_entry must consist of dictionaries.")
            if "name" not in entry or "value" not in entry:
                raise ValueError(
                    "Dictionaries with keys 'name' and 'value' are required."
                )
        kwargs["grading_scheme_entry"] = grading_scheme_entry

        response = self._requester.request(
            "POST",
            "courses/%s/grading_standards" % (self.id),
            title=title,
            _kwargs=combine_kwargs(**kwargs),
        )
        return GradingStandard(self._requester, response.json())

    def column_data_bulk_update(self, column_data, **kwargs):
        """
        Set the content of custom columns.

        :calls: `PUT /api/v1/courses/:course_id/custom_gradebook_column_data \
        <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_column_data_api.bulk_update>`_

        :param column_data: Content to put into the column
        :type column_data: list
        :rtype: :class:`canvasapi.progress.Progress`
        """

        kwargs["column_data"] = column_data

        response = self._requester.request(
            "PUT",
            "courses/{}/custom_gradebook_column_data".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return Progress(self._requester, response.json())

    def conclude(self, **kwargs):
        """
        Mark this course as concluded.

        :calls: `DELETE /api/v1/courses/:id \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.destroy>`_

        :returns: True if the course was concluded, False otherwise.
        :rtype: bool
        """
        kwargs["event"] = "conclude"

        response = self._requester.request(
            "DELETE",
            "courses/{}".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json().get("conclude")

    def create_assignment(self, assignment, **kwargs):
        """
        Create a new assignment for this course.

        Note: The assignment is created in the active state.

        :calls: `POST /api/v1/courses/:course_id/assignments \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.create>`_

        :param assignment: The attributes of the assignment
        :type assignment: dict
        :rtype: :class:`canvasapi.assignment.Assignment`
        """
        from canvasapi.assignment import Assignment

        if isinstance(assignment, dict) and "name" in assignment:
            kwargs["assignment"] = assignment
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")

        response = self._requester.request(
            "POST",
            "courses/{}/assignments".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return Assignment(self._requester, response.json())

    def create_assignment_group(self, **kwargs):
        """
        Create a new assignment group for this course.

        :calls: `POST /api/v1/courses/:course_id/assignment_groups \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.create>`_

        :rtype: :class:`canvasapi.assignment.AssignmentGroup`
        """
        from canvasapi.assignment import AssignmentGroup

        response = self._requester.request(
            "POST",
            "courses/{}/assignment_groups".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"course_id": self.id})

        return AssignmentGroup(self._requester, response_json)

    def create_assignment_overrides(self, assignment_overrides, **kwargs):
        """
        Create the specified overrides for each assignment.

        :calls: `POST /api/v1/courses/:course_id/assignments/overrides \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.batch_create>`_

        :param assignment_overrides: Attributes for the new assignment overrides.
        :type assignment_overrides: list

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.AssignmentOverride`
        """
        from canvasapi.assignment import AssignmentOverride

        kwargs["assignment_overrides"] = assignment_overrides

        return PaginatedList(
            AssignmentOverride,
            self._requester,
            "POST",
            "courses/{}/assignments/overrides".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def create_content_migration(self, migration_type, **kwargs):
        """
        Create a content migration.

        :calls: `POST /api/v1/courses/:course_id/content_migrations \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.create>`_

        :param migration_type: The migrator type to use in this migration
        :type migration_type: str or :class:`canvasapi.content_migration.Migrator`

        :rtype: :class:`canvasapi.content_migration.ContentMigration`
        """
        from canvasapi.content_migration import ContentMigration, Migrator

        if isinstance(migration_type, Migrator):
            kwargs["migration_type"] = migration_type.type
        elif isinstance(migration_type, str):
            kwargs["migration_type"] = migration_type
        else:
            raise TypeError("Parameter migration_type must be of type Migrator or str")

        response = self._requester.request(
            "POST",
            "courses/{}/content_migrations".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"course_id": self.id})

        return ContentMigration(self._requester, response_json)

    def create_course_section(self, **kwargs):
        """
        Create a new section for this course.

        :calls: `POST /api/v1/courses/:course_id/sections \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.create>`_

        :rtype: :class:`canvasapi.course.Section`
        """

        from canvasapi.section import Section

        response = self._requester.request(
            "POST",
            "courses/{}/sections".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return Section(self._requester, response.json())

    def create_custom_column(self, column, **kwargs):
        """
        Create a custom gradebook column.

        :calls: `POST /api/v1/courses/:course_id/custom_gradebook_columns \
        <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.create>`_

        :param column: A dictionary representing the Custom Gradebook Column to create
        :type column: dict

        :rtype: :class:`canvasapi.custom_gradebook_columns.CustomGradebookColumn`
        """
        if isinstance(column, dict) and "title" in column:
            kwargs["column"] = column
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")

        response = self._requester.request(
            "POST",
            "courses/{}/custom_gradebook_columns".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        column_json = response.json()
        column_json.update({"course_id": self.id})

        return CustomGradebookColumn(self._requester, column_json)

    def create_discussion_topic(self, **kwargs):
        """
        Creates a new discussion topic for the course or group.

        :calls: `POST /api/v1/courses/:course_id/discussion_topics \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.create>`_

        :rtype: :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        response = self._requester.request(
            "POST",
            "courses/{}/discussion_topics".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"course_id": self.id})

        return DiscussionTopic(self._requester, response_json)

    def create_epub_export(self, **kwargs):
        """
        Create an ePub export for a course.

        :calls: `POST /api/v1/courses/:course_id/epub_exports/:id\
        <https://canvas.instructure.com/doc/api/e_pub_exports.html#method.epub_exports.create>`_

        :rtype: :class:`canvasapi.course_epub_export.CourseEpubExport`
        """
        response = self._requester.request(
            "POST",
            "courses/{}/epub_exports/".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return CourseEpubExport(self._requester, response.json())

    def create_external_feed(self, url, **kwargs):
        """
        Create a new external feed for the course.

        :calls: `POST /api/v1/courses/:course_id/external_feeds \
        <https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.create>`_

        :param url: The url of the external rss or atom feed
        :type url: str
        :rtype: :class:`canvasapi.external_feed.ExternalFeed`
        """
        from canvasapi.external_feed import ExternalFeed

        response = self._requester.request(
            "POST",
            "courses/{}/external_feeds".format(self.id),
            url=url,
            _kwargs=combine_kwargs(**kwargs),
        )
        return ExternalFeed(self._requester, response.json())

    def create_external_tool(self, **kwargs):
        """
        Create an external tool in the current course.

        :calls: `POST /api/v1/courses/:course_id/external_tools \
        <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.create>`_

        :param name: The name of the tool
        :type name: str

        :rtype: :class:`canvasapi.external_tool.ExternalTool`
        """
        from canvasapi.external_tool import ExternalTool

        required_params = ("name", "privacy_level", "consumer_key", "shared_secret")
        if "client_id" not in kwargs and not all(x in kwargs for x in required_params):
            raise RequiredFieldMissing(
                "Must pass either `client_id` parameter or "
                "`name`, `privacy_level`, `consumer_key`, and `shared_secret` parameters."
            )

        response = self._requester.request(
            "POST",
            "courses/{}/external_tools".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"course_id": self.id})

        return ExternalTool(self._requester, response_json)

    def create_folder(self, name, **kwargs):
        """
        Creates a folder in this course.

        :calls: `POST /api/v1/courses/:course_id/folders \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.create>`_

        :param name: The name of the folder.
        :type name: str
        :rtype: :class:`canvasapi.folder.Folder`
        """
        response = self._requester.request(
            "POST",
            "courses/{}/folders".format(self.id),
            name=name,
            _kwargs=combine_kwargs(**kwargs),
        )
        return Folder(self._requester, response.json())

    def create_group_category(self, name, **kwargs):
        """
        Create a group category.

        :calls: `POST /api/v1/courses/:course_id/group_categories \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.create>`_

        :param name: Name of the category.
        :type name: str
        :rtype: :class:`canvasapi.group.GroupCategory`
        """
        from canvasapi.group import GroupCategory

        response = self._requester.request(
            "POST",
            "courses/{}/group_categories".format(self.id),
            name=name,
            _kwargs=combine_kwargs(**kwargs),
        )
        return GroupCategory(self._requester, response.json())

    def create_late_policy(self, **kwargs):
        """
        Create a late policy. If the course already has a late policy, a bad_request
        is returned since there can only be one late policy per course.

        :calls: `POST /api/v1/courses/:id/late_policy \
        <https://canvas.instructure.com/doc/api/late_policy.html#method.late_policy.create>`_

        :rtype: :class:`canvasapi.course.LatePolicy`
        """

        response = self._requester.request(
            "POST",
            "courses/{}/late_policy".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        late_policy_json = response.json()

        return LatePolicy(self._requester, late_policy_json["late_policy"])

    def create_module(self, module, **kwargs):
        """
        Create a new module.

        :calls: `POST /api/v1/courses/:course_id/modules \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.create>`_

        :param module: The attributes for the module.
        :type module: dict
        :returns: The created module.
        :rtype: :class:`canvasapi.module.Module`
        """
        from canvasapi.module import Module

        if isinstance(module, dict) and "name" in module:
            kwargs["module"] = module
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")

        response = self._requester.request(
            "POST",
            "courses/{}/modules".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        module_json = response.json()
        module_json.update({"course_id": self.id})

        return Module(self._requester, module_json)

    def create_page(self, wiki_page, **kwargs):
        """
        Create a new wiki page.

        :calls: `POST /api/v1/courses/:course_id/pages \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.create>`_

        :param wiki_page: The title for the page.
        :type wiki_page: dict
        :returns: The created page.
        :rtype: :class:`canvasapi.page.Page`
        """

        if isinstance(wiki_page, dict) and "title" in wiki_page:
            kwargs["wiki_page"] = wiki_page
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")

        response = self._requester.request(
            "POST", "courses/{}/pages".format(self.id), _kwargs=combine_kwargs(**kwargs)
        )

        page_json = response.json()
        page_json.update({"course_id": self.id})

        return Page(self._requester, page_json)

    def create_quiz(self, quiz, **kwargs):
        """
        Create a new quiz in this course.

        :calls: `POST /api/v1/courses/:course_id/quizzes \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.create>`_

        :param quiz: The attributes for the quiz.
        :type quiz: dict
        :rtype: :class:`canvasapi.quiz.Quiz`
        """
        from canvasapi.quiz import Quiz

        if isinstance(quiz, dict) and "title" in quiz:
            kwargs["quiz"] = quiz
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")

        response = self._requester.request(
            "POST",
            "courses/{}/quizzes".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        quiz_json = response.json()
        quiz_json.update({"course_id": self.id})

        return Quiz(self._requester, quiz_json)

    def create_rubric(self, **kwargs):
        """
        Create a new rubric.

        :calls: `POST /api/v1/courses/:course_id/rubrics \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics.create>`_

        :returns: Returns a dictionary with rubric and rubric association.
        :rtype: `dict`
        """
        response = self._requester.request(
            "POST",
            "courses/{}/rubrics".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        dictionary = response.json()

        rubric_dict = {}

        if "rubric" in dictionary:
            r_dict = dictionary["rubric"]
            rubric = Rubric(self._requester, r_dict)

            rubric_dict = {"rubric": rubric}

        if "rubric_association" in dictionary:
            ra_dict = dictionary["rubric_association"]
            rubric_association = RubricAssociation(self._requester, ra_dict)

            rubric_dict.update({"rubric_association": rubric_association})

        return rubric_dict

    def create_rubric_association(self, **kwargs):
        """
        Create a new RubricAssociation.

        :calls: `POST /api/v1/courses/:course_id/rubric_associations \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubric_associations.create>`_

        :returns: Returns a RubricAssociation.
        :rtype: :class:`canvasapi.rubric.RubricAssociation`
        """
        from canvasapi.rubric import RubricAssociation

        response = self._requester.request(
            "POST",
            "courses/{}/rubric_associations".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        quiz_json = response.json()
        quiz_json.update({"course_id": self.id})

        return RubricAssociation(self._requester, quiz_json)

    def delete(self, **kwargs):
        """
        Permanently delete this course.

        :calls: `DELETE /api/v1/courses/:id \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.destroy>`_

        :returns: True if the course was deleted, False otherwise.
        :rtype: bool
        """
        kwargs["event"] = "delete"

        response = self._requester.request(
            "DELETE",
            "courses/{}".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json().get("delete")

    def delete_external_feed(self, feed, **kwargs):
        """
        Deletes the external feed.

        :calls: `DELETE /api/v1/courses/:course_id/external_feeds/:external_feed_id \
        <https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.destroy>`_

        :param feed: The object or ID of the feed to be deleted.
        :type feed: :class:`canvasapi.external_feed.ExternalFeed` or int

        :rtype: :class:`canvasapi.external_feed.ExternalFeed`
        """
        from canvasapi.external_feed import ExternalFeed

        feed_id = obj_or_id(feed, "feed", (ExternalFeed,))

        response = self._requester.request(
            "DELETE",
            "courses/{}/external_feeds/{}".format(self.id, feed_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return ExternalFeed(self._requester, response.json())

    def edit_front_page(self, **kwargs):
        """
        Update the title or contents of the front page.

        :calls: `PUT /api/v1/courses/:course_id/front_page \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update_front_page>`_

        :rtype: :class:`canvasapi.course.Course`
        """
        response = self._requester.request(
            "PUT",
            "courses/{}/front_page".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        page_json = response.json()
        page_json.update({"course_id": self.id})

        return Page(self._requester, page_json)

    def edit_late_policy(self, **kwargs):
        """
        Patch a late policy. No body is returned upon success.

        :calls: `PATCH /api/v1/courses/:id/late_policy \
        <https://canvas.instructure.com/doc/api/late_policy.html#method.late_policy.update>`_

        :returns: True if Late Policy was updated successfully. False otherwise.
        :rtype: bool
        """

        response = self._requester.request(
            "PATCH",
            "courses/{}/late_policy".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.status_code == 204

    def enroll_user(self, user, enrollment_type=None, **kwargs):
        """
        Create a new user enrollment for a course or a section.

        :calls: `POST /api/v1/courses/:course_id/enrollments \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.create>`_

        :param user: The object or ID of the user to enroll in this course.
        :type user: :class:`canvasapi.user.User` or int
        :param enrollment_type: The type of enrollment.
        :type enrollment_type: str, optional
        :rtype: :class:`canvasapi.enrollment.Enrollment`
        """
        from canvasapi.enrollment import Enrollment
        from canvasapi.user import User

        kwargs["enrollment[user_id]"] = obj_or_id(user, "user", (User,))

        if enrollment_type:
            warnings.warn(
                (
                    "The `enrollment_type` argument is deprecated and will be "
                    "removed in a future version.\n"
                    "Use `enrollment[type]` as a keyword argument instead. "
                    "e.g. `enroll_user(enrollment={'type': 'StudentEnrollment'})`"
                ),
                DeprecationWarning,
            )
            kwargs["enrollment[type]"] = enrollment_type

        response = self._requester.request(
            "POST",
            "courses/{}/enrollments".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return Enrollment(self._requester, response.json())

    def export_content(self, export_type, **kwargs):
        """
        Begin a content export job for a course.

        :calls: `POST /api/v1/courses/:course_id/content_exports\
        <https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.create>`_

        :param export_type: The type of content to export.
        :type export_type: str

        :rtype: :class:`canvasapi.content_export.ContentExport`
        """
        from canvasapi.content_export import ContentExport

        kwargs["export_type"] = export_type

        response = self._requester.request(
            "POST",
            "courses/{}/content_exports".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return ContentExport(self._requester, response.json())

    def get_all_outcome_links_in_context(self, **kwargs):
        """
        Get all outcome links for context - BETA

        :calls: `GET /api/v1/courses/:course_id/outcome_group_links \
        <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link_index>`_

        :returns: Paginated List of OutcomesLinks in the context.
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.outcome.OutcomeLink`
        """
        from canvasapi.outcome import OutcomeLink

        return PaginatedList(
            OutcomeLink,
            self._requester,
            "GET",
            "courses/{}/outcome_group_links".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_assignment(self, assignment, **kwargs):
        """
        Return the assignment with the given ID.

        :calls: `GET /api/v1/courses/:course_id/assignments/:id \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.show>`_

        :param assignment: The object or ID of the assignment to retrieve.
        :type assignment: :class:`canvasapi.assignment.Assignment` or int

        :rtype: :class:`canvasapi.assignment.Assignment`
        """
        from canvasapi.assignment import Assignment

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))

        response = self._requester.request(
            "GET",
            "courses/{}/assignments/{}".format(self.id, assignment_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Assignment(self._requester, response.json())

    def get_assignment_group(self, assignment_group, **kwargs):
        """
        Retrieve specified assignment group for the specified course.

        :calls: `GET /api/v1/courses/:course_id/assignment_groups/:assignment_group_id \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.show>`_

        :param assignment_group: object or ID of assignment group.
        :type assignment_group: :class:`canvasapi.assignment.AssignmentGroup` or int

        :rtype: :class:`canvasapi.assignment.AssignmentGroup`
        """
        from canvasapi.assignment import AssignmentGroup

        assignment_group_id = obj_or_id(
            assignment_group, "assignment_group", (AssignmentGroup,)
        )

        response = self._requester.request(
            "GET",
            "courses/{}/assignment_groups/{}".format(self.id, assignment_group_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"course_id": self.id})

        return AssignmentGroup(self._requester, response_json)

    def get_assignment_groups(self, **kwargs):
        """
        List assignment groups for the specified course.

        :calls: `GET /api/v1/courses/:course_id/assignment_groups \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.AssignmentGroup`
        """
        from canvasapi.assignment import AssignmentGroup

        return PaginatedList(
            AssignmentGroup,
            self._requester,
            "GET",
            "courses/{}/assignment_groups".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_assignment_overrides(self, assignment_overrides, **kwargs):
        """
        List the specified overrides in this course, providing they target
            sections/groups/students visible to the current user.

        :calls: `GET /api/v1/courses/:course_id/assignments/overrides \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.batch_retrieve>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.AssignmentOverride`
        """
        from canvasapi.assignment import AssignmentOverride

        kwargs["assignment_overrides"] = assignment_overrides

        return PaginatedList(
            AssignmentOverride,
            self._requester,
            "GET",
            "courses/{}/assignments/overrides".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_assignments(self, **kwargs):
        """
        List all of the assignments in this course.

        :calls: `GET /api/v1/courses/:course_id/assignments \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.Assignment`
        """
        from canvasapi.assignment import Assignment

        return PaginatedList(
            Assignment,
            self._requester,
            "GET",
            "courses/{}/assignments".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_assignments_for_group(self, assignment_group, **kwargs):
        """
        Returns a paginated list of assignments for the given assignment group

        :calls: `GET /api/v1/courses/:course_id/assignment_groups/:assignment_group_id/assignments\
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index>`_

        :param assignment_group: The object or id of the assignment group
        :type assignment_group: :class: `canvasapi.assignment.AssignmentGroup` or int

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.Assignment`
        """

        assignment_group_id = obj_or_id(
            assignment_group, "assignment_group", (AssignmentGroup,)
        )

        return PaginatedList(
            Assignment,
            self._requester,
            "GET",
            "courses/{}/assignment_groups/{}/assignments".format(
                self.id, assignment_group_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_blueprint(self, template="default", **kwargs):
        """
        Return the blueprint of a given ID.

        :calls: `GET /api/v1/courses/:course_id/blueprint_templates/:template_id \
        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.master_courses/master_templates.show>`_

        :param template: The object or ID of the blueprint template to get.
        :type template: int or :class:`canvasapi.blueprint.BlueprintTemplate`

        :rtype: :class:`canvasapi.blueprint.BlueprintTemplate`
        """
        from canvasapi.blueprint import BlueprintTemplate

        if template == "default":
            template_id = template
        else:
            template_id = obj_or_id(template, "template", (BlueprintTemplate,))

        response = self._requester.request(
            "GET",
            "courses/{}/blueprint_templates/{}".format(self.id, template_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return BlueprintTemplate(self._requester, response.json())

    def get_collaborations(self, **kwargs):
        """
        Return a list of collaborations for a given course ID.

        :calls: `GET /api/v1/courses/:course_id/collaborations \
        <https://canvas.instructure.com/doc/api/collaborations.html#method.collaborations.api_index>`_

        :rtype: :class:`canvasapi.collaboration.Collaboration`
        """
        return PaginatedList(
            Collaboration,
            self._requester,
            "GET",
            "courses/{}/collaborations".format(self.id),
            _root="collaborations",
            kwargs=combine_kwargs(**kwargs),
        )

    def get_content_export(self, content_export, **kwargs):
        """
        Return information about a single content export.

        :calls: `GET /api/v1/courses/:course_id/content_exports/:id\
        <https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.show>`_

        :param content_export: The object or ID of the content export to show.
        :type content_export: int or :class:`canvasapi.content_export.ContentExport`

        :rtype: :class:`canvasapi.content_export.ContentExport`
        """
        from canvasapi.content_export import ContentExport

        export_id = obj_or_id(content_export, "content_export", (ContentExport,))

        response = self._requester.request(
            "GET",
            "courses/{}/content_exports/{}".format(self.id, export_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return ContentExport(self._requester, response.json())

    def get_content_exports(self, **kwargs):
        """
        Return a paginated list of the past and pending content export jobs for a course.

        :calls: `GET /api/v1/courses/:course_id/content_exports\
        <https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.content_export.ContentExport`
        """
        from canvasapi.content_export import ContentExport

        return PaginatedList(
            ContentExport,
            self._requester,
            "GET",
            "courses/{}/content_exports".format(self.id),
            kwargs=combine_kwargs(**kwargs),
        )

    def get_content_migration(self, content_migration, **kwargs):
        """
        Retrive a content migration by its ID

        :calls: `GET /api/v1/courses/:course_id/content_migrations/:id \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.show>`_

        :param content_migration: The object or ID of the content migration to retrieve.
        :type content_migration: int, str or :class:`canvasapi.content_migration.ContentMigration`

        :rtype: :class:`canvasapi.content_migration.ContentMigration`
        """
        from canvasapi.content_migration import ContentMigration

        migration_id = obj_or_id(
            content_migration, "content_migration", (ContentMigration,)
        )

        response = self._requester.request(
            "GET",
            "courses/{}/content_migrations/{}".format(self.id, migration_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"course_id": self.id})

        return ContentMigration(self._requester, response_json)

    def get_content_migrations(self, **kwargs):
        """
        List content migrations that the current account can view or manage.

        :calls: `GET /api/v1/courses/:course_id/content_migrations/ \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.content_migration.ContentMigration`
        """
        from canvasapi.content_migration import ContentMigration

        return PaginatedList(
            ContentMigration,
            self._requester,
            "GET",
            "courses/{}/content_migrations".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_course_level_assignment_data(self, **kwargs):
        """
        Return a list of assignments for the course sorted by due date

        :calls: `GET /api/v1/courses/:course_id/analytics/assignments \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_assignments>`_

        :rtype: dict
        """

        response = self._requester.request(
            "GET",
            "courses/{}/analytics/assignments".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()

    def get_course_level_participation_data(self, **kwargs):
        """
        Return page view hits and participation numbers grouped by day through the course's history

        :calls: `GET /api/v1/courses/:course_id/analytics/activity \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_participation>`_

        :rtype: dict
        """

        response = self._requester.request(
            "GET",
            "courses/{}/analytics/activity".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()

    def get_course_level_student_summary_data(self, **kwargs):
        """
        Return a summary of per-user access information for all students in a course

        :calls: `GET /api/v1/courses/:course_id/analytics/student_summaries \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_student_summaries>`_

        :rtype: dict
        """

        response = self._requester.request(
            "GET",
            "courses/{}/analytics/student_summaries".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()

    def get_custom_columns(self, **kwargs):
        """
        List of all the custom gradebook columns for a course.

        :calls: `GET /api/v1/courses/:course_id/custom_gradebook_columns \
        <https://canvas.instructure.com/doc/api/custom_gradebook_columns.html#method.custom_gradebook_columns_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.custom_gradebook_columns.CustomGradebookColumn`
        """
        return PaginatedList(
            CustomGradebookColumn,
            self._requester,
            "GET",
            "courses/{}/custom_gradebook_columns".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_discussion_topic(self, topic, **kwargs):
        """
        Return data on an individual discussion topic.

        :calls: `GET /api/v1/courses/:course_id/discussion_topics/:topic_id \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.show>`_

        :param topic: The object or ID of the discussion topic.
        :type topic: :class:`canvasapi.discussion_topic.DiscussionTopic` or int

        :rtype: :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        topic_id = obj_or_id(topic, "topic", (DiscussionTopic,))

        response = self._requester.request(
            "GET",
            "courses/{}/discussion_topics/{}".format(self.id, topic_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"course_id": self.id})

        return DiscussionTopic(self._requester, response_json)

    def get_discussion_topics(self, **kwargs):
        """
        Returns the paginated list of discussion topics for this course or group.

        :calls: `GET /api/v1/courses/:course_id/discussion_topics \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        return PaginatedList(
            DiscussionTopic,
            self._requester,
            "GET",
            "courses/{}/discussion_topics".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_enabled_features(self, **kwargs):
        """
        Lists all enabled features in a course.

        :calls: `GET /api/v1/courses/:course_id/features/enabled \
        <https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.enabled_features>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.feature.Feature`
        """
        return PaginatedList(
            Feature,
            self._requester,
            "GET",
            "courses/{}/features/enabled".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_enrollments(self, **kwargs):
        """
        List all of the enrollments in this course.

        :calls: `GET /api/v1/courses/:course_id/enrollments \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.enrollment.Enrollment`
        """
        from canvasapi.enrollment import Enrollment

        return PaginatedList(
            Enrollment,
            self._requester,
            "GET",
            "courses/{}/enrollments".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_epub_export(self, epub, **kwargs):
        """
        Get information about a single epub export.

        :calls: `GET /api/v1/courses/:course_id/epub_exports/:id\
        <https://canvas.instructure.com/doc/api/e_pub_exports.html#method.epub_exports.show>`_

        :param epub: Object or ID of ePub Export
        :type epub: int or :class:`canvasapi.course_epub_export.CourseEpubExport`

        :rtype: :class:`canvasapi.course_epub_export.CourseEpubExport`
        """

        epub_id = obj_or_id(epub, "epub", (CourseEpubExport,))

        response = self._requester.request(
            "GET",
            "courses/{}/epub_exports/{}".format(self.id, epub_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return CourseEpubExport(self._requester, response.json())

    def get_external_feeds(self, **kwargs):
        """
        Returns the list of External Feeds this course.

        :calls: `GET /api/v1/courses/:course_id/external_feeds \
        <https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.external_feed.ExternalFeed`
        """
        from canvasapi.external_feed import ExternalFeed

        return PaginatedList(
            ExternalFeed,
            self._requester,
            "GET",
            "courses/{}/external_feeds".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_external_tool(self, tool, **kwargs):
        """
        :calls: `GET /api/v1/courses/:course_id/external_tools/:external_tool_id \
        <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.show>`_

        :param tool: The object or ID of the tool to retrieve.
        :type tool: :class:`canvasapi.external_tool.ExternalTool` or int

        :rtype: :class:`canvasapi.external_tool.ExternalTool`
        """
        from canvasapi.external_tool import ExternalTool

        tool_id = obj_or_id(tool, "tool", (ExternalTool,))

        response = self._requester.request(
            "GET",
            "courses/{}/external_tools/{}".format(self.id, tool_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        tool_json = response.json()
        tool_json.update({"course_id": self.id})

        return ExternalTool(self._requester, tool_json)

    def get_external_tools(self, **kwargs):
        """
        :calls: `GET /api/v1/courses/:course_id/external_tools \
        <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.external_tool.ExternalTool`
        """
        from canvasapi.external_tool import ExternalTool

        return PaginatedList(
            ExternalTool,
            self._requester,
            "GET",
            "courses/{}/external_tools".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_feature_flag(self, feature, **kwargs):
        """
        Return the feature flag that applies to given course.

        :calls: `GET /api/v1/courses/:course_id/features/flags/:feature \
        <https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.show>`_

        :param feature: The feature object or name of the feature to retrieve.
        :type feature: :class:`canvasapi.feature.Feature` or str

        :rtype: :class:`canvasapi.feature.FeatureFlag`
        """
        feature_name = obj_or_str(feature, "name", (Feature,))

        response = self._requester.request(
            "GET",
            "courses/{}/features/flags/{}".format(self.id, feature_name),
            _kwargs=combine_kwargs(**kwargs),
        )
        return FeatureFlag(self._requester, response.json())

    def get_features(self, **kwargs):
        """
        Lists all features of a course.

        :calls: `GET /api/v1/courses/:course_id/features \
        <https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.feature.Feature`
        """
        return PaginatedList(
            Feature,
            self._requester,
            "GET",
            "courses/{}/features".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_file(self, file, **kwargs):
        """
        Return the standard attachment json object for a file.

        :calls: `GET /api/v1/courses/:course_id/files/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_show>`_

        :param file: The object or ID of the file to retrieve.
        :type file: :class:`canvasapi.file.File` or int

        :rtype: :class:`canvasapi.file.File`
        """
        from canvasapi.file import File

        file_id = obj_or_id(file, "file", (File,))

        response = self._requester.request(
            "GET",
            "courses/{}/files/{}".format(self.id, file_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return File(self._requester, response.json())

    def get_file_quota(self, **kwargs):
        """
        Returns the total and used storage quota for the course.

        :calls: `GET /api/v1/courses/:course_id/files/quota \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_quota>`_

        :rtype: dict
        """

        response = self._requester.request(
            "GET",
            "courses/{}/files/quota".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()

    def get_files(self, **kwargs):
        """
        Returns the paginated list of files for the course.

        :calls: `GET /api/v1/courses/:course_id/files \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.file.File`
        """
        from canvasapi.file import File

        return PaginatedList(
            File,
            self._requester,
            "GET",
            "courses/{}/files".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_folder(self, folder, **kwargs):
        """
        Returns the details for a course folder

        :calls: `GET /api/v1/courses/:course_id/folders/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.show>`_

        :param folder: The object or ID of the folder to retrieve.
        :type folder: :class:`canvasapi.folder.Folder` or int

        :rtype: :class:`canvasapi.folder.Folder`
        """
        folder_id = obj_or_id(folder, "folder", (Folder,))

        response = self._requester.request(
            "GET",
            "courses/{}/folders/{}".format(self.id, folder_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Folder(self._requester, response.json())

    def get_folders(self, **kwargs):
        """
        Returns the paginated list of all folders for the given course. This will be returned as a
        flat list containing all subfolders as well.

        :calls: `GET /api/v1/courses/:course_id/folders \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.list_all_folders>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.folder.Folder`
        """
        return PaginatedList(
            Folder,
            self._requester,
            "GET",
            "courses/{}/folders".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_full_discussion_topic(self, topic, **kwargs):
        """
        Return a cached structure of the discussion topic.

        :calls: `GET /api/v1/courses/:course_id/discussion_topics/:topic_id/view \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.view>`_

        :param topic: The object or ID of the discussion topic.
        :type topic: :class:`canvasapi.discussion_topic.DiscussionTopic` or int

        :rtype: dict
        """
        topic_id = obj_or_id(topic, "topic", (DiscussionTopic,))

        response = self._requester.request(
            "GET",
            "courses/{}/discussion_topics/{}/view".format(self.id, topic_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_gradebook_history_dates(self, **kwargs):
        """
        Returns a map of dates to grader/assignment groups

        :calls: `GET /api/v1/courses/:course_id/gradebook_history/days\
        <https://canvas.instructure.com/doc/api/gradebook_history.html#method.gradebook_history_api.days>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.grading_history.Day`
        """

        return PaginatedList(
            Day,
            self._requester,
            "GET",
            "courses/{}/gradebook_history/days".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_gradebook_history_details(self, date, **kwargs):
        """
        Returns the graders who worked on this day, along with the
        assignments they worked on. More details can be obtained by
        selecting a grader and assignment and calling the 'submissions'
        api endpoint for a given date.

        :calls: `GET /api/v1/courses/:course_id/gradebook_history/:date\
        <https://canvas.instructure.com/doc/api/gradebook_history.html#method.\
        gradebook_history_api.day_details>`_

        :param date: The date for which you would like to see detailed information.
        :type date: int

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.gradebook_history.Grader`
        """

        return PaginatedList(
            Grader,
            self._requester,
            "GET",
            "courses/{}/gradebook_history/{}".format(self.id, date),
            kwargs=combine_kwargs(**kwargs),
        )

    def get_grading_period(self, grading_period, **kwargs):
        """
        Return a single grading period for the associated course and id.

        :calls: `GET /api/v1/courses/:course_id/grading_periods/:id\
        <https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.index>`_
        :param grading_period_id: The ID of the rubric.
        :type grading_period_id: int

        :rtype: :class:`canvasapi.grading_period.GradingPeriod`
        """

        response = self._requester.request(
            "GET",
            "courses/{}/grading_periods/{}".format(self.id, grading_period),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_grading_period = response.json()["grading_periods"][0]
        response_grading_period.update({"course_id": self.id})

        return GradingPeriod(self._requester, response_grading_period)

    def get_grading_periods(self, **kwargs):
        """
        Return a list of grading periods for the associated course.

        :calls: `GET /api/v1/courses/:course_id/grading_periods\
        <https://canvas.instructure.com/doc/api/grading_periods.html#method.grading_periods.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.grading_period.GradingPeriod`
        """

        return PaginatedList(
            GradingPeriod,
            self._requester,
            "GET",
            "courses/{}/grading_periods".format(self.id),
            {"course_id": self.id},
            _root="grading_periods",
            kwargs=combine_kwargs(**kwargs),
        )

    def get_grading_standards(self, **kwargs):
        """
        Get a PaginatedList of the grading standards available for the course

        :calls: `GET /api/v1/courses/:course_id/grading_standards \
        <https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.grading_standards.GradingStandard`
        """
        return PaginatedList(
            GradingStandard,
            self._requester,
            "GET",
            "courses/%s/grading_standards" % (self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_group_categories(self, **kwargs):
        """
        List group categories for a context.

        :calls: `GET /api/v1/courses/:course_id/group_categories \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.group.GroupCategory`
        """
        from canvasapi.group import GroupCategory

        return PaginatedList(
            GroupCategory,
            self._requester,
            "GET",
            "courses/{}/group_categories".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_groups(self, **kwargs):
        """
        Return list of active groups for the specified course.

        :calls: `GET /api/v1/courses/:course_id/groups \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.context_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.Course`
        """
        from canvasapi.group import Group

        return PaginatedList(
            Group,
            self._requester,
            "GET",
            "courses/{}/groups".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_late_policy(self, **kwargs):
        """
        Returns the late policy for a course.

        :calls: `GET /api/v1/courses/:id/late_policy \
        <https://canvas.instructure.com/doc/api/late_policy.html#method.late_policy.show>`_

        :rtype: :class:`canvasapi.course.LatePolicy`
        """

        response = self._requester.request(
            "GET",
            "courses/{}/late_policy".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        late_policy_json = response.json()

        return LatePolicy(self._requester, late_policy_json["late_policy"])

    def get_licenses(self, **kwargs):
        """
        Returns a paginated list of the licenses that can be applied to the
        files under the course scope

        :calls: `GET /api/v1/course/:course_id/content_licenses \
        <https://canvas.instructure.com/doc/api/files.html#method.usage_rights.licenses>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.license.License`
        """

        return PaginatedList(
            License,
            self._requester,
            "GET",
            "courses/{}/content_licenses".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_migration_systems(self, **kwargs):
        """
        Return a list of migration systems.

        :calls: `GET /api/v1/courses/:course_id/content_migrations/migrators \
        <https://canvas.instructure.com/doc/api/content_migrations.html#method.content_migrations.available_migrators>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.content_migration.Migrator`
        """
        from canvasapi.content_migration import Migrator

        return PaginatedList(
            Migrator,
            self._requester,
            "GET",
            "courses/{}/content_migrations/migrators".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_module(self, module, **kwargs):
        """
        Retrieve a single module by ID.

        :calls: `GET /api/v1/courses/:course_id/modules/:id \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.show>`_

        :param module: The object or ID of the module to retrieve.
        :type module: :class:`canvasapi.module.Module` or int

        :rtype: :class:`canvasapi.module.Module`
        """
        from canvasapi.module import Module

        module_id = obj_or_id(module, "module", (Module,))

        response = self._requester.request(
            "GET", "courses/{}/modules/{}".format(self.id, module_id)
        )
        module_json = response.json()
        module_json.update({"course_id": self.id})

        return Module(self._requester, module_json)

    def get_modules(self, **kwargs):
        """
        Return a list of modules in this course.

        :calls: `GET /api/v1/courses/:course_id/modules \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.module.Module`
        """
        from canvasapi.module import Module

        return PaginatedList(
            Module,
            self._requester,
            "GET",
            "courses/{}/modules".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_multiple_submissions(self, **kwargs):
        """
        List submissions for multiple assignments.
        Get all existing submissions for a given set of students and assignments.

        :calls: `GET /api/v1/courses/:course_id/students/submissions \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.submission.Submission`
        """

        is_grouped = kwargs.get("grouped", False)

        if normalize_bool(is_grouped, "grouped"):
            cls = GroupedSubmission
        else:
            cls = Submission

        return PaginatedList(
            cls,
            self._requester,
            "GET",
            "courses/{}/students/submissions".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_outcome_group(self, group, **kwargs):
        """
        Returns the details of the Outcome Group with the given id.

        :calls: `GET /api/v1/courses/:course_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show>`_

        :param group: The outcome group object or ID to return.
        :type group: :class:`canvasapi.outcome.OutcomeGroup` or int

        :returns: An outcome group object.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        from canvasapi.outcome import OutcomeGroup

        outcome_group_id = obj_or_id(group, "group", (OutcomeGroup,))

        response = self._requester.request(
            "GET", "courses/{}/outcome_groups/{}".format(self.id, outcome_group_id)
        )

        return OutcomeGroup(self._requester, response.json())

    def get_outcome_groups_in_context(self, **kwargs):
        """
        Get all outcome groups for context - BETA

        :calls: `GET /api/v1/courses/:course_id/outcome_groups \
        <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.index>`_

        :returns: Paginated List of OutcomesGroups in the context.
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.outcome.OutcomeGroups`
        """
        from canvasapi.outcome import OutcomeGroup

        return PaginatedList(
            OutcomeGroup,
            self._requester,
            "GET",
            "courses/{}/outcome_groups".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_outcome_import_status(self, outcome_import, **kwargs):
        """
        Get the status of an already created Outcome import.
        Pass 'latest' for the outcome import id for the latest import.

        :calls: `GET /api/v1/courses/:course_id/outcome_imports/:id \
        <https://canvas.instructure.com/doc/api/outcome_imports.html#method.outcome_imports_api.show>`_

        :param outcome_import: The outcome import object or ID to get the status of.
        :type outcome_import: :class:`canvasapi.outcome_import.OutcomeImport`,
            int, or string: "latest"

        :rtype: :class:`canvasapi.outcome_import.OutcomeImport`
        """
        if outcome_import == "latest":
            outcome_import_id = "latest"
        else:
            outcome_import_id = obj_or_id(
                outcome_import, "outcome_import", (OutcomeImport,)
            )

        response = self._requester.request(
            "GET",
            "courses/{}/outcome_imports/{}".format(self.id, outcome_import_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"course_id": self.id})

        return OutcomeImport(self._requester, response_json)

    def get_outcome_result_rollups(self, **kwargs):
        """
        Get all outcome result rollups for context - BETA

        :calls: `GET /api/v1/courses/:course_id/outcome_rollups \
        <https://canvas.instructure.com/doc/api/outcome_results.html#method.outcome_results.rollups>`_

        :returns: List of outcome result rollups in the context.
        :rtype: dict
        """
        response = self._requester.request(
            "GET",
            "courses/{}/outcome_rollups".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()

    def get_outcome_results(self, **kwargs):
        """
        Get all outcome results for context - BETA

        :calls: `GET /api/v1/courses/:course_id/outcome_results \
        <https://canvas.instructure.com/doc/api/outcome_results.html#method.outcome_results.index>`_

        :returns: List of potential related outcome result dicts.
        :rtype: dict
        """
        response = self._requester.request(
            "GET",
            "courses/{}/outcome_results".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()

    def get_page(self, url, **kwargs):
        """
        Retrieve the contents of a wiki page.

        :calls: `GET /api/v1/courses/:course_id/pages/:url \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show>`_

        :param url: The url for the page.
        :type url: str
        :returns: The specified page.
        :rtype: :class:`canvasapi.page.Page`
        """

        response = self._requester.request(
            "GET",
            "courses/{}/pages/{}".format(self.id, url),
            _kwargs=combine_kwargs(**kwargs),
        )
        page_json = response.json()
        page_json.update({"course_id": self.id})

        return Page(self._requester, page_json)

    def get_pages(self, **kwargs):
        """
        List the wiki pages associated with a course.

        :calls: `GET /api/v1/courses/:course_id/pages \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.page.Page`
        """
        return PaginatedList(
            Page,
            self._requester,
            "GET",
            "courses/{}/pages".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_quiz(self, quiz, **kwargs):
        """
        Return the quiz with the given id.

        :calls: `GET /api/v1/courses/:course_id/quizzes/:id \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.show>`_

        :param quiz: The object or ID of the quiz to retrieve.
        :type quiz: :class:`canvasapi.quiz.Quiz` or int

        :rtype: :class:`canvasapi.quiz.Quiz`
        """
        from canvasapi.quiz import Quiz

        quiz_id = obj_or_id(quiz, "quiz", (Quiz,))

        response = self._requester.request(
            "GET",
            "courses/{}/quizzes/{}".format(self.id, quiz_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        quiz_json = response.json()
        quiz_json.update({"course_id": self.id})

        return Quiz(self._requester, quiz_json)

    def get_quiz_overrides(self, **kwargs):
        """
        Retrieve the actual due-at, unlock-at,
        and available-at dates for quizzes based on
        the assignment overrides active for the current API user.

        :calls: `GET /api/v1/courses/:course_id/quizzes/assignment_overrides \
        <https://canvas.instructure.com/doc/api/quiz_assignment_overrides.html#method.quizzes/quiz_assignment_overrides.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.quiz.QuizAssignmentOverrideSet`
        """
        from canvasapi.quiz import QuizAssignmentOverrideSet

        return PaginatedList(
            QuizAssignmentOverrideSet,
            self._requester,
            "GET",
            "courses/{}/quizzes/assignment_overrides".format(self.id),
            _root="quiz_assignment_overrides",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_quizzes(self, **kwargs):
        """
        Return a list of quizzes belonging to this course.

        :calls: `GET /api/v1/courses/:course_id/quizzes \
        <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.quiz.Quiz`
        """
        from canvasapi.quiz import Quiz

        return PaginatedList(
            Quiz,
            self._requester,
            "GET",
            "courses/{}/quizzes".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_recent_students(self, **kwargs):
        """
        Return a list of students in the course ordered by how recently they
        have logged in.

        :calls: `GET /api/v1/courses/:course_id/recent_students \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.recent_students>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

        return PaginatedList(
            User,
            self._requester,
            "GET",
            "courses/{}/recent_students".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_root_outcome_group(self, **kwargs):
        """
        Redirect to root outcome group for context

        :calls: `GET /api/v1/courses/:course_id/root_outcome_group \
        <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.redirect>`_

        :returns: The OutcomeGroup of the context.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        from canvasapi.outcome import OutcomeGroup

        response = self._requester.request(
            "GET",
            "courses/{}/root_outcome_group".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return OutcomeGroup(self._requester, response.json())

    def get_rubric(self, rubric_id, **kwargs):
        """
        Get a single rubric, based on rubric id.

        :calls: `GET /api/v1/courses/:course_id/rubrics/:id \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.show>`_

        :param rubric_id: The ID of the rubric.
        :type rubric_id: int
        :rtype: :class:`canvasapi.rubric.Rubric`
        """
        response = self._requester.request(
            "GET",
            "courses/%s/rubrics/%s" % (self.id, rubric_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return Rubric(self._requester, response.json())

    def get_rubrics(self, **kwargs):
        """
        Get the paginated list of active rubrics for the current course.

        :calls: `GET /api/v1/courses/:course_id/rubrics \
        <https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.rubric.Rubric`
        """
        return PaginatedList(
            Rubric,
            self._requester,
            "GET",
            "courses/%s/rubrics" % (self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_section(self, section, **kwargs):
        """
        Retrieve a section.

        :calls: `GET /api/v1/courses/:course_id/sections/:id \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.show>`_

        :param section: The object or ID of the section to retrieve.
        :type section: :class:`canvasapi.section.Section` or int

        :rtype: :class:`canvasapi.section.Section`
        """
        from canvasapi.section import Section

        section_id = obj_or_id(section, "section", (Section,))

        response = self._requester.request(
            "GET",
            "courses/{}/sections/{}".format(self.id, section_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Section(self._requester, response.json())

    def get_sections(self, **kwargs):
        """
        List all sections in a course.

        :calls: `GET /api/v1/courses/:course_id/sections \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.section.Section`
        """
        from canvasapi.section import Section

        return PaginatedList(
            Section,
            self._requester,
            "GET",
            "courses/{}/sections".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_settings(self, **kwargs):
        """
        Returns this course's settings.

        :calls: `GET /api/v1/courses/:course_id/settings \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.settings>`_

        :rtype: dict
        """
        response = self._requester.request(
            "GET",
            "courses/{}/settings".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_single_grading_standard(self, grading_standard_id, **kwargs):
        """
        Get a single grading standard from the course.

        :calls: `GET /api/v1/courses/:course_id/grading_standards/:grading_standard_id \
        <https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_show>`_

        :param grading_standard_id: The grading standard id
        :type grading_standard_id: int
        :rtype: :class:`canvasapi.grading_standards.GradingStandard`
        """

        response = self._requester.request(
            "GET",
            "courses/%s/grading_standards/%d" % (self.id, grading_standard_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return GradingStandard(self._requester, response.json())

    def get_submission_history(self, date, grader_id, assignment_id, **kwargs):
        """
        Gives a nested list of submission versions.

        :calls: `GET /api/v1/courses/:course_id/gradebook_history/:date/graders\
        /:grader_id/assignments/:assignment_id/submissions\
        <https://canvas.instructure.com/doc/api/gradebook_history.html#method.\
        gradebook_history_api.submissions>`_

        :param date: The date for which you would like to see submissions
        :type grader_id: str
        :param grader_id: The ID of the grader for which you want to see submissions.
        :type grader_id: int
        :param assignment_id: The ID of the assignment for which you want to see submissions
        :type assignment_id: int

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.gradebook_history.SubmissionHistory`
        """

        return PaginatedList(
            SubmissionHistory,
            self._requester,
            "GET",
            "courses/{}/gradebook_history/{}/graders/{}/assignments/{}/submissions".format(
                self.id, date, grader_id, assignment_id
            ),
            kwargs=combine_kwargs(**kwargs),
        )

    def get_tabs(self, **kwargs):
        """
        List available tabs for a course.
        Returns a list of navigation tabs available in the current context.

        :calls: `GET /api/v1/courses/:course_id/tabs \
        <https://canvas.instructure.com/doc/api/tabs.html#method.tabs.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.tab.Tab`
        """
        return PaginatedList(
            Tab,
            self._requester,
            "GET",
            "courses/{}/tabs".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_todo_items(self, **kwargs):
        """
        Returns the current user's course-specific todo items.

        :calls: `GET /api/v1/courses/:course_id/todo \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.todo_items>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.todo.Todo`
        """

        return PaginatedList(
            Todo,
            self._requester,
            "GET",
            "courses/{}/todo".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_uncollated_submissions(self, **kwargs):
        """
        Gives a paginated, uncollated list of submission versions for all matching
        submissions in the context. This SubmissionVersion objects will not include
        the new_grade or previous_grade keys, only the grade; same for graded_at
        and grader.

        :calls: `GET /api/v1/courses/:course_id/gradebook_history/feed\
        <https://canvas.instructure.com/doc/api/gradebook_history.html#method\
        .gradebook_history_api.feed>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.gradebook_history.SubmissionVersion`
        """

        return PaginatedList(
            SubmissionVersion,
            self._requester,
            "GET",
            "courses/{}/gradebook_history/feed".format(self.id),
            kwargs=combine_kwargs(**kwargs),
        )

    def get_user(self, user, user_id_type=None, **kwargs):
        """
        Retrieve a user by their ID. `user_id_type` denotes which endpoint to try as there are
        several different ids that can pull the same user record from Canvas.

        :calls: `GET /api/v1/courses/:course_id/users/:id \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.user>`_

        :param user: The object or ID of the user to retrieve.
        :type user: :class:`canvasapi.user.User` or int
        :param user_id_type: The type of the ID to search for.
        :type user_id_type: str

        :rtype: :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

        if user_id_type:
            uri = "courses/{}/users/{}:{}".format(self.id, user_id_type, user)
        else:
            user_id = obj_or_id(user, "user", (User,))
            uri = "courses/{}/users/{}".format(self.id, user_id)

        response = self._requester.request("GET", uri, _kwargs=combine_kwargs(**kwargs))
        return User(self._requester, response.json())

    def get_user_in_a_course_level_assignment_data(self, user, **kwargs):
        """
        Return a list of assignments for the course sorted by due date

        :calls: `GET /api/v1/courses/:course_id/analytics/users/:student_id/assignments \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_assignments>`_

        :param user: The object or ID of the related user
        :type user: :class:`canvasapi.user.User` or int

        :rtype: dict
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            "GET",
            "courses/{}/analytics/users/{}/assignments".format(self.id, user_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()

    def get_user_in_a_course_level_messaging_data(self, user, **kwargs):
        """
        Return messaging hits grouped by day through the entire history of the course

        :calls: `GET /api/v1/courses/:course_id/analytics/users/:student_id/communication \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_messaging>`_

        :param user: The object or ID of the related user
        :type user: :class:`canvasapi.user.User` or int

        :rtype: dict
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            "GET",
            "courses/{}/analytics/users/{}/communication".format(self.id, user_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()

    def get_user_in_a_course_level_participation_data(self, user, **kwargs):
        """
        Return page view hits grouped by hour and participation details through course's history

        :calls: `GET /api/v1/courses/:course_id/analytics/users/:student_id/activity \
        <https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_participation>`_

        :param user: The object or ID of the related user
        :type user: :class:`canvasapi.user.User` or int

        :rtype: dict
        """
        from canvasapi.user import User

        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            "GET",
            "courses/{}/analytics/users/{}/activity".format(self.id, user_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()

    def get_users(self, **kwargs):
        """
        List all users in a course.

        :calls: `GET /api/v1/courses/:course_id/search_users \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.users>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.user.User`
        """
        from canvasapi.user import User

        return PaginatedList(
            User,
            self._requester,
            "GET",
            "courses/{}/search_users".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def import_outcome(self, attachment, **kwargs):
        """
        Import outcome into canvas.

        :calls: `POST /api/v1/courses/:course_id/outcome_imports \
        <https://canvas.instructure.com/doc/api/outcome_imports.html#method.outcome_imports_api.create>`_

        :param attachment: A file handler or path of the file to import.
        :type attachment: file or str

        :rtype: :class:`canvasapi.outcome_import.OutcomeImport`
        """

        attachment, is_path = file_or_path(attachment)

        try:
            response = self._requester.request(
                "POST",
                "courses/{}/outcome_imports".format(self.id),
                file={"attachment": attachment},
                _kwargs=combine_kwargs(**kwargs),
            )

            response_json = response.json()
            response_json.update({"course_id": self.id})

            return OutcomeImport(self._requester, response_json)
        finally:
            if is_path:
                attachment.close()

    def list_blueprint_subscriptions(self, **kwargs):
        """
        Return a list of blueprint subscriptions for the given course.

        :calls: `GET /api/v1/courses/:course_id/blueprint_subscriptions\
        <https://canvas.instructure.com/doc/api/blueprint_courses.html#method.\
        master_courses/master_templates.subscriptions_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.blueprint.BlueprintSubscription`
        """

        return PaginatedList(
            BlueprintSubscription,
            self._requester,
            "GET",
            "courses/{}/blueprint_subscriptions".format(self.id),
            {"course_id": self.id},
            kwargs=combine_kwargs(**kwargs),
        )

    def preview_html(self, html, **kwargs):
        """
        Preview HTML content processed for this course.

        :calls: `POST /api/v1/courses/:course_id/preview_html \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.preview_html>`_

        :param html: The HTML code to preview.
        :type html: str
        :rtype: str
        """
        kwargs["html"] = html

        response = self._requester.request(
            "POST",
            "courses/{}/preview_html".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json().get("html", "")

    def remove_usage_rights(self, **kwargs):
        """
        Removes the usage rights for specified files that are under the current course scope

        :calls: `DELETE /api/v1/courses/:course_id/usage_rights \
        <https://canvas.instructure.com/doc/api/files.html#method.usage_rights.remove_usage_rights>`_

        :rtype: dict
        """

        response = self._requester.request(
            "DELETE",
            "courses/{}/usage_rights".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()

    def reorder_pinned_topics(self, order, **kwargs):
        """
        Puts the pinned discussion topics in the specified order.
        All pinned topics should be included.

        :calls: `POST /api/v1/courses/:course_id/discussion_topics/reorder \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.reorder>`_

        :param order: The ids of the pinned discussion topics in the desired order.
            e.g. [104, 102, 103], (104, 102, 103), or "104,102,103"
        :type order: string or iterable sequence of values

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        # Convert iterable sequence to comma-separated string
        if is_multivalued(order):
            order = ",".join([str(topic_id) for topic_id in order])

        # Check if is a string with commas
        if not isinstance(order, str) or "," not in order:
            raise ValueError("Param `order` must be a list, tuple, or string.")

        kwargs["order"] = order

        response = self._requester.request(
            "POST",
            "courses/{}/discussion_topics/reorder".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json().get("reorder")

    def reset(self, **kwargs):
        """
        Delete the current course and create a new equivalent course
        with no content, but all sections and users moved over.

        :calls: `POST /api/v1/courses/:course_id/reset_content \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.reset_content>`_

        :rtype: :class:`canvasapi.course.Course`
        """
        response = self._requester.request(
            "POST",
            "courses/{}/reset_content".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Course(self._requester, response.json())

    def resolve_path(self, full_path=None, **kwargs):
        """
        Returns the paginated list of all of the folders in the given
        path starting at the course root folder. Returns root folder if called
        with no arguments.

        :calls: `GET /api/v1/courses/:course_id/folders/by_path/*full_path \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.resolve_path>`_

        :param full_path: Full path to resolve, relative to course root.
        :type full_path: string

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.folder.Folder`
        """

        if full_path:
            return PaginatedList(
                Folder,
                self._requester,
                "GET",
                "courses/{0}/folders/by_path/{1}".format(self.id, full_path),
                _kwargs=combine_kwargs(**kwargs),
            )
        else:
            return PaginatedList(
                Folder,
                self._requester,
                "GET",
                "courses/{0}/folders/by_path".format(self.id),
                _kwargs=combine_kwargs(**kwargs),
            )

    def set_quiz_extensions(self, quiz_extensions, **kwargs):
        """
        Set extensions for student all quiz submissions in a course.

        :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/extensions
            <https://canvas.instructure.com/doc/api/quiz_extensions.html#method.quizzes/quiz_extensions.create>`_

        :param quiz_extensions: List of dictionaries representing extensions.
        :type quiz_extensions: list

        :rtype: list of :class:`canvasapi.quiz.QuizExtension`

        Example Usage:

        >>> course.set_quiz_extensions([
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
            "courses/{}/quiz_extensions".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        extension_list = response.json()["quiz_extensions"]
        return [
            QuizExtension(self._requester, extension) for extension in extension_list
        ]

    def set_usage_rights(self, **kwargs):
        """
        Changes the usage rights for specified files that are under the current course scope

        :calls: `PUT /api/v1/courses/:course_id/usage_rights \
        <https://canvas.instructure.com/doc/api/files.html#method.usage_rights.set_usage_rights>`_

        :rtype: :class:`canvasapi.usage_rights.UsageRights`
        """

        response = self._requester.request(
            "PUT",
            "courses/{}/usage_rights".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return UsageRights(self._requester, response.json())

    def show_front_page(self, **kwargs):
        """
        Retrieve the content of the front page.

        :calls: `GET /api/v1/courses/:course_id/front_page \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_front_page>`_

        :rtype: :class:`canvasapi.course.Course`
        """
        response = self._requester.request(
            "GET",
            "courses/{}/front_page".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        page_json = response.json()
        page_json.update({"course_id": self.id})

        return Page(self._requester, page_json)

    def submissions_bulk_update(self, **kwargs):
        """
        Update the grading and comments on multiple student's assignment
        submissions in an asynchronous job.

        :calls: `POST /api/v1/courses/:course_id/submissions/update_grades \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.bulk_update>`_

        :rtype: :class:`canvasapi.progress.Progress`
        """
        response = self._requester.request(
            "POST",
            "courses/{}/submissions/update_grades".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Progress(self._requester, response.json())

    def update(self, **kwargs):
        """
        Update this course.

        :calls: `PUT /api/v1/courses/:id \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.update>`_

        :returns: `True` if the course was updated, `False` otherwise.
        :rtype: `bool`
        """
        response = self._requester.request(
            "PUT", "courses/{}".format(self.id), _kwargs=combine_kwargs(**kwargs)
        )

        if response.json().get("name"):
            super(Course, self).set_attributes(response.json())

        return response.json().get("name")

    def update_assignment_overrides(self, assignment_overrides, **kwargs):
        """
        Update a list of specified overrides for each assignment.

        Note: All current overridden values must be supplied if they are to be retained.

        :calls: `PUT /api/v1/courses/:course_id/assignments/overrides \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.batch_update>`_

        :param assignment_overrides: Attributes for the updated assignment overrides.
        :type assignment_overrides: list

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.assignment.AssignmentOverride`
        """
        from canvasapi.assignment import AssignmentOverride

        kwargs["assignment_overrides"] = assignment_overrides

        return PaginatedList(
            AssignmentOverride,
            self._requester,
            "PUT",
            "courses/{}/assignments/overrides".format(self.id),
            {"course_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def update_settings(self, **kwargs):
        """
        Update a course's settings.

        :calls: `PUT /api/v1/courses/:course_id/settings \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.update_settings>`_

        :rtype: dict
        """
        response = self._requester.request(
            "PUT", "courses/{}/settings".format(self.id), **kwargs
        )
        return response.json()

    def upload(self, file: FileOrPathLike, **kwargs):
        """
        Upload a file to this course.

        :calls: `POST /api/v1/courses/:course_id/files \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.create_file>`_

        :param file: The file or path of the file to upload.
        :type file: file or str
        :returns: True if the file uploaded successfully, False otherwise, \
                    and the JSON response from the API.
        :rtype: tuple
        """
        return Uploader(
            self._requester, "courses/{}/files".format(self.id), file, **kwargs
        ).start()


class CourseNickname(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.nickname, self.course_id)

    def remove(self, **kwargs):
        """
        Remove the nickname for the given course. Subsequent course API
        calls will return the actual name for the course.

        :calls: `DELETE /api/v1/users/self/course_nicknames/:course_id \
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.delete>`_

        :rtype: :class:`canvasapi.course.CourseNickname`
        """
        response = self._requester.request(
            "DELETE",
            "users/self/course_nicknames/{}".format(self.course_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return CourseNickname(self._requester, response.json())


class LatePolicy(CanvasObject):
    def __str__(self):
        return "Late Policy {}".format(self.id)
