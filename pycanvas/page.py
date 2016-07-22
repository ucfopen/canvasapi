from canvas_object import CanvasObject

from util import combine_kwargs


class Page(CanvasObject):

    def __str__(self):
        return "url: %s, title: %s" % (
            self.url,
            self.title
        )

    def edit(self, **kwargs):
        """
        Update the title or the contents of a specified wiki
        page.

        :calls: `PUT /api/v1/courses/:course_id/pages/:url \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update>`_

        :rtype: :class: `pycanvas.course.Course`
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

        :rtype: :class: `pycanvas.course.Course`
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

        :rtype: :class:`pycanvas.group.Group` or :class:`pycanvas.course.Course`
        """
        from group import Group
        from course import Course

        response = self._requester.request(
            'GET',
            '%ss/%s' % (self.parent_type, self.parent_id)
        )

        if self.parent_type == 'group':
            return Group(self._requester, response.json())
        elif self.parent_type == 'course':
            return Course(self._requester, response.json())
