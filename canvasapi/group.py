from canvasapi.canvas_object import CanvasObject
from canvasapi.discussion_topic import DiscussionTopic
from canvasapi.folder import Folder
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.paginated_list import PaginatedList
from canvasapi.tab import Tab
from canvasapi.util import combine_kwargs


class Group(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def create_page(self, wiki_page, **kwargs):
        """
        Create a new wiki page.

        :calls: `POST /api/v1/groups/:group_id/pages \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.create>`_

        :param wiki_page: Details about the page to create.
        :type wiki_page: dict
        :returns: The created page.
        :rtype: :class:`canvasapi.page.Page`
        """
        from canvasapi.course import Page

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

        :rtype: :class:`canvasapi.page.Page`
        """
        from canvasapi.course import Page

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

        :rtype: :class:`canvasapi.group.Group`
        """
        from canvasapi.course import Page

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
        :type url: str
        :returns: The specified page.
        :rtype: :class:`canvasapi.groups.Group`
        """
        from canvasapi.course import Page

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

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.page.Page`
        """
        from canvasapi.course import Page
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

        :rtype: :class:`canvasapi.group.Group`
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

        :rtype: :class:`canvasapi.group.Group`
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

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.group.GroupMembership`
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

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.user.User`
        """
        from canvasapi.user import User
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
        :type user: :class:`canvasapi.user.User` or int

        :rtype: :class:`canvasapi.user.User`
        """
        from canvasapi.user import User
        from canvasapi.util import obj_or_id

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
        from canvasapi.upload import Uploader

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

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.group.GroupMembership`
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

        :calls: `GET /api/v1/groups/:group_id/users/:user_id \
            <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.show>`_

            or `GET /api/v1/groups/:group_id/memberships/:membership_id
            <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.show>`_

        :param invitees: list of user ids
        :type invitees: integer list

        :rtype: :class:`canvasapi.group.GroupMembership`
        """
        response = self._requester.request(
            'GET',
            'groups/%s/%s/%s' % (self.id, membership_type, user_id)
        )
        return GroupMembership(self._requester, response.json())

    def create_membership(self, user_id, **kwargs):
        """
        Join, or request to join, a group, depending on the join_level of the group.
        If the membership or join request already exists, then it is simply returned.

        :calls: `POST /api/v1/groups/:group_id/memberships \
        <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.create>`_

        :rtype: :class:`canvasapi.group.GroupMembership`
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

        :rtype: :class:`canvasapi.group.GroupMembership`
        """
        response = self._requester.request(
            'PUT',
            'groups/%s/users/%s' % (self.id, user_id),
            **combine_kwargs(**kwargs)
        )
        return GroupMembership(self._requester, response.json())

    def get_discussion_topic(self, topic_id):
        """
        Return data on an individual discussion topic.

        :calls: `GET /api/v1/groups/:group_id/discussion_topics/:topic_id \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.show>`_

        :param topic_id: The ID of the discussion topic.
        :type topic_id: int

        :rtype: :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        response = self._requester.request(
            'GET',
            'groups/%s/discussion_topics/%s' % (self.id, topic_id)
        )

        response_json = response.json()
        response_json.update({'group_id': self.id})

        return DiscussionTopic(self._requester, response_json)

    def get_full_discussion_topic(self, topic_id):
        """
        Return a cached structure of the discussion topic.

        :calls: `GET /api/v1/courses/:course_id/discussion_topics/:topic_id/view \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.view>`_

        :param topic_id: The ID of the discussion topic.
        :type topic_id: int

        :rtype: :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        response = self._requester.request(
            'GET',
            'groups/%s/discussion_topics/%s/view' % (self.id, topic_id),
        )

        response_json = response.json()
        response_json.update({'group_id': self.id})

        return DiscussionTopic(self._requester, response_json)

    def get_discussion_topics(self, **kwargs):
        """
        Returns the paginated list of discussion topics for this course or group.

        :calls: `GET /api/v1/groups/:course_id/discussion_topics \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.discussion_topic.DiscussionTopic`
        """

        return PaginatedList(
            DiscussionTopic,
            self._requester,
            'GET',
            'groups/%s/discussion_topics' % (self.id),
            {'group_id': self.id},
            **combine_kwargs(**kwargs)
        )

    def create_discussion_topic(self, **kwargs):
        """
        Creates a new discussion topic for the course or group.

        :calls: `POST /api/v1/courses/:group_id/discussion_topics \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.create>`_

        :rtype: :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        response = self._requester.request(
            'POST',
            'groups/%s/discussion_topics' % (self.id),
            **combine_kwargs(**kwargs)
        )

        response_json = response.json()
        response_json.update({'group_id': self.id})

        return DiscussionTopic(self._requester, response_json)

    def reorder_pinned_topics(self, order):
        """
        Puts the pinned discussion topics in the specified order.
        All pinned topics should be included.

        :calls: `POST /api/v1/groups/:group_id/discussion_topics/reorder \
        <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.reorder>`_

        :param order: The ids of the pinned discussion topics in the desired order.
            e.g. [104, 102, 103]
        :type order: list

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        if not isinstance(order, list):
            raise ValueError("Param order needs to be string or a list.")

        response = self._requester.request(
            'POST',
            'groups/%s/discussion_topics/reorder' % (self.id),
            order=order
        )

        return response.json().get('reorder')

    def list_external_feeds(self):
        """
        Returns the list of External Feeds this group.

        :calls: `GET /api/v1/groups/:group_id/external_feeds \
        <https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.external_feed.ExternalFeed`
        """
        from canvasapi.external_feed import ExternalFeed
        return PaginatedList(
            ExternalFeed,
            self._requester,
            'GET',
            'groups/%s/external_feeds' % (self.id)
        )

    def create_external_feed(self, url, **kwargs):
        """
        Create a new external feed for the group.

        :calls: `POST /api/v1/groups/:group_id/external_feeds \
        <https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.create>`_

        :param url: The urlof the external rss or atom feed
        :type url: str
        :rtype: :class:`canvasapi.external_feed.ExternalFeed`
        """
        from canvasapi.external_feed import ExternalFeed
        response = self._requester.request(
            'POST',
            'groups/%s/external_feeds' % self.id,
            url=url,
            **combine_kwargs(**kwargs)
        )
        return ExternalFeed(self._requester, response.json())

    def delete_external_feed(self, feed_id):
        """
        Deletes the external feed.

        :calls: `DELETE /api/v1/groups/:group_id/external_feeds/:external_feed_id \
        <https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.destroy>`_

        :param feed_id: The id of the feed to be deleted.
        :type feed_id: int
        :rtype: :class:`canvasapi.external_feed.ExternalFeed`
        """
        from canvasapi.external_feed import ExternalFeed
        response = self._requester.request(
            'DELETE',
            'groups/%s/external_feeds/%s' % (self.id, feed_id)
        )
        return ExternalFeed(self._requester, response.json())

    def list_files(self, **kwargs):
        """
        Returns the paginated list of files for the group.

        :calls: `GET api/v1/courses/:group_id/files \
        <https://canvas.instructure.com/doc/api/files.html#method.files.api_index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.file.File`
        """
        from canvasapi.file import File

        return PaginatedList(
            File,
            self._requester,
            'GET',
            'groups/%s/files' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def get_folder(self, folder_id):
        """
        Returns the details for a group's folder

        :calls: `GET /api/v1/groups/:group_id/folders/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.show>`_

        :param folder_id: The ID of the folder to retrieve.
        :type folder_id: int
        :rtype: :class:`canvasapi.folder.Folder`
        """
        response = self._requester.request(
            'GET',
            'groups/%s/folders/%s' % (self.id, folder_id)
        )
        return Folder(self._requester, response.json())

    def list_folders(self):
        """
        Returns the paginated list of all folders for the given group. This will be returned as a
        flat list containing all subfolders as well.

        :calls: `GET /api/v1/groups/:group_id/folders \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.list_all_folders>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.folder.Folder`
        """
        return PaginatedList(
            Folder,
            self._requester,
            'GET',
            'groups/%s/folders' % (self.id)
        )

    def create_folder(self, name, **kwargs):
        """
        Creates a folder in this group.

        :calls: `POST /api/v1/groups/:group_id/folders \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.create>`_

        :param name: The name of the folder.
        :type name: str
        :rtype: :class:`canvasapi.folder.Folder`
        """
        response = self._requester.request(
            'POST',
            'groups/%s/folders' % self.id,
            name=name,
            **combine_kwargs(**kwargs)
        )
        return Folder(self._requester, response.json())

    def list_tabs(self, **kwargs):
        """
        List available tabs for a group.
        Returns a list of navigation tabs available in the current context.

        :calls: `GET /api/v1/groups/:group_id/tabs \
        <https://canvas.instructure.com/doc/api/tabs.html#method.tabs.index>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.tab.Tab`
        """
        return PaginatedList(
            Tab,
            self._requester,
            'GET',
            'groups/%s/tabs' % (self.id),
            **combine_kwargs(**kwargs)
        )


class GroupMembership(CanvasObject):

    def __str__(self):
        return "{} - {} ({})".format(self.user_id, self.group_id, self.id)

    def update(self, mem_id, **kwargs):
        """
        Accept a membership request, or add/remove moderator rights.

        :calls: `PUT /api/v1/groups/:group_id/memberships/:membership_id \
        <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.update>`_

        :rtype: :class:`canvasapi.group.GroupMembership`
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
        :type user: :class:`canvasapi.user.User` or int

        :returns: An empty dictionary
        :rtype: dict
        """
        from canvasapi.user import User
        from canvasapi.util import obj_or_id

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

        :returns: An empty dictionary
        :rtype: dict
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
        Create a group.

        :calls: `POST /api/v1/group_categories/:group_category_id/groups \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.create>`_

        :rtype: :class:`canvasapi.group.Group`
        """
        response = self._requester.request(
            'POST',
            'group_categories/%s/groups' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return Group(self._requester, response.json())

    def update(self, **kwargs):
        """
        Update a group category.

        :calls: `PUT /api/v1/group_categories/:group_category_id \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.update>`_

        :rtype: :class:`canvasapi.group.GroupCategory`
        """
        response = self._requester.request(
            'PUT',
            'group_categories/%s' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return GroupCategory(self._requester, response.json())

    def delete(self):
        """
        Delete a group category.

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
        List groups in group category.

        :calls: `GET /api/v1/group_categories/:group_category_id/groups \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.groups>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.group.Group`
        """
        return PaginatedList(
            Group,
            self._requester,
            'GET',
            'group_categories/%s/groups' % (self.id)
        )

    def list_users(self, **kwargs):
        """
        List users in group category.

        :calls: `GET /api/v1/group_categories/:group_category_id/users \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.users>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.user.User`
        """
        from canvasapi.user import User
        return PaginatedList(
            User,
            self._requester,
            'GET',
            'group_categories/%s/users' % (self.id),
            **combine_kwargs(**kwargs)
        )

    def assign_members(self, sync=False):
        """
        Assign unassigned members.

        :calls: `POST /api/v1/group_categories/:group_category_id/assign_unassigned_members \
        <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.assign_unassigned_members>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of :class:`canvasapi.user.User`
            or :class:`canvasapi.progress.Progress`
        """
        from canvasapi.user import User
        from canvasapi.progress import Progress
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
