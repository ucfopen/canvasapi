from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.util import combine_kwargs


class AppointmentGroup(CanvasObject):

    def delete(self, **kwargs):
        """
        Delete this appointment group.

        :calls: `DELETE /api/v1/appointment_groups/:id \
        <https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.destroy>`_

        :rtype: :class:`canvasapi.appointment_group.AppointmentGroup`
        """
        response = self._requester.request(
            'DELETE',
            'appointment_groups/%s' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return AppointmentGroup(self._requester, response.json())

    def edit(self, appointment_group, **kwargs):
        """
        Modify this appointment group.

        :calls: `PUT /api/v1/appointment_groups/:id \
        <https://canvas.instructure.com/doc/api/appointment_groups.html#method.appointment_groups.update>`_

        :rtype: :class:`canvasapi.appointment_group.AppointmentGroup`
        """
        if isinstance(appointment_group, dict) and 'context_codes' in appointment_group:
            kwargs['appointment_group'] = appointment_group
        else:
            raise RequiredFieldMissing(
                "Dictionary with key 'context_codes' is required."
            )

        response = self._requester.request(
            'PUT',
            'appointment_groups/%s' % (self.id),
            **combine_kwargs(**kwargs)
        )

        if 'title' in response.json():
            super(AppointmentGroup, self).set_attributes(response.json())

        return AppointmentGroup(self._requester, response.json())

    def __str__(self):
        return "{} ({})".format(self.title, self.id)
