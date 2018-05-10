from __future__ import absolute_import, division, print_function, unicode_literals

from canvasapi.canvas_object import CanvasObject
from canvasapi.folder import Folder
from canvasapi.util import combine_kwargs, obj_or_id
from scripts.validate_docstrings import validate_method

import unittest

import requests_mock
# test_endpoint_docstrings
@requests_mock.Mocker()
class TestValidateDocstrings(unittest.TestCase):
    def test_validate_method_verd_mismatch(self, m):
        self.assertFalse(validate_method(ExampleMethods.verb_mismatch, True))

    def test_validate_method_invalid_verb(self, m):
        self.assertFalse(validate_method(ExampleMethods.invalid_verb, True))

    def test_validate_method_no_api_call(self, m):
        self.assertTrue(validate_method(ExampleMethods.no_api_call, True))

    def test_validate_method_good_docstring(self, m):
        self.assertTrue(validate_method(ExampleMethods.good_docstring, True))

    def test_validate_method_multiple_endpoints(self, m):
        self.assertTrue(validate_method(ExampleMethods.multiple_endpoints,
            True
        ))

    def test_validate_method_multiline_URL(self, m):
        self.assertTrue(validate_method(ExampleMethods.multiline_URL, True))

    def test_validate_method_multiline_URL(self, m):
        self.assertTrue(validate_method(ExampleMethods.non_api_call, True))


class ExampleMethods(CanvasObject):
    def verb_mismatch(self):
        """
        :calls: `PUT /api/v1/files/:id  \
        <https://canvas.instructure.com/doc/api/files.html#method.files.destroy>`_

        :rtype: :class:`canvasapi.file.File`
        """
        response = self._requester.request(
            'DELETE',
            'files/{}'.format(self.id)
        )
        return ExampleMethods(self._requester, response.json())

    def invalid_verb(self):
        """
        Delete this file.

        :calls: `BELETE /api/v1/files/:id  \
        <https://canvas.instructure.com/doc/api/files.html#method.files.destroy>`_

        :rtype: :class:`canvasapi.file.File`
        """
        response = self._requester.request(
            'DELETE',
            'files/{}'.format(self.id)
        )
        return ExampleMethods(self._requester, response.json())

    def no_api_call(self):
        """
        Empty docstring.
        """
        return False

    def good_docstring(self):
        """
        Delete this file.

        :calls: `DELETE /api/v1/files/:id  \
        <https://canvas.instructure.com/doc/api/files.html#method.files.destroy>`_

        :rtype: :class:`canvasapi.file.File`
        """
        response = self._requester.request(
            'DELETE',
            'files/{}'.format(self.id)
        )
        return ExampleMethods(self._requester, response.json())

    def multiple_endpoints(self, folder):
        """
        Return the details for a folder

        :calls: `GET /api/v1/folders/:id \
        <https://canvas.instructure.com/doc/api/files.html#method.folders.show>`_

        :param folder: The object or ID of the folder to retrieve.
        :type folder: :class:`canvasapi.folder.Folder` or int

        :rtype: :class:`canvasapi.folder.Folder`
        """
        folder_id = obj_or_id(folder, "folder", (Folder,))

        response = self.__requester.request(
            'GET',
            'folders/{}'.format(folder_id)
        )
        return Folder(self.__requester, response.json())


    def multiline_URL(self, **kwargs):
        """
        Fetch all preferences for the given communication channel.

        :calls: `GET
            /api/v1/users/:user_id/communication_channels/:communication_channel_id/ \
                notification_preferences \
        <https://canvas.instructure.com/doc/api/notification_preferences.html#method.notification_preferences.index>`_

        :rtype: `list`
        """
        response = self._requester.request(
            'GET',
            'users/{}/communication_channels/{}/notification_preferences'.format(
                self.user_id,
                self.id
            ),
            _kwargs=combine_kwargs(**kwargs)
        )

        return response.json()['notification_preferences']

    def non_api_call(self):
        """
        Kick off uploading process. Handles open/closing file if a path
        is passed.

        :calls: request_upload_token
        :returns: True if the file uploaded successfully, False \
            otherwise, and the JSON response from the API.
        :rtype: tuple
        """
        pass
