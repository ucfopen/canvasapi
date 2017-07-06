from __future__ import unicode_literals
import os

from builtins import object, str

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
        :param file: The file or path of the file to upload.
        :type file: file or str
        """
        if isinstance(file, str):
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
        Request an upload token.
        """
        # open file if using filename
        file = open(self.file, 'rb') if self._using_filename else self.file

        self.kwargs['name'] = os.path.basename(file.name)
        self.kwargs['size'] = os.fstat(file.fileno()).st_size

        response = self._requester.request(
            'POST',
            self.url,
            **combine_kwargs(**self.kwargs)
        )

        # close file if using filename
        if self._using_filename:
            file.close()

        return self.upload(response)

    def upload(self, response):
        """
        Upload the file.

        :param response: The response from the upload request.
        :type response: dict
        :returns: True if the file uploaded successfully, False otherwise, \
                    and the JSON response from the API.
        :rtype: tuple
        """
        response = response.json()
        if not response.get('upload_url'):
            raise ValueError('Bad API response. No upload_url.')

        if not response.get('upload_params'):
            raise ValueError('Bad API response. No upload_params.')

        # open file if using filename
        file = open(self.file, 'rb') if self._using_filename else self.file

        kwargs = response.get('upload_params')
        kwargs['file'] = file

        response_json = self._requester.request(
            'POST',
            use_auth=False,
            _url=response.get('upload_url'),
            **kwargs
        ).json()

        # close file if using filename
        if self._using_filename:
            file.close()

        if 'url' in response_json:
            return (True, response_json)

        return (False, response_json)
