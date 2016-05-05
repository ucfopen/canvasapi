from canvas_object import CanvasObject
from util import combine_kwargs
from paginated_list import PaginatedList


class Section(CanvasObject):

    def __str__(self):
        return ""

    def get_info(self):
        """
        Get details about a specific sections
        :calls: `GET /api/v1/sections/:id`
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.index>
        :rtype: Section
        """
        response = self._requester.request(
            'GET',
            'sections/%s' % (self.id)
        )
        return Section(self._requester, response.json())

    def list_enrollments(self):
        """
        Lists all of the enrollments for a user.

        :calls: `GET /api/v1/sections/:section_id/enrollments`
        <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index>
        :rtype: :class:`PaginatedList` of :class:`Enrollment`
        """
        from enrollment import Enrollment

        return PaginatedList(
            Enrollment,
            self._requester,
            'GET',
            'sections/%s/enrollments' % (self.id)
        )
