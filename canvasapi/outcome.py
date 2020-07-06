from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs, obj_or_id


class Outcome(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.url)

    def update(self, **kwargs):
        """
        Modify an existing outcome.

        :calls: `PUT /api/v1/outcomes/:id \
        <https://canvas.instructure.com/doc/api/outcomes.html#method.outcomes_api.update>`_

        :returns: True if updated, False otherwise.
        :rtype: bool
        """
        response = self._requester.request(
            "PUT", "outcomes/{}".format(self.id), _kwargs=combine_kwargs(**kwargs)
        )

        if "id" in response.json():
            super(Outcome, self).set_attributes(response.json())

        return "id" in response.json()


class OutcomeLink(CanvasObject):
    def __str__(self):
        return "Group {} with Outcome {} ({})".format(
            self.outcome_group, self.outcome, self.url
        )

    def context_ref(self):
        if self.context_type == "Course":
            return "courses/{}".format(self.context_id)
        elif self.context_type == "Account":
            return "accounts/{}".format(self.context_id)

    def get_outcome(self):
        """
        Return the linked outcome

        :calls: `GET /api/v1/outcomes/:id \
        <https://canvas.instructure.com/doc/api/outcomes.html#method.outcomes_api.show>`_

        :returns: Outcome object that was in the OutcomeLink
        :rtype: :class:`canvasapi.outcome.Outcome`
        """
        oid = self.outcome["id"]
        response = self._requester.request("GET", "outcomes/{}".format(oid))

        return Outcome(self._requester, response.json())

    def get_outcome_group(self):
        """
        Return the linked outcome group

        :calls: `GET /api/v1/global/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show>`_
            or `GET /api/v1/accounts/:account_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show>`_
            or `GET /api/v1/courses/:course_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show>`_

        :returns: Linked outcome group object.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        ogid = self.outcome_group["id"]
        response = self._requester.request(
            "GET", "{}/outcome_groups/{}".format(self.context_ref(), ogid)
        )

        return OutcomeGroup(self._requester, response.json())


class OutcomeGroup(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.url)

    def context_ref(self):
        if self.context_type == "Course":
            return "courses/{}".format(self.context_id)
        elif self.context_type == "Account":
            return "accounts/{}".format(self.context_id)
        elif self.context_type is None:
            return "global"

    def update(self, **kwargs):
        """
        Update an outcome group.

        :calls: `PUT /api/v1/global/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.update>`_
            or `PUT /api/v1/accounts/:account_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.update>`_
            or `PUT /api/v1/courses/:course_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.update>`_

        :returns: True if updated, False otherwise.
        :rtype: bool
        """
        response = self._requester.request(
            "PUT",
            "{}/outcome_groups/{}".format(self.context_ref(), self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        if "id" in response.json():
            super(OutcomeGroup, self).set_attributes(response.json())

        return "id" in response.json()

    def delete(self):
        """
        Delete an outcome group.

        :calls: `DELETE /api/v1/global/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.destroy>`_
            or `DELETE /api/v1/accounts/:account_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.destroy>`_
            or `DELETE /api/v1/courses/:course_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.destroy>`_

        :returns: True if successful, false if failed.
        :rtype: bool
        """
        response = self._requester.request(
            "DELETE", "{}/outcome_groups/{}".format(self.context_ref(), self.id)
        )

        if "id" in response.json():
            super(OutcomeGroup, self).set_attributes(response.json())

        return "id" in response.json()

    def get_linked_outcomes(self, **kwargs):
        """
        List linked outcomes.

        :calls: `GET /api/v1/global/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.outcomes>`_
            or `GET /api/v1/accounts/:account_id/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.outcomes>`_
            or `GET /api/v1/courses/:course_id/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.outcomes>`_

        :returns: Paginated List of Outcomes linked to the group.
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.outcome.OutcomeLink`
        """
        return PaginatedList(
            OutcomeLink,
            self._requester,
            "GET",
            "{}/outcome_groups/{}/outcomes".format(self.context_ref(), self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def link_existing(self, outcome):
        """
        Link to an existing Outcome.

        :calls: `PUT /api/v1/global/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link>`_
            or `PUT /api/v1/accounts/:account_id/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link>`_
            or `PUT /api/v1/courses/:course_id/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link>`_

        :param outcome: The object or ID of the outcome.
        :type outcome: :class:`canvasapi.outcome.Outcome` or int

        :returns: OutcomeLink object with current OutcomeGroup and newly linked Outcome.
        :rtype: :class:`canvasapi.outcome.OutcomeLink`
        """
        outcome_id = obj_or_id(outcome, "outcome", (Outcome,))

        response = self._requester.request(
            "PUT",
            "{}/outcome_groups/{}/outcomes/{}".format(
                self.context_ref(), self.id, outcome_id
            ),
        )

        return OutcomeLink(self._requester, response.json())

    def link_new(self, title, **kwargs):
        """
        Create a new Outcome and link it to this OutcomeGroup

        :calls: `POST /api/v1/global/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link>`_
            or `POST /api/v1/accounts/:account_id/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link>`_
            or `POST /api/v1/courses/:course_id/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link>`_

        :param title: The title of the new outcome.
        :type title: str

        :returns: OutcomeLink object with current OutcomeGroup and newly linked Outcome.
        :rtype: :class:`canvasapi.outcome.OutcomeLink`
        """
        response = self._requester.request(
            "POST",
            "{}/outcome_groups/{}/outcomes".format(self.context_ref(), self.id),
            title=title,
            _kwargs=combine_kwargs(**kwargs),
        )

        return OutcomeLink(self._requester, response.json())

    def unlink_outcome(self, outcome):
        """
        Remove an Outcome from and OutcomeLink

        :calls: `DELETE /api/v1/global/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.unlink>`_
            or `DELETE /api/v1/accounts/:account_id/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.unlink>`_
            or `DELETE /api/v1/courses/:course_id/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.unlink>`_

        :param outcome: The object or ID of the outcome.
        :type outcome: :class:`canvasapi.outcome.Outcome` or int

        :returns: True if successful, false if failed.
        :rtype: bool
        """
        outcome_id = obj_or_id(outcome, "outcome", (Outcome,))

        response = self._requester.request(
            "DELETE",
            "{}/outcome_groups/{}/outcomes/{}".format(
                self.context_ref(), self.id, outcome_id
            ),
        )

        if "context_id" in response.json():
            super(OutcomeGroup, self).set_attributes(response.json())

        return "context_id" in response.json()

    def get_subgroups(self, **kwargs):
        """
        List subgroups.

        :calls: `GET /api/v1/global/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.subgroups>`_
            or `GET /api/v1/accounts/:account_id/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.subgroups>`_
            or `GET /api/v1/courses/:course_id/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.subgroups>`_

        :returns: Paginated List of OutcomeGroups linked to the current group.
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.outcome.OutcomeGroup`
        """
        return PaginatedList(
            OutcomeGroup,
            self._requester,
            "GET",
            "{}/outcome_groups/{}/subgroups".format(self.context_ref(), self.id),
            {"context_type": self.context_type, "context_id": self.context_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def create_subgroup(self, title, **kwargs):
        """
        Create a subgroup of the current group

        :calls: `POST /api/v1/global/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.create>`_
            or `POST /api/v1/accounts/:account_id/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.create>`_
            or `POST /api/v1/courses/:course_id/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.create>`_

        :param title: The title of the subgroup.
        :type title: str

        :returns: Itself as an OutcomeGroup object.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        response = self._requester.request(
            "POST",
            "{}/outcome_groups/{}/subgroups".format(self.context_ref(), self.id),
            title=title,
            _kwargs=combine_kwargs(**kwargs),
        )

        return OutcomeGroup(self._requester, response.json())

    def import_outcome_group(self, outcome_group):
        """
        Import an outcome group as a subgroup into the current outcome group

        :calls: `POST /api/v1/global/outcome_groups/:id/import \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.import>`_
            or `POST /api/v1/accounts/:account_id/outcome_groups/:id/import \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.import>`_
            or `POST /api/v1/courses/:course_id/outcome_groups/:id/import \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.import>`_

        :param outcome: The object or ID of the outcome group to import.
        :type outcome: :class:`canvasapi.outcome.OutcomeGroup` or int

        :returns: Itself as an OutcomeGroup object.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        source_outcome_group_id = obj_or_id(
            outcome_group, "outcome_group", (OutcomeGroup,)
        )

        response = self._requester.request(
            "POST",
            "{}/outcome_groups/{}/import".format(self.context_ref(), self.id),
            source_outcome_group_id=source_outcome_group_id,
        )

        return OutcomeGroup(self._requester, response.json())
