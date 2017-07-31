from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


@python_2_unicode_compatible
class EnrollmentTerm(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def delete(self):
        """
        Delete this Enrollment Term.

        :calls: `DELETE /api/v1/accounts/:account_id/terms/:id \
        <https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms.destroy>`_

        :rtype: :class:`canvasapi.enrollment_term.EnrollmentTerm`
        """
        response = self._requester.request(
            'DELETE',
            'accounts/%s/terms/%s' % (self.account_id, self.id)
        )
        return EnrollmentTerm(self._requester, response.json())

    def edit(self, **kwargs):
        """
        Modify this Enrollment Term.

        :calls: `PUT /api/v1/accounts/:account_id/terms/:id \
        <https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms.update>`_

        :rtype: :class:`canvasapi.enrollment_term.EnrollmentTerm`
        """
        response = self._requester.request(
            'PUT',
            'accounts/%s/terms/%s' % (self.account_id, self.id),
            **combine_kwargs(**kwargs)
        )

        return EnrollmentTerm(self._requester, response.json())
