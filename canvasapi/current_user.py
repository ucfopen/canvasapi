from __future__ import absolute_import, division, print_function, unicode_literals

import warnings

from six import python_2_unicode_compatible

from canvasapi.bookmark import Bookmark
from canvasapi.course import Course
from canvasapi.favorite import Favorite
from canvasapi.group import Group
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

    def get_favorite_courses(self, **kwargs):
        """
        Retrieve the paginated list of favorite courses for the current user.
        If the user has not chosen any favorites,
        then a selection of currently enrolled courses will be returned.

        :calls: 'GET /api/v1/users/self/favorites/courses \
        <https://canvas.instructure.com/doc/api/favorites.html#method.favorites.list_favorite_courses>'_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList`
        of :class:`canvasapi.course.Course`
        """

        return PaginatedList(
            Course,
            self._requester,
            'GET',
            'users/self/favorites/courses',
            _kwargs=combine_kwargs(**kwargs)
        )

    def get_favorite_groups(self, **kwargs):
        """
        Retrieve the paginated list of favorite groups for the current user.
        If the user has not chosen any favorites, then a selection of groups
        that the user is a member of will be returned.

        :calls: 'GET /api/v1/users/self/favorites/courses \
        <https://canvas.instructure.com/doc/api/favorites.html#method.favorites.list_favorite_groups>'_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList`
        of :class:`canvasapi.group.Group`
        """

        return PaginatedList(
            Group,
            self._requester,
            'GET',
            'users/self/favorites/groups',
            _kwargs=combine_kwargs(**kwargs)
        )

    def add_favorite_course(self, course, **kwargs):
        """
        Add a course to the current user's favorites. If the course is already
        in the user's favorites, nothing happens.

        :calls: 'POST /api/v1/users/self/favorites/courses/:id \
        <https://canvas.instructure.com/doc/api/favorites.html#method.favorites.add_favorite_course>'_

        :param ID: The ID or SIS ID of the course.
        :type ID: `int`

        :rtype: :class:`canvasapi.favorite.Favorite`
        """

        course_id = obj_or_id(course, "course", (Course,))

        response = self._requester.request(
            'POST',
            'users/self/favorites/courses/{}'.format(course_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return Favorite(self._requester, response.json())

    def add_favorite_group(self, group, **kwargs):
        """
        Add a group to the current user's favorites. If the group is already
        in the user's favorites, nothing happens.

        :calls: 'POST /api/v1/users/self/favorites/groups/:id \
        <https://canvas.instructure.com/doc/api/
        favorites.html#method.favorites.add_favorite_groups>'_

        :param ID: The ID or SIS ID of the group.
        :type ID: `int`

        :rtype: :class:`canvasapi.favorite.Favorite`
        """

        group_id = obj_or_id(group, "group", (Group,))

        response = self._requester.request(
            'POST',
            'users/self/favorites/groups/{}'.format(group_id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return Favorite(self._requester, response.json())

    def remove_favorite_course(self, course, **kwargs):
        """
        Remove a course from the current user's favorites.

        :calls: 'DELETE /api/v1/users/self/favorites/courses/:id \
        <https://canvas.instructure.com/doc/api/favorites.html#method.favorites.remove_favorite_course>'_

        :param ID: The ID or SIS ID of the course.
        :type ID: 'int'

        :rtype: :class:'canvasapi.favorite.Favorite'
        """

        course_id = obj_or_id(course, "course", (Course,))

        response = self._requester.request(
            ''
        )

        return Favorite(self._requester, response.json())
