from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class AuthenticationProviders(CanvasObject):

    def __str__(self):  # pragma: no cover
        return "{} ({})".format(self.auth_type, self.position)

    def update(self, **kwargs):
        """
        Update an authentication provider using the same options as the create endpoint

        :calls: `PUT /api/v1/accounts/:account_id/authentication_providers/:id \
        <https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.update>`_

        :rtype: :class:`canvasapi.authentication_providers.AuthenticationProviders`
        """
        response = self._requester.request(
            'PUT',
            'accounts/%s/authentication_providers/%s' % (self.account_id, self.id),
            **combine_kwargs(**kwargs)
        )

        return AuthenticationProviders(self._requester, response.json())

    def delete(self):
        """
        Delete the config

        :calls: `DELETE /api/v1/accounts/:account_id/authentication_providers/:id \
        <https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.destroy>`_

        :rtype: :class:`canvasapi.authentication_providers.AuthenticationProviders`
        """
        response = self._requester.request(
            'DELETE',
            'accounts/%s/authentication_providers/%s' % (self.account_id, self.id)
        )
        return AuthenticationProviders(self._requester, response.json())
