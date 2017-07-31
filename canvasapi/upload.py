from __future__ import absolute_import, division, print_function, unicode_literals
import os

from six import string_types

from canvasapi.util import combine_kwargs


class Uploader(object):
    """
    Upload a file to Canvas.
    """

    def __init__(self, requester, url, file, **kwargs):
        """
        :param requester: The :class:`canvasapi.requester.Requester` to pass requests through.
        :type requester: :class:`canvasapi.requester.Requester`
        :param url: The URL to upload the file to.
        :type url: str
        :param file: A file handler or path of the file to upload.
        :type file: file or str
        """
        if isinstance(file, string_types):
            if not os.path.exists(file):
                raise IOError('File ' + file + ' does not exist.')
            self._using_filename = True
        else:
            self._using_filename = False

        self._requester = requester
        self.url = url
        self.file = file
        self.kwargs = kwargs

    def start(self):
        """
        Kick off uploading process. Handles open/closing file if a path
        is passed.

        :calls: request_upload_token
        :returns: True if the file uploaded successfully, False \
            otherwise, and the JSON response from the API.
        :rtype: tuple
        """
        if self._using_filename:
            with open(self.file, 'rb') as file:
                return self.request_upload_token(file)
        else:
            return self.request_upload_token(self.file)

    def request_upload_token(self, file):
        """
        Request an upload token.

        :param file: A file handler pointing to the file to upload.
        :returns: True if the file uploaded successfully, False otherwise, \
            and the JSON response from the API.
        :rtype: tuple
        """
        self.kwargs['name'] = os.path.basename(file.name)
        self.kwargs['size'] = os.fstat(file.fileno()).st_size

        response = self._requester.request(
            'POST',
            self.url,
            **combine_kwargs(**self.kwargs)
        )

        return self.upload(response, file)

    def upload(self, response, file):
        """
        Upload the file.

        :param response: The response from the upload request.
        :type response: dict
        :param file: A file handler pointing to the file to upload.
        :returns: True if the file uploaded successfully, False otherwise, \
            and the JSON response from the API.
        :rtype: tuple
        """
        response = response.json()
        if not response.get('upload_url'):
            raise ValueError('Bad API response. No upload_url.')

        if not response.get('upload_params'):
            raise ValueError('Bad API response. No upload_params.')

        kwargs = response.get('upload_params')
        kwargs['file'] = file

        response_json = self._requester.request(
            'POST',
            use_auth=False,
            _url=response.get('upload_url'),
            **kwargs
        ).json()

        if 'url' in response_json:
            return (True, response_json)

        return (False, response_json)
