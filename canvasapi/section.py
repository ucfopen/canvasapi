from canvasapi.canvas_object import CanvasObject
from canvasapi.enrollment import Enrollment
from canvasapi.paginated_list import PaginatedList
from canvasapi.progress import Progress
from canvasapi.submission import GroupedSubmission, Submission
from canvasapi.user import User
from canvasapi.util import combine_kwargs, normalize_bool, obj_or_id


class Section(CanvasObject):
    def __str__(self):
        return "{} - {} ({})".format(self.name, self.course_id, self.id)

    def cross_list_section(self, new_course, **kwargs):
        """
        Move the Section to another course.

        :calls: `POST /api/v1/sections/:id/crosslist/:new_course_id \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.crosslist>`_

        :param new_course: The object or ID of the new course.
        :type new_course: :class:`canvasapi.course.Course` or int

        :rtype: :class:`canvasapi.section.Section`
        """
        from canvasapi.course import Course

        new_course_id = obj_or_id(new_course, "new_course", (Course,))

        response = self._requester.request(
            "POST",
            "sections/{}/crosslist/{}".format(self.id, new_course_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Section(self._requester, response.json())

    def decross_list_section(self, **kwargs):
        """
        Undo cross-listing of a section.

        :calls: `DELETE /api/v1/sections/:id/crosslist \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.uncrosslist>`_

        :rtype: :class:`canvasapi.section.Section`
        """
        response = self._requester.request(
            "DELETE",
            "sections/{}/crosslist".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Section(self._requester, response.json())

    def delete(self, **kwargs):
        """
        Delete a target section.

        :calls: `DELETE /api/v1/sections/:id \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.destroy>`_

        :rtype: :class:`canvasapi.section.Section`
        """
        response = self._requester.request(
            "DELETE", "sections/{}".format(self.id), _kwargs=combine_kwargs(**kwargs)
        )
        return Section(self._requester, response.json())

    def edit(self, **kwargs):
        """
        Edit contents of a target section.

        :calls: `PUT /api/v1/sections/:id \
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.update>`_

        :rtype: :class:`canvasapi.section.Section`
        """
        response = self._requester.request(
            "PUT", "sections/{}".format(self.id), _kwargs=combine_kwargs(**kwargs)
        )

        if "name" in response.json():
            super(Section, self).set_attributes(response.json())

        return self

    def enroll_user(self, user, **kwargs):
        """
        Create a new user enrollment for a course or a section.

        :calls: `POST /api/v1/section/:section_id/enrollments \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.create>`_

        :param user: The object or ID of the user to enroll in this course.
        :type user: :class:`canvasapi.user.User` or int
        :rtype: :class:`canvasapi.enrollment.Enrollment`
        """

        kwargs["enrollment[user_id]"] = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            "POST",
            "sections/{}/enrollments".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return Enrollment(self._requester, response.json())

    def get_assignment_override(self, assignment, **kwargs):
        """
        Return override for the specified assignment for this section.

        :param assignment: The assignment to get an override for
        :type assignment: :class:`canvasapi.assignment.Assignment` or int

        :calls: `GET /api/v1/sections/:course_section_id/assignments/:assignment_id/override \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.section_alias>`_

        :rtype: :class:`canvasapi.assignment.AssignmentOverride`
        """
        from canvasapi.assignment import Assignment, AssignmentOverride

        assignment_id = obj_or_id(assignment, "assignment", (Assignment,))

        response = self._requester.request(
            "GET", "sections/{}/assignments/{}/override".format(self.id, assignment_id)
        )
        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        return AssignmentOverride(self._requester, response_json)

    def get_enrollments(self, **kwargs):
        """
        List all of the enrollments for the current user.

        :calls: `GET /api/v1/sections/:section_id/enrollments \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.enrollment.Enrollment`
        """
        from canvasapi.enrollment import Enrollment

        return PaginatedList(
            Enrollment,
            self._requester,
            "GET",
            "sections/{}/enrollments".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_multiple_submissions(self, **kwargs):
        """
        List submissions for multiple assignments.
        Get all existing submissions for a given set of students and assignments.

        :calls: `GET /api/v1/sections/:section_id/students/submissions \
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
            "sections/{}/students/submissions".format(self.id),
            {"section_id": self.id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def submissions_bulk_update(self, **kwargs):
        """
        Update the grading and comments on multiple student's assignment
        submissions in an asynchronous job.

        :calls: `POST /api/v1/sections/:section_id/submissions/update_grades \
        <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.bulk_update>`_

        :rtype: :class:`canvasapi.progress.Progress`
        """
        response = self._requester.request(
            "POST",
            "sections/{}/submissions/update_grades".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Progress(self._requester, response.json())
