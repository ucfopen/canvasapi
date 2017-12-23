from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs, obj_or_id


@python_2_unicode_compatible
class DiscussionTopic(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)

    @property
    def _parent_id(self):
        """
        Return the id of the course or group that spawned this discussion topic.

        :rtype: int
        """
        if hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'group_id'):
            return self.group_id
        else:
            raise ValueError("Discussion Topic does not have a course_id or group_id")

    @property
    def _parent_type(self):
        """
        Return whether the discussion topic was spawned from a course or group.

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
        Return the object that spawned this discussion topic.

        :rtype: :class:`canvasapi.group.Group` or :class:`canvasapi.course.Course`
        """
        from canvasapi.group import Group
        from canvasapi.course import Course

        response = self._requester.request(
            'GET',
            '{}s/{}'.format(self._parent_type, self._parent_id)
        )

        if self._parent_type == 'group':
            return Group(self._requester, response.json())
        elif self._parent_type == 'course':
            return Course(self._requester, response.json())

    def delete(self):
        """
        Deletes the discussion topic. This will also delete the assignment.

        :calls: `DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.destroy>`_

            or `DELETE /api/v1/groups/:group_id/discussion_topics/:topic_id \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.destroy>`_

        :returns: True if the discussion topic was deleted, False otherwise.
        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            '{}s/{}/discussion_topics/{}'.format(
                self._parent_type,
                self._parent_id,
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
            '{}s/{}/discussion_topics/{}'.format(
                self._parent_type,
                self._parent_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        return DiscussionTopic(self._requester, response.json())

    def post_entry(self, **kwargs):
        """
        Creates a new entry in a discussion topic.

        :calls: `POST /api/v1/courses/:course_id/discussion_topics/:topic_id/entries \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.add_entry>`_

            or `POST /api/v1/groups/:group_id/discussion_topics/:topic_id/entries \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.add_entry>`_

        :rtype: :class:`canvasapi.discussion_topic.DiscussionEntry`
        """
        response = self._requester.request(
            'POST',
            '{}s/{}/discussion_topics/{}/entries'.format(
                self._parent_type,
                self._parent_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update({
            'discussion_id': self.id,
            '{}_id'.format(self._parent_type): self._parent_id
        })
        return DiscussionEntry(self._requester, response_json)

    def list_topic_entries(self, **kwargs):
        """
        Retreive the top-level entries in a discussion topic.

        :calls: `GET /api/v1/courses/:course_id/discussion_topics/:topic_id/entries \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.entries>`_

            or `GET /api/v1/groups/:group_id/discussion_topics/:topic_id/entries \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.entries>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.discussion_topic.DiscussionEntry`
        """
        return PaginatedList(
            DiscussionEntry,
            self._requester,
            'GET',
            '{}s/{}/discussion_topics/{}/entries'.format(
                self._parent_type,
                self._parent_id,
                self.id
            ),
            {
                'discussion_id': self.id,
                '{}_id'.format(self._parent_type): self._parent_id
            },
            _kwargs=combine_kwargs(**kwargs)
        )

    def list_entries(self, ids, **kwargs):
        """
        Retrieve a paginated list of discussion entries, given a list
        of ids. Entries will be returned in id order, smallest id first.

        :calls: `GET /api/v1/courses/:course_id/discussion_topics/:topic_id/entry_list \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.entry_list>`_

            or `GET /api/v1/groups/:group_id/discussion_topics/:topic_id/entry_list \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.entry_list>`_

        :param ids: A list of entry objects or IDs to retrieve.
        :type ids: :class:`canvasapi.discussion_topic.DiscussionEntry`, or list or tuple of int

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.discussion_topic.DiscussionEntry`
        """

        entry_ids = [obj_or_id(item, "ids", (DiscussionEntry, )) for item in ids]

        kwargs.update(ids=entry_ids)
        return PaginatedList(
            DiscussionEntry,
            self._requester,
            'GET',
            '{}s/{}/discussion_topics/{}/entry_list'.format(
                self._parent_type,
                self._parent_id,
                self.id
            ),
            {
                'discussion_id': self.id,
                '{}_id'.format(self._parent_type): self._parent_id
            },
            _kwargs=combine_kwargs(**kwargs),
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
            '{}s/{}/discussion_topics/{}/read'.format(
                self._parent_type,
                self._parent_id,
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
            '{}s/{}/discussion_topics/{}/read'.format(
                self._parent_type,
                self._parent_id,
                self.id
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
            '{}s/{}/discussion_topics/{}/read_all'.format(
                self._parent_type,
                self._parent_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
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
            '{}s/{}/discussion_topics/{}/read_all'.format(
                self._parent_type,
                self._parent_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
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
            '{}s/{}/discussion_topics/{}/subscribed'.format(
                self._parent_type,
                self._parent_id,
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
            '{}s/{}/discussion_topics/{}/subscribed'.format(
                self._parent_type,
                self._parent_id,
                self.id
            )
        )
        return response.status_code == 204


@python_2_unicode_compatible
class DiscussionEntry(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.message, self.id)

    @property
    def _discussion_parent_id(self):
        """
        Return the id of the course or group that spawned the discussion topic.

        :rtype: int
        """
        if hasattr(self, 'course_id'):
            return self.course_id
        elif hasattr(self, 'group_id'):
            return self.group_id
        else:
            raise ValueError("Discussion Topic does not have a course_id or group_id")

    @property
    def _discussion_parent_type(self):
        """
        Return whether the discussion topic was spawned from a course or group.

        :rtype: str
        """
        if hasattr(self, 'course_id'):
            return 'course'
        elif hasattr(self, 'group_id'):
            return 'group'
        else:
            raise ValueError("Discussion Topic does not have a course_id or group_id")

    def get_discussion(self):
        """
        Return the discussion topic object this entry is related to

        :rtype: :class:`canvasapi.discussion_topic.DiscussionTopic`
        """

        response = self._requester.request(
            'GET',
            '{}s/{}/discussion_topics/{}'.format(
                self._discussion_parent_type,
                self._discussion_parent_id,
                self.discussion_id
            )
        )

        response_json = response.json()
        response_json.update(
            {'{}_id'.format(self._discussion_parent_type): self._discussion_parent_id}
        )

        return DiscussionTopic(self._requester, response.json())

    def update(self, **kwargs):
        """
        Updates an existing discussion entry.

        :calls: `PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:id \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_entries.update>`_

            or `PUT /api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:id \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_entries.update>`_

        :rtype: bool
        """
        response = self._requester.request(
            'PUT',
            '{}s/{}/discussion_topics/{}/entries/{}'.format(
                self._discussion_parent_type,
                self._discussion_parent_id,
                self.discussion_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )

        if response.json().get('updated_at'):
            super(DiscussionEntry, self).set_attributes(response.json())

        return 'updated_at' in response.json()

    def delete(self, **kwargs):
        """
        Delete this discussion entry.

        :calls: `DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:id \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_entries.destroy>`_

            or `DELETE /api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:id \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_entries.destroy>`_

        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            '{}s/{}/discussion_topics/{}/entries/{}'.format(
                self._discussion_parent_type,
                self._discussion_parent_id,
                self.discussion_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        return 'deleted_at' in response.json()

    def post_reply(self, **kwargs):
        """
        Add a reply to this entry.

        :calls: `POST
            /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/replies
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.add_reply>`_

            or `POST /api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:entry_id/replies
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.add_reply>`_

        :rtype: :class:`canvasapi.discussion_topic.DiscussionEntry`
        """
        response = self._requester.request(
            'POST',
            '{}s/{}/discussion_topics/{}/entries/{}/replies'.format(
                self._discussion_parent_type,
                self._discussion_parent_id,
                self.discussion_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )
        response_json = response.json()
        response_json.update(discussion_id=self.discussion_id)
        return DiscussionEntry(self._requester, response_json)

    def list_replies(self, **kwargs):
        """
        Retrieves the replies to a top-level entry in a discussion topic.

        :calls: `GET
            /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/replies \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.replies>`_

            or `GET
            /api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:entry_id/replies \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.replies>`_

        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.discussion_topic.DiscussionEntry`
        """
        return PaginatedList(
            DiscussionEntry,
            self._requester,
            'GET',
            '{}s/{}/discussion_topics/{}/entries/{}/replies'.format(
                self._discussion_parent_type,
                self._discussion_parent_id,
                self.discussion_id,
                self.id
            ),
            {
                'discussion_id': self.discussion_id,
                '{}_id'.format(self._discussion_parent_type): self._discussion_parent_id
            },
            _kwargs=combine_kwargs(**kwargs)
        )

    # TODO: update to use correct class
    def mark_as_read(self):
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
            '{}s/{}/discussion_topics/{}/entries/{}/read'.format(
                self._discussion_parent_type,
                self._discussion_parent_id,
                self.discussion_id,
                self.id
            )
        )
        return response.status_code == 204

    # TODO: update to use correct class
    def mark_as_unread(self):
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
            '{}s/{}/discussion_topics/{}/entries/{}/read'.format(
                self._discussion_parent_type,
                self._discussion_parent_id,
                self.discussion_id,
                self.id
            )
        )
        return response.status_code == 204

    def rate(self, rating, **kwargs):
        """
        Rate this discussion entry.

        :calls: `POST
            /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:entry_id/rating \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.rate_entry>`_

            or `POST
            /api/v1/groups/:group_id/discussion_topics/:topic_id/entries/:entry_id/rating \
            <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.rate_entry>`_

        :param rating: A rating to set on this entry. Only 0 and 1 are accepted.
        :type rating: int
        :rtype: bool
        """
        if rating not in (0, 1):
            raise ValueError("`rating` must be 0 or 1.")

        response = self._requester.request(
            'POST',
            '{}s/{}/discussion_topics/{}/entries/{}/rating'.format(
                self._discussion_parent_type,
                self._discussion_parent_id,
                self.discussion_id,
                self.id
            ),
            rating=rating,
            _kwargs=combine_kwargs(**kwargs)
        )
        return response.status_code == 204
