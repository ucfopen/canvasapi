from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class PlannerNote(CanvasObject):
    def __str__(self):
        return "{} {} ({})".format(self.title, self.todo_date, self.id)

    def update(self, **kwargs):
        """
        Update a planner note for the current user

        :calls: `PUT /api/v1/planner_notes/:id \
        <https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.update>`_

        :rtype: :class:`canvasapi.planner.PlannerNote`
        """

        response = self._requester.request(
            "PUT", "planner_notes/{}".format(self.id), _kwargs=combine_kwargs(**kwargs)
        )
        return PlannerNote(self._requester, response.json())

    def delete(self, **kwargs):
        """
        Delete a planner note for the current user

        :calls: `DELETE /api/v1/planner_notes/:id \
        <https://canvas.instructure.com/doc/api/planner.html#method.planner_notes.destroy>`_

        :rtype: :class:`canvasapi.planner.PlannerNote`
        """
        response = self._requester.request(
            "DELETE",
            "planner_notes/{}".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return PlannerNote(self._requester, response.json())


class PlannerOverride(CanvasObject):
    def __str__(self):
        return "{} {} ({})".format(self.plannable_id, self.marked_complete, self.id)

    def update(self, **kwargs):
        """
        Update a planner override's visibilty for the current user

        :calls: `PUT /api/v1/planner/overrides/:id \
        <https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.update>`_

        :rtype: :class:`canvasapi.planner.PlannerOverride`
        """

        response = self._requester.request(
            "PUT",
            "planner/overrides/{}".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return PlannerOverride(self._requester, response.json())

    def delete(self, **kwargs):
        """
        Delete a planner override for the current user

        :calls: `DELETE /api/v1/planner/overrides/:id \
        <https://canvas.instructure.com/doc/api/planner.html#method.planner_overrides.destroy>`_

        :rtype: :class:`canvasapi.planner.PlannerOverride`
        """
        response = self._requester.request(
            "DELETE",
            "planner/overrides/{}".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return PlannerOverride(self._requester, response.json())
