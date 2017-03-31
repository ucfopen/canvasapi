class CanvasException(Exception):  # pragma: no cover
    """
    Base class for all errors returned by the Canvas API.
    """
    def __init__(self, message):
        if isinstance(message, dict):
            self.error_report_id = message.get('error_report_id', None)

            errors = message.get('errors', False)
            if errors:
                self.message = str(errors)
            else:
                self.message = ('Something went wrong. ', message)
        else:
            self.message = message

    def __str__(self):
        return self.message


class BadRequest(CanvasException):
    """Canvas was unable to understand the request. More information may be needed."""
    pass


class InvalidAccessToken(CanvasException):
    """canvasapi was unable to make an API connection."""
    pass


class Unauthorized(CanvasException):
    """canvasapi's key is valid, but is unauthorized to access the requested resource."""
    pass


class ResourceDoesNotExist(CanvasException):
    """Canvas could not locate the requested resource."""
    pass


class RequiredFieldMissing(CanvasException):
    """A required field is missing."""
    pass
