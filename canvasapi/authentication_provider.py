from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


class AuthenticationProvider(CanvasObject):
    def __str__(self):  # pragma: no cover
        return "{} ({})".format(self.auth_type, self.position)

    def update(self, **kwargs):
        """
        Update an authentication provider using the same options as the create endpoint

        :calls: `PUT /api/v1/accounts/:account_id/authentication_providers/:id \
        <https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.update>`_

        :rtype: :class:`canvasapi.authentication_provider.AuthenticationProvider`
        """
        response = self._requester.request(
            "PUT",
            "accounts/{}/authentication_providers/{}".format(self.account_id, self.id),
            _kwargs=combine_kwargs(**kwargs),
        )

        if response.json().get("auth_type"):
            super(AuthenticationProvider, self).set_attributes(response.json())

        return response.json().get("auth_type")

    def delete(self):
        """
        Delete the config

        :calls: `DELETE /api/v1/accounts/:account_id/authentication_providers/:id \
        <https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.destroy>`_

        :rtype: :class:`canvasapi.authentication_provider.AuthenticationProvider`
        """
        response = self._requester.request(
            "DELETE",
            "accounts/{}/authentication_providers/{}".format(self.account_id, self.id),
        )
        return AuthenticationProvider(self._requester, response.json())
