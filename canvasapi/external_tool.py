from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import CanvasException
from canvasapi.util import combine_kwargs


class ExternalTool(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    @property
    def parent_id(self):
        """
        Return the id of the course or account that spawned this tool.

        :rtype: int
        """
        if hasattr(self, "course_id"):
            return self.course_id
        elif hasattr(self, "account_id"):
            return self.account_id
        else:
            raise ValueError("ExternalTool does not have a course_id or account_id")

    @property
    def parent_type(self):
        """
        Return whether the tool was spawned from a course or account.

        :rtype: str
        """
        if hasattr(self, "course_id"):
            return "course"
        elif hasattr(self, "account_id"):
            return "account"
        else:
            raise ValueError("ExternalTool does not have a course_id or account_id")

    def get_parent(self):
        """
        Return the object that spawned this tool.

        :rtype: :class:`canvasapi.account.Account` or :class:`canvasapi.account.Course`
        """
        from canvasapi.account import Account
        from canvasapi.course import Course

        response = self._requester.request(
            "GET", "{}s/{}".format(self.parent_type, self.parent_id)
        )

        if self.parent_type == "account":
            return Account(self._requester, response.json())
        elif self.parent_type == "course":
            return Course(self._requester, response.json())

    def delete(self):
        """
        Remove the specified external tool.

        :calls: `DELETE /api/v1/courses/:course_id/external_tools/:external_tool_id
            <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.destroy>`_
            or `DELETE /api/v1/accounts/:account_id/external_tools/:external_tool_id
            <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.destroy>`_

        :rtype: :class:`canvasapi.external_tool.ExternalTool`
        """
        response = self._requester.request(
            "DELETE",
            "{}s/{}/external_tools/{}".format(
                self.parent_type, self.parent_id, self.id
            ),
        )

        return ExternalTool(self._requester, response.json())

    def edit(self, **kwargs):
        """
        Update the specified external tool.

        :calls: `PUT /api/v1/courses/:course_id/external_tools/:external_tool_id
            <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.update>`_
            or `PUT /api/v1/accounts/:account_id/external_tools/:external_tool_id
            <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.update>`_

        :rtype: :class:`canvasapi.external_tool.ExternalTool`
        """
        response = self._requester.request(
            "PUT",
            "{}s/{}/external_tools/{}".format(
                self.parent_type, self.parent_id, self.id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()

        if "name" in response_json:
            super(ExternalTool, self).set_attributes(response_json)

        return ExternalTool(self._requester, response_json)

    def get_sessionless_launch_url(self, **kwargs):
        """
        Return a sessionless launch url for an external tool.

        :calls: `GET /api/v1/courses/:course_id/external_tools/sessionless_launch
            <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch>`_
            or `GET /api/v1/accounts/:account_id/external_tools/sessionless_launch \
            <https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch>`_

        :rtype: str
        """
        kwargs["id"] = self.id
        response = self._requester.request(
            "GET",
            "{}s/{}/external_tools/sessionless_launch".format(
                self.parent_type, self.parent_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        try:
            return response.json()["url"]
        except KeyError:
            raise CanvasException("Canvas did not respond with a valid URL")
