from canvas_object import CanvasObject
from paginated_list import PaginatedList
from util import combine_kwargs


class User(CanvasObject):

    def __str__(self):
        return "%s" % (self.name)

    def get_profile(self, **kwargs):
        """
        Get a user's profile.

        :calls: `GET /api/v1/user/:id <https://canvas.instructure.com/doc/api/users.html#method.profile.settings>`
        :rtype: dict
        """
        response = self._requester.request(
            'GET',
            'users/%s/profile' % (self.id)
        )
        return response.json()

    def get_page_views(self):
        """
        Get a user's pageviews.

        :calls: `GET /api/v1/users/:user_id/page_views <https://canvas.instructure.com/doc/api/users.html#method.page_views.index>`
        :rtype :class:`pycanvas.user.User`
        """
        from page_view import PageView

        return PaginatedList(
            PageView,
            self._requester,
            'GET',
            'users/%s/page_views' % (self.id)
        )

    def get_courses(self):
        """
        Get a user's courses.

        :calls: `GET /api/v1/users/:user_id/courses
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.user_index>`
        :rtype: list
        """
        from course import Course

        return PaginatedList(
            Course,
            self._requester,
            'GET',
            'users/%s/courses' % (self.id)
        )

    def get_missing_submissions(self):
        """
        Returns past-due assignments for which the student does not
        have a submission.

        :calls: `GET /api/v1/users/:user_id/missing_submissions
        <https://canvas.instructure.com/doc/api/users.html#method.users.missing_submissions>`
        :rtype: :class:`PaginatedList` of :class:`Assignment`
        """
        from assignment import Assignment

        return PaginatedList(
            Assignment,
            self._requester,
            'GET',
            'users/%s/missing_submissions' % (self.id)
        )

    def update_settings(self, **kwargs):
        """
        Update an existing user's settings.

        :calls: `PUT /api/v1/users/:id/settings
        <https://canvas.instructure.com/doc/api/users.html#method.users.settings>`
        :rtype: dict
        """
        response = self._requester.request(
            'PUT',
            'users/%s/settings' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return response.json()

    def get_color(self, asset_string):
        """
        Returns the custom colors that have been saved for a user for a given context.

        The `asset_string` parameter should be in the format 'context_id', for example 'course_42'.

        :calls: `GET /api/v1/users/:id/colors/:asset_string
        <https://canvas.instructure.com/doc/api/users.html#method.users.get_custom_color>`
        :param asset_string: string
        :rtype: dict
        """
        response = self._requester.request(
            'GET',
            'users/%s/colors/%s' % (self.id, asset_string)
        )
        return response.json()

    def get_colors(self):
        """
        Returns all custom colors that have been saved for a user.

        :calls: `GET /api/v1/users/:id/colors
        <https://canvas.instructure.com/doc/api/users.html#method.users.get_custom_colors>`
        :rtype: dict
        """
        response = self._requester.request(
            'GET',
            'users/%s/colors' % (self.id)
        )
        return response.json()

    def update_color(self, asset_string, hexcode):
        """
        Updates a custom color for a user for a given context. This allows colors for the calendar and elsewhere to be customized on a user basis.

        The `asset_string` parameter should be in the format 'context_id', for example 'course_42'.
        The `hexcode` parameter need not include the '#'.

        :calls: `PUT /api/v1/users/:id/colors/:asset_string
        <https://canvas.instructure.com/doc/api/users.html#method.users.set_custom_color>`
        :param asset_string: string
        :param hexcode: string
        :rtype: dict
        """
        response = self._requester.request(
            'PUT',
            'users/%s/colors/%s' % (self.id, asset_string),
            hexcode=hexcode
        )
        return response.json()

    def edit(self, **kwargs):
        """
        Modify an existing user.


        :calls: `PUT /api/v1/users/:id
        <https://canvas.instructure.com/doc/api/users.html#method.users.update>`
        :rtype: :class:`User`
        """
        response = self._requester.request(
            'PUT',
            'users/%s' % (self.id),
            **combine_kwargs(**kwargs)
        )
        super(User, self).set_attributes(response.json())
        return self

    def merge_into(self, destination_user):
        """
        Merge a user into another user.

        :calls: `PUT /api/v1/users/:id/merge_into/:destination_user_id
        <https://canvas.instructure.com/doc/api/users.html#method.users.merge_into>`
        :param destination_user: :class:`User`
        :rtype: :class:`User`
        """
        assert isinstance(destination_user, User)
        response = self._requester.request(
            'PUT',
            'users/%s/merge_into/%s' % (self.id, destination_user.id),
        )
        super(User, self).set_attributes(response.json())
        return self

    def get_avatars(self):
        """
        Retrieve the possible user avatar options that can be set with the user update endpoint.

        :calls: `GET /api/v1/users/:user_id/avatars
        <https://canvas.instructure.com/doc/api/users.html#method.profile.profile_pics>`
        :rtype: :class:`PaginatedList` of :class:`Avatar`
        """
        from avatar import Avatar

        return PaginatedList(
            Avatar,
            self._requester,
            'GET',
            '/users/%s/avatars' % (self.id)
        )

    def get_assignments(self, course_id):
        """
        Returns the list of assignments for the specified user if the current
        user has rights to view. See List assignments for valid arguments.

        :calls: `GET /api/v1/users/:user_id/courses/:course_id/assignments`
        :rtype: :class:`PaginatedList` of :class:`Assignment`
        """
        from assignment import Assignment

        return PaginatedList(
            Assignment,
            self._requester,
            'GET',
            'users/%s/courses/%s/assignments' % (self.id, course_id)
        )
