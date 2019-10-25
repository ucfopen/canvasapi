from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs

@python_2_unicode_compatible
class Grader(CanvasObject):
    def __str__(self):
        return "{}".format(self.id)

    def list_submissions(self):
        pass

@python_2_unicode_compatible
class Day(CanvasObject):
    def __str__(self):
        return "{}".format(self.date)

@python_2_unicode_compatible
class SubmissionVersion(CanvasObject):
    def __str__(self):
        return "{} {}".format(self.assignment_id, self.id)

    def get_submissions(self, grader_id, assignment_id, **kwargs):
        """
        Gives a nested list of submission versions.

        :calls: `GET /api/v1/courses/:course_id/gradebook_history/:date/graders\
        /:grader_id\/assignments/:assignment_id/submissions\
        <https://canvas.instructure.com/doc/api/gradebook_history.html#method.\
        gradebook_history_api.submissions>`_

        :param grader_id: The ID of the grader for which you want to see submissions.
        :type grader_id: int
        :param assignment_id: The ID of the assignment for which you want to see submissions
        :type assignment_id: int

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.gradebook_history.Grader`
        """
    
        return PaginatedList(
            Grader,
            self._requester,
            "GET",
            "courses/{}/gradebook_history/{}/graders/{}/assignments/{}/submissions".format(
                self.course_id, self.date, grader_id, assignment_id 
            ),
            kwargs=combine_kwargs(**kwargs),
        )

@python_2_unicode_compatible
class SubmissionHistory(CanvasObject):
    pass