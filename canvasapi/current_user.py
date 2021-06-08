from canvasapi.bookmark import Bookmark
from canvasapi.course import Course
from canvasapi.favorite import Favorite
from canvasapi.group import Group
from canvasapi.paginated_list import PaginatedList
from canvasapi.user import User
from canvasapi.util import combine_kwargs, obj_or_id


class CurrentUser(User):
    def __init__(self, _requester):
        self._requester = _requester

        response = self._requester.request("GET", "users/self")

        super(CurrentUser, self).__init__(self._requester, response.json())

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def add_favorite_course(self, course, use_sis_id=False, **kwargs):
        """
        Add a course to the current user's favorites. If the course is already
        in the user's favorites, nothing happens.

        :calls: `POST /api/v1/users/self/favorites/courses/:id \
        <https://canvas.instructure.com/doc/api/favorites.html#method.favorites.add_favorite_course>`_

        :param course: The course or ID/SIS ID of the course.
        :type course: :class:`canvasapi.course.Course` or int

        :param use_sis_id: Whether or not `course` is an sis ID.
            Defaults to `False`.
        :type use_sis_id: bool

        :rtype: :class:`canvasapi.favorite.Favorite`
        """
        if use_sis_id:
            course_id = course
            uri_str = "users/self/favorites/courses/sis_course_id:{}"
        else:
            course_id = obj_or_id(course, "course", (Course,))
            uri_str = "users/self/favorites/courses/{}"

        response = self._requester.request(
            "POST", uri_str.format(course_id), _kwargs=combine_kwargs(**kwargs)
        )
        return Favorite(self._requester, response.json())

    def add_favorite_group(self, group, use_sis_id=False, **kwargs):
        """
        Add a group to the current user's favorites. If the group is already
        in the user's favorites, nothing happens.

        :calls: `POST /api/v1/users/self/favorites/groups/:id \
        <https://canvas.instructure.com/doc/api/favorites.html#method.favorites.add_favorite_groups>`_

        :param group: The ID or SIS ID of the group.
        :type group: :class:`canvasapi.group.Group` or int

        :param use_sis_id: Whether or not `group` is an sis ID.
            Defaults to `False`.
        :type use_sis_id: bool

        :rtype: :class:`canvasapi.favorite.Favorite`
        """
        if use_sis_id:
            group_id = group
            uri_str = "users/self/favorites/groups/sis_group_id:{}"
        else:
            group_id = obj_or_id(group, "group", (Group,))
            uri_str = "users/self/favorites/groups/{}"

        response = self._requester.request(
            "POST", uri_str.format(group_id), _kwargs=combine_kwargs(**kwargs)
        )
        return Favorite(self._requester, response.json())

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
            "POST",
            "users/self/bookmarks",
            name=name,
            url=url,
            _kwargs=combine_kwargs(**kwargs),
        )

        return Bookmark(self._requester, response.json())

    def get_bookmark(self, bookmark, **kwargs):
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
            "GET",
            "users/self/bookmarks/{}".format(bookmark_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return Bookmark(self._requester, response.json())

    def get_bookmarks(self, **kwargs):
        """
        List bookmarks that the current user can view or manage.

        :calls: `GET /api/v1/users/self/bookmarks \
        <https://canvas.instructure.com/doc/api/bookmarks.html#method.bookmarks/bookmarks.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.bookmark.Bookmark`
        """
        return PaginatedList(Bookmark, self._requester, "GET", "users/self/bookmarks")

    def get_favorite_courses(self, **kwargs):
        """
        Retrieve the paginated list of favorite courses for the current user.
        If the user has not chosen any favorites,
        then a selection of currently enrolled courses will be returned.

        :calls: `GET /api/v1/users/self/favorites/courses \
        <https://canvas.instructure.com/doc/api/favorites.html#method.favorites.list_favorite_courses>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.course.Course`
        """

        return PaginatedList(
            Course,
            self._requester,
            "GET",
            "users/self/favorites/courses",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_favorite_groups(self, **kwargs):
        """
        Retrieve the paginated list of favorite groups for the current user.
        If the user has not chosen any favorites, then a selection of groups
        that the user is a member of will be returned.

        :calls: `GET /api/v1/users/self/favorites/groups \
        <https://canvas.instructure.com/doc/api/favorites.html#method.favorites.list_favorite_groups>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.group.Group`
        """

        return PaginatedList(
            Group,
            self._requester,
            "GET",
            "users/self/favorites/groups",
            _kwargs=combine_kwargs(**kwargs),
        )

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
            "GET",
            "users/self/groups",
            _kwargs=combine_kwargs(**kwargs),
        )

    def reset_favorite_courses(self, **kwargs):
        """
        Reset the current user's course favorites to the default
        automatically generated list of enrolled courses

        :calls: `DELETE /api/v1/users/self/favorites/courses \
        <https://canvas.instructure.com/doc/api/favorites.html#method.favorites.reset_course_favorites>`_

        :returns: `True` if reset correctly, `False` otherwise.
        :rtype: bool
        """

        response = self._requester.request(
            "DELETE", "users/self/favorites/courses", _kwargs=combine_kwargs(**kwargs)
        )
        return response.json().get("message") == "OK"

    def reset_favorite_groups(self, **kwargs):
        """
        Reset the current user's group favorites to the default
        automatically generated list of enrolled groups

        :calls: `DELETE /api/v1/users/self/favorites/groups \
        <https://canvas.instructure.com/doc/api/favorites.html#method.favorites.reset_groups_favorites>`_

        :returns: `True` if reset correctly, `False` otherwise.
        :rtype: bool
        """

        response = self._requester.request(
            "DELETE", "users/self/favorites/groups", _kwargs=combine_kwargs(**kwargs)
        )
        return response.json().get("message") == "OK"
