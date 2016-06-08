from canvas_object import CanvasObject
from paginated_list import PaginatedList
from util import combine_kwargs


class Section(CanvasObject):

    def __str__(self):
        return 'Section #%s \"%s\" |course_id: %s' % (
            self.id,
            self.name,
            self.course_id
        )

    def list_enrollments(self, **kwargs):
        """
        List all of the enrollments for the current user.

        :calls: `GET /api/v1/sections/:section_id/enrollments \
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.enrollment.Enrollment`
        """
        from enrollment import Enrollment

        return PaginatedList(
            Enrollment,
            self._requester,
            'GET',
            'sections/%s/enrollments' % (self.id),
            **combine_kwargs(**kwargs)
        )
