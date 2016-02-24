"""
A collection of PyCanvas exception classes.
"""


class CanvasException(Exception):
    """
    Base class for all errors returned by the Canvas API.
    """
    def __init__(self, message):
        if isinstance(message, dict):
            self.error_report_id = message.get('error_report_id', None)

            errors = message.get('errors', False)
            if errors:
                self.message = ''.join(error['message'] for error in errors)
            else:
                self.message = 'Something went wrong.'
        else:
            self.message = message


class InvalidAccessToken(CanvasException):
    """PyCanvas was unable to make an API connection."""
    pass


class PermissionError(CanvasException):
    """PyCanvas's key is valid, but is unauthorized to access the requested resource."""
    pass


class ResourceDoesNotExist(CanvasException):
    """Canvas could not locate the requested resource."""
    pass
