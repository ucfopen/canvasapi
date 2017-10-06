from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs, obj_or_id


@python_2_unicode_compatible
class Outcome(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.title, self.url)

    def show(self, **kwargs):
        """
        Returns the details of the outcome with the given id.

        :calls: `GET /api/v1/outcomes/:id \
        <https://canvas.instructure.com/doc/api/outcomes.html#method.outcomes_api.show>`_

        :returns: Itself as an object.
        :rtype: :class:`canvasapi.outcome.Outcome`
        """
        response = self._requester.request(
            'GET',
            'outcomes/%s' % (self.id)
        )
        return Outcome(self._requester, response.json())

    def update(self, **kwargs):
        """
        Modify an existing outcome.

        :calls: `PUT /api/v1/outcomes/:id \
        <https://canvas.instructure.com/doc/api/outcomes.html#method.outcomes_api.update>`_

        :returns: True if updated, False otherwise.
        :rtype: bool
        """
        response = self._requester.request(
            'PUT',
            'outcomes/%s' % (self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        if 'id' in response.json():
            super(Outcome, self).set_attributes(response.json())

        return 'id' in response.json()


@python_2_unicode_compatible
class OutcomeLink(CanvasObject):

    def __str__(self):
        return "Group {} with Outcome {} ({})".format(
            self.outcome_group,
            self.outcome,
            self.url
        )

    def get_outcome(self):
        oid = self.outcome['id']
        response = self._requester.request(
            'GET',
            'outcomes/%s' % (oid)
        )

        return Outcome(self._requester, response.json())


@python_2_unicode_compatible
class OutcomeGroup(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.title, self.url)

    def context_ref(self):
        if self.context_type == 'Course':
            return 'courses/%s' % (self.context_id)
        elif self.context_type == 'Account':
            return 'accounts/%s' % (self.context_id)
        elif self.context_type is None:
            return 'global'

    def show(self):
        """
        Returns the details of the Outcome Group with the given id.

        :calls: `GET /api/v1/global/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show>`_
            or `GET /api/v1/accounts/:account_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show>`_
            or `GET /api/v1/courses/:course_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.show>`_

        :returns: Itself as an OutcomeGroup object.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        response = self._requester.request(
            'GET',
            '%s/outcome_groups/%s' % (self.context_ref(), self.id)
        )

        return OutcomeGroup(self._requester, response.json())

    def update(self, **kwargs):
        """
        Update an outcome group.

        :calls: `PUT /api/v1/global/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.update`_
            or `PUT /api/v1/accounts/:account_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.update`_
            or `PUT /api/v1/courses/:course_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.update`_

        :returns: True if updated, False otherwise.
        :rtype: bool
        """
        response = self._requester.request(
            'PUT',
            '%s/outcome_groups/%s' % (self.context_ref(), self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        if 'id' in response.json():
            super(OutcomeGroup, self).set_attributes(response.json())

        return 'id' in response.json()

    def delete(self):
        """
        Delete an outcome group.

        :calls: `DELETE /api/v1/global/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.destroy`_
            or `DELETE /api/v1/accounts/:account_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.destroy`_
            or `DELETE /api/v1/courses/:course_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.destroy`_

        :returns: True if successful, false if failed.
        :rtype: bool
        """
        response = self._requester.request(
            'DELETE',
            '%s/outcome_groups/%s' % (self.context_ref(), self.id)
        )

        if 'id' in response.json():
            super(OutcomeGroup, self).set_attributes(response.json())

        return 'id' in response.json()

    def list_linked_outcomes(self, **kwargs):
        """
        List linked outcomes.

        :calls: `GET /api/v1/global/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.outcomes`_
            or `GET /api/v1/accounts/:account_id/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.outcomes`_
            or `GET /api/v1/courses/:course_id/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.outcomes`_

        :returns: Paginated List of Outcomes linked to the group.
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.outcome.OutcomeLink`
        """
        return PaginatedList(
            OutcomeLink,
            self._requester,
            'GET',
            '%s/outcome_groups/%s/outcomes' % (self.context_ref(), self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

    def link_existing(self, outcome):
        """
        Link to an existing Outcome.

        :calls: `PUT /api/v1/global/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link`_
            or `PUT /api/v1/accounts/:account_id/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link`_
            or `PUT /api/v1/courses/:course_id/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link`_

        :returns: OutcomeLink object with current OutcomeGroup and newly linked Outcome.
        :rtype: :class:`canvasapi.outcome.OutcomeLink`
        """
        outcome_id = obj_or_id(outcome, "outcome", (Outcome,))

        response = self._requester.request(
            'PUT',
            '%s/outcome_groups/%s/outcomes/%s' % (
                self.context_ref(),
                self.id,
                outcome_id
            )
        )

        return OutcomeLink(self._requester, response.json())

    def link_new(self, title, **kwargs):
        """
        Create a new Outcome and link it to this OutcomeGroup

        :calls: `POST /api/v1/global/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link`_
            or `POST /api/v1/accounts/:account_id/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link`_
            or `POST /api/v1/courses/:course_id/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link`_

        :params: title, description, ratings, and mastery points.
            Title is the only required param.

        :returns: OutcomeLink object with current OutcomeGroup and newly linked Outcome.
        :rtype: :class:`canvasapi.outcome.OutcomeLink`
        """
        response = self._requester.request(
            'POST',
            '%s/outcome_groups/%s/outcomes' % (self.context_ref(), self.id),
            title=title,
            _kwargs=combine_kwargs(**kwargs)
        )

        return OutcomeLink(self._requester, response.json())

    def unlink_outcome(self, outcome):
        """
        Remove an Outcome from and OutcomeLink

        :calls: `DELETE /api/v1/global/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.unlink`_
            or `DELETE /api/v1/accounts/:account_id/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.unlink`_
            or `DELETE /api/v1/courses/:course_id/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.unlink`_

        :returns: True if successful, false if failed.
        :rtype: bool
        """
        outcome_id = obj_or_id(outcome, "outcome", (Outcome,))

        response = self._requester.request(
            'DELETE',
            '%s/outcome_groups/%s/outcomes/%s' % (
                self.context_ref(),
                self.id,
                outcome_id
            )
        )

        if 'context_id' in response.json():
            super(OutcomeGroup, self).set_attributes(response.json())

        return 'context_id' in response.json()

    def list_subgroups(self):
        """
        List subgroups.

        :calls: `GET /api/v1/global/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.subgroups`_
            or `GET /api/v1/accounts/:account_id/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.subgroups`_
            or `GET /api/v1/courses/:course_id/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.subgroups`_

        :returns: Paginated List of OutcomeGroups linked to the current group.
        :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
            :class:`canvasapi.outcome.OutcomeGroup`
        """
        return PaginatedList(
            OutcomeGroup,
            self._requester,
            'GET',
            '%s/outcome_groups/%s/subgroups' % (self.context_ref(), self.id)
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
            'POST',
            '%s/outcome_groups/%s/subgroups' % (self.context_ref(), self.id),
            title=title,
            _kwargs=combine_kwargs(**kwargs)
        )

        return OutcomeGroup(self._requester, response.json())

    def import_outcome_group(self, source_outcome_group_id):
        """
        Import an outcome group as a subgroup into the current outcome group

        :calls: `POST /api/v1/global/outcome_groups/:id/import \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.import>`_
            or `POST /api/v1/accounts/:account_id/outcome_groups/:id/import \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.import>`_
            or `POST /api/v1/courses/:course_id/outcome_groups/:id/import \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.import>`_

        :param source_outcome_group_id: The id of the Outcome Group to be imported.
        :type source_outcome_group_id: int

        :returns: Itself as an OutcomeGroup object.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        response = self._requester.request(
            'POST',
            '%s/outcome_groups/%s/import' % (self.context_ref(), self.id),
            source_outcome_group_id=source_outcome_group_id
        )

        return OutcomeGroup(self._requester, response.json())
