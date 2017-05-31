from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class Login(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.id, self.unique_id)

    def delete(self):
        """
        Delete an existing login.

        :calls: `DELETE /api/v1/users/:user_id/logins/:id \
        <https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.destroy>`_

        :rtype: :class:`canvasapi.login.Login`
        """

        response = self._requester.request(
            'DELETE',
            'users/%s/logins/%s' % (self.id, self.unique_id)
        )
        return Login(self._requester, response.json())

    def edit(self, **kwargs):
        """
        Update an existing login for a user in the given account.

        :calls: `PUT /api/v1/accounts/:account_id/logins/:id \
        <https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.update>`_

        :rtype: :class:`canvasapi.login.Login`
        """
        response = self._requester.request(
            'PUT',
            'accounts/%s/logins/%s' % (self.id, self.unique_id),
            **combine_kwargs(**kwargs)
        )

        return Login(self._requester, response.json())
