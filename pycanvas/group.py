from pycanvas.canvas_object import CanvasObject
from pycanvas.paginated_list import PaginatedList
from pycanvas.util import combine_kwargs
from pycanvas.exceptions import RequiredFieldMissing


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
        from pycanvas.course import Page

        response = self._requester.request(
            'GET',
            'groups/%s/front_page' % (self.id)
        )
        page_json = response.json()
        page_json.update({'group_id': self.id})

        return Page(self._requester, page_json)

    def edit_front_page(self, **kwargs):
        """
        Update the title or contents of the front page.

        :calls: `PUT /api/v1/groups/:group_id/front_page \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update_front_page>`_

        :rtype: :class:`pycanvas.group.Group`
        """
        from pycanvas.course import Page

        response = self._requester.request(
            'PUT',
            'groups/%s/front_page' % (self.id),
            **combine_kwargs(**kwargs)
        )
        page_json = response.json()
        page_json.update({'group_id': self.id})

        return Page(self._requester, page_json)

    def get_pages(self, **kwargs):
        """
        List the wiki pages associated with a group.

        :calls: `GET /api/v1/groups/:group_id/pages \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.index>`_

        :rtype: :class:`pycanvas.groups.Group`
        """
        from pycanvas.course import Page
        return PaginatedList(
            Page,
            self._requester,
            'GET',
            'groups/%s/pages' % (self.id),
            {'group_id': self.id},
            **combine_kwargs(**kwargs)
        )

    def create_page(self, wiki_page, **kwargs):
        """
        Create a new wiki page.

        :calls: `POST /api/v1/groups/:group_id/pages \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.create>`_

        :param title: The title for the page.
        :type title: dict
        :returns: The created page.
        :rtype: :class: `pycanvas.groups.Group`
        """
        from pycanvas.course import Page

        if isinstance(wiki_page, dict) and 'title' in wiki_page:
            kwargs['wiki_page'] = wiki_page
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")

        response = self._requester.request(
            'POST',
            'groups/%s/pages' % (self.id),
            **combine_kwargs(**kwargs)
        )

        page_json = response.json()
        page_json.update({'group_id': self.id})

        return Page(self._requester, page_json)

    def get_page(self, url):
        """
        Retrieve the contents of a wiki page.
        :calls: `GET /api/v1/groups/:group_id/pages/:url \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show>`_

        :param url: The url for the page.
        :type url: string
        :returns: The specified page.
        :rtype: :class: `pycanvas.groups.Group`
        """
        from pycanvas.course import Page

        response = self._requester.request(
            'GET',
            'groups/%s/pages/%s' % (self.id, url)
        )
        page_json = response.json()
        page_json.update({'group_id': self.id})

        return Page(self._requester, page_json)
