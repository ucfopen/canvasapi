import os

from util import combine_kwargs


def uploader(requester, url, path=None, file=None, **kwargs):
    """
    Upload a file to a course.

    :param url: The url of the endpoint to upload to.
    :type url: str
    :param path: The path of the file to upload.
    :type path: str
    :param file: The file to upload.
    :type file: file
    :rtype: bool
    """
    if not path and not file:
        raise ValueError('Must provide a path or a file pointer.')

    if path:
        if not os.path.exists(path):
            raise IOError('File ' + path + ' does not exist.')
        file = open(path, 'rb')

    kwargs['name'] = os.path.basename(file.name)
    kwargs['size'] = os.fstat(file.fileno()).st_size

    response = requester.request(
        'POST',
        url,
        **combine_kwargs(**kwargs)
    )

    response = response.json()

    upload_url = response.get('upload_url')

    if not upload_url:
        raise Exception('Malformed response. Either you or Canvas made a mistake.')

    upload_params = response.get('upload_params')

    if not upload_params:
        raise Exception('Failed to collect upload_params?')

    kwargs = upload_params
    # Add our file to the kwargs
    kwargs['file'] = file

    response = requester.request(
        'POST',
        use_auth=False,
        url=upload_url,
        **kwargs
    )
    return response.json()
