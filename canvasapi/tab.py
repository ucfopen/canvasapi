from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class Tab(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.label, self.id)

    def update(self, **kwargs):
        """
        Update a tab for a course.

        Note: Home and Settings tabs are not manageable, and can't be
        hidden or moved.

        :calls: `PUT /api/v1/courses/:course_id/tabs/:tab_id \
        <https://canvas.instructure.com/doc/api/tabs.html#method.tabs.update>`_

        :rtype: :class:`canvasapi.tab.Tab`
        """
        if not hasattr(self, "course_id"):
            raise ValueError("Can only update tabs from a Course.")

        response = self._requester.request(
            "PUT",
            "courses/{}/tabs/{}".format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"course_id": self.course_id})

        super(Tab, self).set_attributes(response_json)

        return self
