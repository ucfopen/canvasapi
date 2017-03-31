from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs
from canvasapi.paginated_list import PaginatedList


class Page(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.title, self.url)

    def edit(self, **kwargs):
        """
        Update the title or the contents of a specified wiki
        page.

        :calls: `PUT /api/v1/courses/:course_id/pages/:url \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update>`_

        :rtype: :class:`canvasapi.course.Course`
        """
        response = self._requester.request(
            'PUT',
            '%ss/%s/pages/%s' % (self.parent_type, self.parent_id, self.url),
            **combine_kwargs(**kwargs)
        )

        page_json = response.json()
        page_json.update({'course_id': self.id})
        super(Page, self).set_attributes(page_json)

        return self

    def delete(self):
        """
        Delete this page.

        :calls: `DELETE /api/v1/courses/:course_id/pages/:url \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.destroy>`_

        :rtype: :class:`canvasapi.course.Course`
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s/pages/%s' % (self.course_id, self.url)
        )
        return Page(self._requester, response.json())

    @property
    def parent_id(self):
        """
        Return the id of the course or group that spawned this page.

        :rtype: int
        """
        if hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'group_id'):
            return self.group_id
        else:
            raise ValueError("Page does not have a course_id or group_id")

    @property
    def parent_type(self):
        """
        Return whether the page was spawned from a course or group.

        :rtype: str
        """
        if hasattr(self, 'course_id'):
            return 'course'
        elif hasattr(self, 'group_id'):
            return 'group'
        else:
            raise ValueError("ExternalTool does not have a course_id or group_id")

    def get_parent(self):
        """
        Return the object that spawned this page.

        :rtype: :class:`canvasapi.group.Group` or :class:`canvasapi.course.Course`
        """
        from canvasapi.group import Group
        from canvasapi.course import Course

        response = self._requester.request(
            'GET',
            '%ss/%s' % (self.parent_type, self.parent_id)
        )

        if self.parent_type == 'group':
            return Group(self._requester, response.json())
        elif self.parent_type == 'course':
            return Course(self._requester, response.json())

    def show_latest_revision(self, **kwargs):
        """
        Retrieve the contents of the latest revision.

        :calls: `GET /api/v1/courses/:course_id/pages/:url/revisions/latest \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_revision>`_

        :rtype: :class:`canvasapi.pagerevision.PageRevision`
        """
        response = self._requester.request(
            'GET',
            '%ss/%s/pages/%s/revisions/latest' % (self.parent_type, self.parent_id, self.url),
            **combine_kwargs(**kwargs)
        )
        return PageRevision(self._requester, response.json())

    def get_revision_by_id(self, revision_id, **kwargs):
        """
        Retrieve the contents of the revision by the id.

        :calls: `GET /api/v1/courses/:course_id/pages/:url/revisions/:revision_id \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_revision>`_

        :param revision_id: The id of a specified revision.
        :type revision_id: int
        :returns: Contents of the page revision.
        :rtype: :class:`canvasapi.pagerevision.PageRevision`
        """
        response = self._requester.request(
            'GET',
            '%ss/%s/pages/%s/revisions/%s' % (
                self.parent_type,
                self.parent_id,
                self.url,
                revision_id
            ),
            **combine_kwargs(**kwargs)
        )
        pagerev_json = response.json()
        if self.parent_type == "group":
            pagerev_json.update({'group_id': self.id})
        elif self.parent_type == "course":
            pagerev_json.update({'course_id': self.id})

        return PageRevision(self._requester, pagerev_json)

    def list_revisions(self, **kwargs):
        """
        List the revisions of a page.

        :calls: `GET /api/v1/courses/:course_id/pages/:url/revisions \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.revisions>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.pagerevision.PageRevision`
        """
        return PaginatedList(
            PageRevision,
            self._requester,
            'GET',
            '%ss/%s/pages/%s/revisions' % (self.parent_type, self.parent_id, self.url),
            **combine_kwargs(**kwargs)
        )

    def revert_to_revision(self, revision_id):
        """
        Revert the page back to a specified revision.

        :calls: `POST /api/v1/courses/:course_id/pages/:url/revisions/:revision_id \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.revert>`_

        :param revision_id: The id of a specified revision.
        :type revision_id: int
        :returns: Contents of the page revision.
        :rtype: :class:`canvasapi.pagerevision.PageRevision`
        """
        response = self._requester.request(
            'POST',
            '%ss/%s/pages/%s/revisions/%s' % (
                self.parent_type,
                self.parent_id,
                self.url,
                revision_id
            ),
        )
        pagerev_json = response.json()
        if self.parent_type == "group":
            pagerev_json.update({'group_id': self.id})
        elif self.parent_type == "course":
            pagerev_json.update({'group_id': self.id})

        return PageRevision(self._requester, pagerev_json)


class PageRevision(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.updated_at, self.revision_id)

    @property
    def parent_id(self):
        """
        Return the id of the course or group that spawned this page.

        :rtype: int
        """
        if hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'group_id'):
            return self.group_id
        else:
            raise ValueError("Page does not have a course_id or group_id")

    @property
    def parent_type(self):
        """
        Return whether the page was spawned from a course or group.

        :rtype: str
        """
        if hasattr(self, 'course_id'):
            return 'course'
        elif hasattr(self, 'group_id'):
            return 'group'
        else:
            raise ValueError("ExternalTool does not have a course_id or group_id")

    def get_parent(self):
        """
        Return the object that spawned this page.

        :rtype: :class:`canvasapi.group.Group` or :class:`canvasapi.course.Course`
        """
        from canvasapi.group import Group
        from canvasapi.course import Course

        response = self._requester.request(
            'GET',
            '%ss/%s' % (self.parent_type, self.parent_id)
        )

        if self.parent_type == 'group':
            return Group(self._requester, response.json())
        elif self.parent_type == 'course':
            return Course(self._requester, response.json())
