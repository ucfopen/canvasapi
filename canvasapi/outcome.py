from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs


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

        :returns: Updated Outcome object.
        :rtype: :class:`canvasapi.outcome.Outcome`
        """
        response = self._requester.request(
            'PUT',
            'outcomes/%s' % (self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return Outcome(self._requester, response.json())


@python_2_unicode_compatible
class OutcomeLink(CanvasObject):

    def __str__(self):
        return "Group {} with Outcome {} ({})".format(
            self.outcome_group,
            self.outcome,
            self.url
        )


@python_2_unicode_compatible
class OutcomeGroup(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.title, self.url)

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
        if self.context_type is "Course":
            response = self._requester.request(
                'GET',
                'courses/%s/outcome_groups/%s' % (self.context_id, self.id)
            )
        elif self.context_type is "Account":
            response = self._requester.request(
                'GET',
                'accounts/%s/outcome_groups/%s' % (self.context_id, self.id)
            )
        else:  # context_type and context_id should be "null" if global. Test this.
            response = self._requester.request(
                'GET',
                'global/outcome_groups/%s' % (self.id)
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

        :returns: Updated object as an OutcomeGroup object.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        if self.context_type is "Course":
            response = self._requester.request(
                'PUT',
                'courses/%s/outcome_groups/%s' % (self.context_id, self.id),
                _kwargs=combine_kwargs(**kwargs)
            )
        elif self.context_type is "Account":
            response = self._requester.request(
                'PUT',
                'accounts/%s/outcome_groups/%s' % (self.context_id, self.id),
                _kwargs=combine_kwargs(**kwargs)
            )
        else:  # context_type and context_id should be "null" if global. Test this.
            response = self._requester.request(
                'PUT',
                'global/outcome_groups/%s' % (self.id),
                _kwargs=combine_kwargs(**kwargs)
            )

        return OutcomeGroup(self._requester, response.json())

    def delete(self):
        """
        Delete an outcome group.

        :calls: `DELETE /api/v1/global/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.destroy`_
            or `DELETE /api/v1/accounts/:account_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.destroy`_
            or `DELETE /api/v1/courses/:course_id/outcome_groups/:id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.destroy`_

        :returns: Deleted OutcomeGroup object.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        if self.context_type is "Course":
            response = self._requester.request(
                'DELETE',
                'courses/%s/outcome_groups/%s' % (self.context_id, self.id)
            )
        elif self.context_type is "Account":
            response = self._requester.request(
                'DELETE',
                'accounts/%s/outcome_groups/%s' % (self.context_id, self.id)
            )
        else:  # context_type and context_id should be "null" if global. Test this.
            response = self._requester.request(
                'DELETE',
                'global/outcome_groups/%s' % (self.id)
            )

        return OutcomeGroup(self._requester, response.json())

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
        if self.context_type is "Course":
            return PaginatedList(
                OutcomeLink,
                self._requester,
                'GET',
                'courses/%s/outcome_groups/%s/outcomes' % (self.context_id, self.id),
                _kwargs=combine_kwargs(**kwargs)
            )
        elif self.context_type is "Account":
            return PaginatedList(
                OutcomeLink,
                self._requester,
                'GET',
                'accounts/%s/outcome_groups/%s/outcomes' % (self.context_id, self.id),
                _kwargs=combine_kwargs(**kwargs)
            )
        else:  # context_type and context_id should be "null" if global. Test this.
            return PaginatedList(
                OutcomeLink,
                self._requester,
                'GET',
                'global/outcome_groups/%s/outcomes' % (self.id),
                _kwargs=combine_kwargs(**kwargs)
            )

    def link_existing(self, outcome_id):
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
        if self.context_type is "Course":
            response = self._requester.request(
                'PUT',
                'courses/%s/outcome_groups/%s/outcomes/%s' % (
                    self.context_id,
                    self.id,
                    outcome_id
                )
            )
        elif self.context_type is "Account":
            response = self._requester.request(
                'PUT',
                'accounts/%s/outcome_groups/%s/outcomes/%s' % (
                    self.context_id,
                    self.id,
                    outcome_id
                )
            )
        else:  # context_type and context_id should be "null" if global. Test this.
            response = self._requester.request(
                'PUT',
                'global/outcome_groups/%s/outcomes/%s' % (
                    self.id,
                    outcome_id
                )
            )

        return OutcomeLink(self._requester, response.json())

    def link_new(self, **kwargs):
        """
        Create a new Outcome and link it to this OutcomeGroup

        :calls: `POST /api/v1/global/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link`_
            or `POST /api/v1/accounts/:account_id/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link`_
            or `POST /api/v1/courses/:course_id/outcome_groups/:id/outcomes \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.link`_

        :returns: OutcomeLink object with current OutcomeGroup and newly linked Outcome.
        :rtype: :class:`canvasapi.outcome.OutcomeLink`
        """
        if self.context_type is "Course":
            response = self._requester.request(
                'POST',
                'courses/%s/outcome_groups/%s/outcomes/%s' % (self.context_id, self.id),
                _kwargs=combine_kwargs(**kwargs)
            )
        elif self.context_type is "Account":
            response = self._requester.request(
                'POST',
                'accounts/%s/outcome_groups/%s/outcomes/%s' % (self.context_id, self.id),
                _kwargs=combine_kwargs(**kwargs)
            )
        else:  # context_type and context_id should be "null" if global. Test this.
            response = self._requester.request(
                'POST',
                'global/outcome_groups/%s/outcomes/%s' % (self.id),
                _kwargs=combine_kwargs(**kwargs)
            )

        return OutcomeLink(self._requester, response.json())

    def unlink_outcome(self, outcome_id):
        """
        Remove an Outcome from and OutcomeLink

        :calls: `DELETE /api/v1/global/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.unlink`_
            or `DELETE /api/v1/accounts/:account_id/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.unlink`_
            or `DELETE /api/v1/courses/:course_id/outcome_groups/:id/outcomes/:outcome_id \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.unlink`_

        :returns: OutcomeLink object with current OutcomeGroup and newly linked Outcome.
        :rtype: :class:`canvasapi.outcome.OutcomeLink`
        """
        if self.context_type is "Course":
            response = self._requester.request(
                'DELETE',
                'courses/%s/outcome_groups/%s/outcomes/%s' % (
                    self.context_id,
                    self.id,
                    outcome_id
                )
            )
        elif self.context_type is "Account":
            response = self._requester.request(
                'DELETE',
                'accounts/%s/outcome_groups/%s/outcomes/%s' % (
                    self.context_id,
                    self.id,
                    outcome_id
                )
            )
        else:  # context_type and context_id should be "null" if global. Test this.
            response = self._requester.request(
                'DELETE',
                'global/outcome_groups/%s/outcomes/%s' % (
                    self.id,
                    outcome_id
                )
            )

        return OutcomeLink(self._requester, response.json())

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
        if self.context_type is "Course":
            return PaginatedList(
                OutcomeGroup,
                self._requester,
                'GET',
                'courses/%s/outcome_groups/%s/subgroups' % (self.context_id, self.id)
            )
        elif self.context_type is "Account":
            return PaginatedList(
                OutcomeGroup,
                self._requester,
                'GET',
                'accounts/%s/outcome_groups/%s/subgroups' % (self.context_id, self.id)
            )
        else:  # context_type and context_id should be "null" if global. Test this.
            return PaginatedList(
                OutcomeGroup,
                self._requester,
                'GET',
                'global/outcome_groups/%s/subgroups' % (self.id)
            )

    def create_subgroup(self, **kwargs):
        """
        Create a subgroup of the current group

        :calls: `POST /api/v1/global/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.create>`_
            or `POST /api/v1/accounts/:account_id/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.create>`_
            or `POST /api/v1/courses/:course_id/outcome_groups/:id/subgroups \
            <https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.create>`_

        :returns: Itself as an OutcomeGroup object.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        if self.context_type is "Course":
            response = self._requester.request(
                'POST',
                'courses/%s/outcome_groups/%s/subgroups' % (self.context_id, self.id),
                _kwargs=combine_kwargs(**kwargs)
            )
        elif self.context_type is "Account":
            response = self._requester.request(
                'POST',
                'accounts/%s/outcome_groups/%s/subgroups' % (self.context_id, self.id),
                _kwargs=combine_kwargs(**kwargs)
            )
        else:  # context_type and context_id should be "null" if global. Test this.
            response = self._requester.request(
                'POST',
                'global/outcome_groups/%s/subgroups' % (self.id),
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

        :returns: Itself as an OutcomeGroup object.
        :rtype: :class:`canvasapi.outcome.OutcomeGroup`
        """
        if self.context_type is "Course":
            response = self._requester.request(
                'POST',
                'courses/%s/outcome_groups/%s/import' % (self.context_id, self.id),
                source_outcome_group_id
            )
        elif self.context_type is "Account":
            response = self._requester.request(
                'POST',
                'accounts/%s/outcome_groups/%s/import' % (self.context_id, self.id),
                source_outcome_group_id
            )
        else:  # context_type and context_id should be "null" if global. Test this.
            response = self._requester.request(
                'POST',
                'global/outcome_groups/%s/import' % (self.id),
                source_outcome_group_id
            )

        return OutcomeGroup(self._requester, response.json())
