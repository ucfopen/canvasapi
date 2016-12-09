from pycanvas.canvas_object import CanvasObject
from pycanvas.exceptions import RequiredFieldMissing
from pycanvas.paginated_list import PaginatedList
from pycanvas.util import combine_kwargs


class Group(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def create_page(self, wiki_page, **kwargs):
        """
        Create a new wiki page.

        :calls: `POST /api/v1/groups/:group_id/pages \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.create>`_

        :param title: The title for the page.
        :type title: dict
        :returns: The created page.
        :rtype: :class: `pycanvas.page.Page`
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

    def edit_front_page(self, **kwargs):
        """
        Update the title or contents of the front page.

        :calls: `PUT /api/v1/groups/:group_id/front_page \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update_front_page>`_

        :rtype: :class:`pycanvas.page.Page`
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

    def get_pages(self, **kwargs):
        """
        List the wiki pages associated with a group.

        :calls: `GET /api/v1/groups/:group_id/pages \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.index>`_

        :rtype: :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.page.Page`
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

    def edit(self, **kwargs):
        """
        Edit a group.

        :calls: `PUT /api/v1/groups/:group_id \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.update>`_

        :rtype: :class:`pycanvas.group.Group`
        """
        response = self._requester.request(
            'PUT',
            'groups/%s' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return Group(self._requester, response.json())

    def delete(self):
        """
        Delete a group.

        :calls: `DELETE /api/v1/groups/:group_id \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.destroy>`_

        :rtype: :class:`pycanvas.group.Group`
        """
        response = self._requester.request(
            'DELETE',
            'groups/%s' % (self.id)
        )
        return Group(self._requester, response.json())

    def invite(self, invitees):
        """
        Invite users to group.

        :calls: `POST /api/v1/groups/:group_id/invite \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.invite>`_

        :param invitees: list of user ids
        :type invitees: integer list

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.group.GroupMembership`
        """
        return PaginatedList(
            GroupMembership,
            self._requester,
            'POST',
            'groups/%s/invite' % (self.id),
            invitees=invitees
        )

    def list_users(self, **kwargs):
        """
        List users in a group.

        :calls: `POST /api/v1/groups/:group_id/users \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.users>`_

        :param invitees: list of user ids
        :type invitees: integer list

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.user.User`
        """
        from pycanvas.user import User
        return PaginatedList(
            User,
            self._requester,
            'GET',
            'groups/%s/users' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def remove_user(self, user):
        """
        Leave a group if allowed.

        :calls: `DELETE /api/v1/groups/:group_id/:type/:id \
        <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.destroy>`_

        :param user: The user object or ID to remove from the group.
        :type user: :class:`pycanvas.user.User` or int

        :rtype: :class:`pycanvas.user.User`
        """
        from pycanvas.user import User
        from pycanvas.util import obj_or_id

        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            'DELETE',
            'groups/%s/users/%s' % (self.id, user_id),
        )
        return User(self._requester, response.json())

    def upload(self, file, **kwargs):
        """
        Upload a file to the group.
        Only those with the 'Manage Files' permission on a group can upload files to the group.
        By default, this is anybody participating in the group, or any admin over the group.

        :calls: `POST /api/v1/groups/:group_id/files \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.create_file>`_

        :param path: The path of the file to upload.
        :type path: str
        :param file: The file or path of the file to upload.
        :type file: file or str
        :returns: True if the file uploaded successfully, False otherwise, \
                    and the JSON response from the API.
        :rtype: tuple
        """
        from pycanvas.upload import Uploader

        return Uploader(
            self._requester,
            'groups/%s/files' % (self.id),
            file,
            **kwargs
        ).start()

    def preview_html(self, html):
        """
        Preview HTML content processed for this course.

        :calls: `POST /api/v1/groups/:group_id/preview_html \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.preview_html>`_

        :param html: The HTML code to preview.
        :type html: str
        :rtype: str
        """
        response = self._requester.request(
            'POST',
            'groups/%s/preview_html' % (self.id),
            html=html
        )
        return response.json().get('html', '')

    # def get_activity_stream(self):
    #     """
    #     Returns the current user's group-specific activity stream, paginated.

    #     :calls: `GET /api/v1/groups/:group_id/activity_stream \
    #     <https://canvas.instructure.com/doc/api/groups.html#method.groups.activity_stream>`_

    #     :rtype: list of various objects.
    #     """
    #     response = self._requester.request(
    #         'GET',
    #         'groups/self/activity_stream/'
    #     )
    #     return response.json()

    def get_activity_stream_summary(self):
        """
        Return a summary of the current user's global activity stream.

        :calls: `GET /api/v1/groups/:group_id/activity_stream/summary \
        <https://canvas.instructure.com/doc/api/users.html#method.groups.activity_stream_summary>`_

        :rtype: dict
        """
        response = self._requester.request(
            'GET',
            'groups/%s/activity_stream/summary' % (self.id)
        )
        return response.json()

    def list_memberships(self, **kwargs):
        """
        List users in a group.

        :calls: `GET /api/v1/groups/:group_id/memberships \
        <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.index>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.group.GroupMembership`
        """
        return PaginatedList(
            GroupMembership,
            self._requester,
            'GET',
            'groups/%s/memberships' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def get_membership(self, user_id, membership_type):
        """
        List users in a group.

        if membership_type = 'users'
        :calls: `GET /api/v1/groups/:group_id/users/:user_id \
        <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.show>`_

        if membership_type = 'memberships'
        :calls: `GET /api/v1/groups/:group_id/memberships/:membership_id \
        <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.show>`_

        :param invitees: list of user ids
        :type invitees: integer list

        :rtype: :class:`pycanvas.group.GroupMembership`
        """
        response = self._requester.request(
            'GET',
            'groups/%s/%s/%s' % (self.id, membership_type, user_id)
        )
        return GroupMembership(self._requester, response.json())

    def create_membership(self, user_id, **kwargs):
        """
        Join, or request to join, a group, depending on the join_level of the group.
        If the membership or join request already exists, then it is simply returned

        :calls: `POST /api/v1/groups/:group_id/memberships \
        <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.create>`_

        :rtype: :class:`pycanvas.group.GroupMembership`
        """
        response = self._requester.request(
            'POST',
            'groups/%s/memberships' % (self.id),
            user_id=user_id,
            **combine_kwargs(**kwargs)
        )
        return GroupMembership(self._requester, response.json())

    def update_membership(self, user_id, **kwargs):
        """
        Accept a membership request, or add/remove moderator rights.

        :calls: `PUT /api/v1/groups/:group_id/users/:user_id \
        <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.update>`_

        :rtype: :class:`pycanvas.group.GroupMembership`
        """
        response = self._requester.request(
            'PUT',
            'groups/%s/users/%s' % (self.id, user_id),
            **combine_kwargs(**kwargs)
        )
        return GroupMembership(self._requester, response.json())


class GroupMembership(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.user_id, self.group_id)

    def update(self, mem_id, **kwargs):
        """
        Accept a membership request, or add/remove moderator rights.

        :calls: `PUT /api/v1/groups/:group_id/memberships/:membership_id \
        <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.update>`_

        :rtype: :class:`pycanvas.group.GroupMembership`
        """
        response = self._requester.request(
            'PUT',
            'groups/%s/memberships/%s' % (self.id, mem_id),
            **combine_kwargs(**kwargs)
        )
        return GroupMembership(self._requester, response.json())

    def remove_user(self, user):
        """
        Remove user from membership.

        :calls: `DELETE /api/v1/groups/:group_id/:type/:id \
        <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.destroy>`_

        :param user: The user object or ID to remove from the group.
        :type user: :class:`pycanvas.user.User` or int

        :rtype: empty dict
        """
        from pycanvas.user import User
        from pycanvas.util import obj_or_id

        user_id = obj_or_id(user, "user", (User,))

        response = self._requester.request(
            'DELETE',
            'groups/%s/users/%s' % (self.id, user_id),
        )
        return response.json()

    def remove_self(self):
        """
        Leave a group if allowed.

        :calls: `DELETE /api/v1/groups/:group_id/:type/:id \
        <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.destroy>`_

        :rtype: empty dict
        """
        response = self._requester.request(
            'DELETE',
            'groups/%s/memberships/self' % (self.id),
        )
        return response.json()


class GroupCategory(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def create_group(self, **kwargs):
        """
        Create a group

        :calls: `POST /api/v1/group_categories/:group_category_id/groups \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.create>`_

        :rtype: :class:`pycanvas.group.Group`
        """
        response = self._requester.request(
            'POST',
            'group_categories/%s/groups' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return Group(self._requester, response.json())

    def get_category(self, cat_id):
        """
        Get a single group category

        :calls: `GET /api/v1/group_categories/:group_category_id \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.show>`_

        :rtype: :class:`pycanvas.group.GroupCategory`
        """
        response = self._requester.request(
            'GET',
            'group_categories/%s' % (cat_id)
        )
        return GroupCategory(self._requester, response.json())

    def update(self, **kwargs):
        """
        Update a Group Category

        :calls: `PUT /api/v1/group_categories/:group_category_id \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.update>`_

        :rtype: :class:`pycanvas.group.GroupCategory`
        """
        response = self._requester.request(
            'PUT',
            'group_categories/%s' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return GroupCategory(self._requester, response.json())

    def delete(self):
        """
        Delete a Group Category

        :calls: `DELETE /api/v1/group_categories/:group_category_id \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.destroy>`_

        :rtype: empty dict
        """
        response = self._requester.request(
            'DELETE',
            'group_categories/%s' % (self.id)
        )
        return response.json()

    def list_groups(self):
        """
        List groups in group category

        :calls: `GET /api/v1/group_categories/:group_category_id/groups \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.groups>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.group.Group`
        """
        return PaginatedList(
            Group,
            self._requester,
            'GET',
            'group_categories/%s/groups' % (self.id)
        )

    def list_users(self, **kwargs):
        """
        List users in group category

        :calls: `GET /api/v1/group_categories/:group_category_id/users \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.users>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.user.User`
        """
        from pycanvas.user import User
        return PaginatedList(
            User,
            self._requester,
            'GET',
            'group_categories/%s/users' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def assign_members(self, sync=False):
        """
        Assign unassigned members

        :calls: `POST /api/v1/group_categories/:group_category_id/assign_unassigned_members \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.assign_unassigned_members>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.user.User`
            or :class:`pycanvas.progress.Progress`
        """
        from pycanvas.user import User
        from pycanvas.progress import Progress
        if sync:
            return PaginatedList(
                User,
                self._requester,
                'POST',
                'group_categories/%s/assign_unassigned_members' % (self.id)
            )
        else:
            response = self._requester.request(
                'POST',
                'group_categories/%s/assign_unassigned_members' % (self.id)
            )
            return Progress(self._requester, response.json())
