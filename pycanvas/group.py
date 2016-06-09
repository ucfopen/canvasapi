from canvas_object import CanvasObject
from paginated_list import PaginatedList
from util import combine_kwargs
from exceptions import RequiredFieldMissing


class Group(CanvasObject):

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.description)

    def show_front_page(self):
        """
        Retrieve the content of the front page.

        :calls: `GET /api/v1/groups/:group_id/front_page \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_front_page>`_

        :rtype: :class:`pycanvas.group.Group`
        """
        from course import Page

        response = self._requester.request(
            'GET',
            'groups/%s/front_page' % (self.id)
        )
        return Page(self._requester, response.json())

    def create_front_page(self, **kwargs):
        """
        Update the title or contents of the front page.

        :calls: `PUT /api/v1/groups/:group_id/front_page \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update_front_page>`_

        :rtype: :class:`pycanvas.group.Group`
        """
        from course import Page

        response = self._requester.request(
            'PUT',
            'groups/%s/front_page' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return Page(self._requester, response.json())
