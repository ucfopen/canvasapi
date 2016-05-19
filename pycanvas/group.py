from canvas_object import CanvasObject
from util import combine_kwargs
from paginated_list import PaginatedList
from exceptions import RequiredFieldMissing


class Group(CanvasObject):

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.description)

    def show_front_page(self):
        """
        Retrieve the content of the front page.

        :calls: `GET /api/v1/groups/:group_id/front_page \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_front_page>`_

        :rtype: :class:`pycanvas.course.Course`
        """
        from course import Page

        response = self._requester.request(
            'GET',
            'courses/%s/front_page' % (self.id)
        )
        return Page(self._requester, response.json())
