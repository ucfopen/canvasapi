from pycanvas.canvas_object import CanvasObject
from pycanvas.util import combine_kwargs


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

        :rtype: :class:`pycanvas.group.Group` or :class:`pycanvas.course.Course`
        """
        from pycanvas.group import Group
        from pycanvas.course import Course

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
        Deletes the discussion topic. This will also delete the assignment, if it's an assignment discussion.

        :calls: `DELETE /api/v1/courses/:course_id/discussion_topics/:topic_id \
                <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.destroy>`_

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

    def update_entry(self, entry_id, **kwargs):
        """
        Updates an existing discussion entry.

        :calls: `PUT /api/v1/courses/:course_id/discussion_topics/:topic_id/entries/:id \
                <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_entries.update>`_

        :rtype: :class:`pycanvas.discussion_topic.DiscussionTopic`
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

        :rtype: :class:`pycanvas.discussion_topic.DiscussionTopic`
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
