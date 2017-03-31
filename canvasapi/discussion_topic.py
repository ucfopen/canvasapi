from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs


class DiscussionTopic(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)

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
            raise ValueError("Discussion Topic does not have a course_id or group_id")

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
            raise ValueError("Discussion Topic does not have a course_id or group_id")

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

    def delete(self, topic_id):
        """
        Deletes the discussion topic. This will also delete the assignment.

        :calls: `DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.destroy>`_

            or `DELETE /api/v1/groups/:group_id/discussion_topics/:topic_id \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.destroy>`_

        :param topic_id: ID of a topic.
        :type topic_id: int
        :returns: True if the discussion topic was deleted, False otherwise.
        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            '%ss/%s/discussion_topics/%s' % (
                self.parent_type,
                self.parent_id,
                self.id
            )
        )
        return 'deleted_at' in response.json()

    def update(self, **kwargs):
        """
        Updates an existing discussion topic for the course or group.

        :calls: `PUT /api/v1/courses/:course_id/discussion_topics/:topic_id \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.update>`_

            or `PUT /api/v1/groups/:group_id/discussion_topics/:topic_id \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.update>`_

        :rtype: :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        response = self._requester.request(
            'PUT',
            '%ss/%s/discussion_topics/%s' % (
                self.parent_type,
                self.parent_id,
                self.id
            ),
            **combine_kwargs(**kwargs)
        )
        return DiscussionTopic(self._requester, response.json())

    def update_entry(self, entry_id, **kwargs):
        """
        Updates an existing discussion entry.

        :calls: `PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:id \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_entries.update>`_

            or `PUT /api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:id \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_entries.update>`_

        :param entry_id: ID of an entry.
        :type entry_id: int
        :rtype: bool
        """
        response = self._requester.request(
            'PUT',
            '%ss/%s/discussion_topics/%s/entries/%s' % (
                self.parent_type,
                self.parent_id,
                self.id,
                entry_id
            ),
            **combine_kwargs(**kwargs)
        )
        return 'updated_at' in response.json()

    def delete_entry(self, entry_id, **kwargs):
        """
        Delete a discussion entry.

        :calls: `DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:id \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_entries.destroy>`_

            or `DELETE /api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:id \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_entries.destroy>`_

        :param entry_id: ID of an entry.
        :type entry_id: int
        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            '%ss/%s/discussion_topics/%s/entries/%s' % (
                self.parent_type,
                self.parent_id,
                self.id,
                entry_id
            ),
            **combine_kwargs(**kwargs)
        )
        return 'deleted_at' in response.json()

    def post_entry(self, **kwargs):
        """
        Creates a new entry in a discussion topic.

        :calls: `POST /api/v1/courses/:course_id/discussion_topics/:topic_id/entries \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.add_entry>`_

            or `POST /api/v1/groups/:group_id/discussion_topics/:topic_id/entries \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.add_entry>`_

        :rtype: bool
        """
        response = self._requester.request(
            'POST',
            '%ss/%s/discussion_topics/%s/entries' % (
                self.parent_type,
                self.parent_id,
                self.id
            ),
            **combine_kwargs(**kwargs)
        )
        return 'created_at' in response.json()

    def list_topic_entries(self, **kwargs):
        """
        Retreive the paginated top-level entries in a discussion topic.

        :calls: `GET /api/v1/courses/:course_id/discussion_topics/:topic_id/entries \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.entries>`_

            or `GET /api/v1/groups/:group_id/discussion_topics/:topic_id/entries \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.entries>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        return PaginatedList(
            DiscussionTopic,
            self._requester,
            'GET',
            '%ss/%s/discussion_topics/%s/entries' % (
                self.parent_type,
                self.parent_id,
                self.id
            ),
            **combine_kwargs(**kwargs)
        )

    def post_reply(self, entry_id, **kwargs):
        """
        Add a reply to an entry in a discussion topic.

        :calls: `POST
            /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/replies
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.add_reply>`_

            or `POST /api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:entry_id/replies
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.add_reply>`_

        :param entry_id: ID of an entry.
        :type entry_id: int
        :rtype: :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        response = self._requester.request(
            'POST',
            '%ss/%s/discussion_topics/%s/entries/%s/replies' % (
                self.parent_type,
                self.parent_id,
                self.id,
                entry_id
            ),
            **combine_kwargs(**kwargs)
        )
        return DiscussionTopic(self._requester, response.json())

    def list_entry_replies(self, entry_id, **kwargs):
        """
        Retrieves the replies to a top-level entry in a discussion topic.

        :calls: `GET
            /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/replies \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.replies>`_

            or `GET
            /api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:entry_id/replies \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.replies>`_

        :param entry_id: ID of an entry.
        :type entry_id: int
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        return PaginatedList(
            DiscussionTopic,
            self._requester,
            'GET',
            '%ss/%s/discussion_topics/%s/entries/%s/replies' % (
                self.parent_type,
                self.parent_id,
                self.id,
                entry_id
            ),
            **combine_kwargs(**kwargs)
        )

    def list_entries(self, **kwargs):
        """
        Retrieve a paginated list of discussion entries, given a list of ids.

        :calls: `GET /api/v1/courses/:course_id/discussion_topics/:topic_id/entry_list \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.entries>`_

            or `GET /api/v1/groups/:group_id/discussion_topics/:topic_id/entry_list \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.entries>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        return PaginatedList(
            DiscussionTopic,
            self._requester,
            'GET',
            '%ss/%s/discussion_topics/%s/entry_list' % (
                self.parent_type,
                self.parent_id,
                self.id
            ),
            **combine_kwargs(**kwargs)
        )

    def mark_as_read(self):
        """
        Mark the initial text of the discussion topic as read.

        :calls: `PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/read \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_topic_read>`_

            or `PUT /api/v1/groups/:group_id/discussion_topics/:topic_id/read \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_topic_read>`_

        :rtype: bool
        """
        response = self._requester.request(
            'PUT',
            '%ss/%s/discussion_topics/%s/read' % (
                self.parent_type,
                self.parent_id,
                self.id
            )
        )
        return response.status_code == 204

    def mark_as_unread(self):
        """
        Mark the initial text of the discussion topic as unread.

        :calls: `DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/read \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_topic_read>`_

            or `DELETE /api/v1/groups/:group_id/discussion_topics/:topic_id/read \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_topic_read>`_

        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            '%ss/%s/discussion_topics/%s/read' % (
                self.parent_type,
                self.parent_id,
                self.id
            )
        )
        return response.status_code == 204

    def mark_entry_as_read(self, entry_id):
        """
        Mark a discussion entry as read.

        :calls: `PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/read\
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_entry_read>`_

            or `PUT /api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:entry_id/read \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_entry_read>`_

        :rtype: bool
        """
        response = self._requester.request(
            'PUT',
            '%ss/%s/discussion_topics/%s/entries/%s/read' % (
                self.parent_type,
                self.parent_id,
                self.id,
                entry_id
            )
        )
        return response.status_code == 204

    def mark_entry_as_unread(self, entry_id):
        """
        Mark a discussion entry as unread.

        :calls: `DELETE
            /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/read \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_entry_unread>`_

            or `DELETE
            /api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:entry_id/read \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_entry_unread>`_

        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            '%ss/%s/discussion_topics/%s/entries/%s/read' % (
                self.parent_type,
                self.parent_id,
                self.id,
                entry_id
            )
        )
        return response.status_code == 204

    def mark_entries_as_read(self, **kwargs):
        """
        Mark the discussion topic and all its entries as read.

        :calls: `PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/read_all \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_all_read>`_

            or `PUT /api/v1/groups/:group_id/discussion_topics/:topic_id/read_all \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_all_read>`_

        :rtype: bool
        """
        response = self._requester.request(
            'PUT',
            '%ss/%s/discussion_topics/%s/read_all' % (
                self.parent_type,
                self.parent_id,
                self.id
            ),
            **combine_kwargs(**kwargs)
        )
        return response.status_code == 204

    def mark_entries_as_unread(self, **kwargs):
        """
        Mark the discussion topic and all its entries as read.

        :calls: `DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/read_all \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_all_read>`_

            or `DELETE /api/v1/groups/:group_id/discussion_topics/:topic_id/read_all \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.mark_all_read>`_

        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            '%ss/%s/discussion_topics/%s/read_all' % (
                self.parent_type,
                self.parent_id,
                self.id
            ),
            **combine_kwargs(**kwargs)
        )
        return response.status_code == 204

    def rate_entry(self, entry_id, **kwargs):
        """
        Rate a discussion entry.

        :calls: `POST
            /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/rating \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.rate_entry>`_

            or `POST
            /api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:entry_id/rating \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.rate_entry>`_

        :rtype: bool
        """
        response = self._requester.request(
            'POST',
            '%ss/%s/discussion_topics/%s/entries/%s/rating' % (
                self.parent_type,
                self.parent_id,
                self.id,
                entry_id
            ),
            **combine_kwargs(**kwargs)
        )
        return response.status_code == 204

    def subscribe(self):
        """
        Subscribe to a topic to receive notifications about new entries.

        :calls: `PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/subscribed \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.subscribe_topic>`_

            or `PUT /api/v1/groups/:group_id/discussion_topics/:topic_id/subscribed \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.subscribe_topic>`_

        :rtype: bool
        """
        response = self._requester.request(
            'PUT',
            '%ss/%s/discussion_topics/%s/subscribed' % (
                self.parent_type,
                self.parent_id,
                self.id
            )
        )
        return response.status_code == 204

    def unsubscribe(self):
        """
        Unsubscribe from a topic to stop receiving notifications about new entries.

        :calls: `DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/subscribed \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.unsubscribe_topic>`_

            or `DELETE /api/v1/groups/:group_id/discussion_topics/:topic_id/subscribed \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.unsubscribe_topic>`_

        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            '%ss/%s/discussion_topics/%s/subscribed' % (
                self.parent_type,
                self.parent_id,
                self.id
            )
        )
        return response.status_code == 204
