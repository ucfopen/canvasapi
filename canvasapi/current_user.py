from __future__ import absolute_import, division, print_function, unicode_literals

import warnings

from six import python_2_unicode_compatible

from canvasapi.bookmark import Bookmark
from canvasapi.paginated_list import PaginatedList
from canvasapi.user import User
from canvasapi.util import combine_kwargs, obj_or_id


@python_2_unicode_compatible
class CurrentUser(User):
    def __init__(self, _requester):
        self._requester = _requester

        response = self._requester.request(
            'GET',
            'users/self'
        )

        super(CurrentUser, self).__init__(self._requester, response.json())

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def list_groups(self, **kwargs):
        """
        Return the list of active groups for the user.

        .. warning::
            .. deprecated:: 0.10.0
                Use :func:`canvasapi.current_user.CurrentUser.get_groups` instead.

        :calls: `GET /api/v1/users/self/groups \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of :class:`canvasapi.group.Group`
        """
        warnings.warn(
            "`list_groups` is being deprecated and will be removed in a "
            "future version. Use `get_groups` instead",
            DeprecationWarning
        )

        return self.get_groups(**kwargs)

    def get_groups(self, **kwargs):
        """
        Return the list of active groups for the user.

        :calls: `GET /api/v1/users/self/groups \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of :class:`canvasapi.group.Group`
        """
        from canvasapi.group import Group

        return PaginatedList(
            Group,
            self._requester,
            'GET',
            'users/self/groups',
            _kwargs=combine_kwargs(**kwargs)
        )

    def list_bookmarks(self, **kwargs):
        """
        List bookmarks that the current user can view or manage.

        .. warning::
            .. deprecated:: 0.10.0
                Use :func:`canvasapi.current_user.CurrentUser.get_bookmarks` instead.

        :calls: `GET /api/v1/users/self/bookmarks \
        <https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.bookmark.Bookmark`
        """
        warnings.warn(
            "`list_bookmarks` is being deprecated and will be removed in a "
            "future version. Use `get_bookmarks` instead",
            DeprecationWarning
        )

        return self.get_bookmarks(**kwargs)

    def get_bookmarks(self, **kwargs):
        """
        List bookmarks that the current user can view or manage.

        :calls: `GET /api/v1/users/self/bookmarks \
        <https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.bookmark.Bookmark`
        """
        return PaginatedList(
            Bookmark,
            self._requester,
            'GET',
            'users/self/bookmarks'
        )

    def create_bookmark(self, name, url, **kwargs):
        """
        Create a new Bookmark.

        :calls: `POST /api/v1/users/self/bookmarks \
        <https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.create>`_

        :param name: The name of the bookmark.
        :type name: `str`
        :param url: The url of the bookmark.
        :type url: `str`
        :rtype: :class:`canvasapi.bookmark.Bookmark`
        """
        from canvasapi.bookmark import Bookmark

        response = self._requester.request(
            'POST',
            'users/self/bookmarks',
            name=name,
            url=url,
            _kwargs=combine_kwargs(**kwargs)
        )

        return Bookmark(self._requester, response.json())

    def get_bookmark(self, bookmark):
        """
        Return single Bookmark by id

        :calls: `GET /api/v1/users/self/bookmarks/:id \
        <https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.show>`_

        :param bookmark: The object or ID of the bookmark.
        :type bookmark: :class:`canvasapi.bookmark.Bookmark` or int

        :rtype: :class:`canvasapi.bookmark.Bookmark`
        """
        from canvasapi.bookmark import Bookmark

        bookmark_id = obj_or_id(bookmark, "bookmark", (Bookmark,))

        response = self._requester.request(
            'GET',
            'users/self/bookmarks/{}'.format(bookmark_id)
        )
        return Bookmark(self._requester, response.json())
