from canvasapi.canvas_object import CanvasObject


# As of June 30th, 2025, the SmartSearch API is experimental, and may cause breaks
# on code changes. If you've landed here on an error, it could be the API was updated.
class SearchResult(CanvasObject):
    """
    Represents a result (which can be of multiple types) return from the `SmartSearch API. \
    <https://canvas.instructure.com/doc/api/smart_search.html#method.smart_search.search>`_
    """

    REQUIRED_FIELDS = ["content_id", "content_type", "title", "html_url"]

    def __init__(self, requester, attributes):
        super(SearchResult, self).__init__(requester, attributes)

        missing = [f for f in self.REQUIRED_FIELDS if not hasattr(self, f)]
        if missing:
            raise ValueError("SearchResult missing required fields: {}".format(missing))

    def __str__(self):
        # Using Untitled as a fallback in the event the API changes.
        return "<SearchResult: {} - {}>".format(
            self.content_type, getattr(self, "title", "Untitled")
        )

    def resolve(self):
        """
        Resolve this SearchResult into the corresponding Canvas object.

        :return: The full object (e.g., Page, Assignment, DiscussionTopic), or None if
                resolution fails.
        :rtype: :class:`canvasapi.page.Page`, :class:`canvasapi.assignment.Assignment`,
                :class:`canvasapi.discussion_topic.DiscussionTopic`
        """
        if not hasattr(self, "content_type") or not hasattr(self, "content_id"):
            raise ValueError(
                "SearchResult is missing 'content_type' or 'content_id' for resolution"
            )

        # Use course_id set from Course.smartsearch to create a "fake" Course object to work from
        from canvasapi.course import Course

        course = Course(self._requester, {"id": self.course_id})

        types = {
            "WikiPage": course.get_page,
            "Assignment": course.get_assignment,
            "DiscussionTopic": course.get_discussion_topic,
            "Announcement": course.get_discussion_topic,
        }

        resolver = types.get(self.content_type)
        if not resolver:
            raise ValueError(
                "Resolution not supported for content_type: {}".format(
                    self.content_type
                )
            )

        return resolver(self.content_id)
