class CanvasException(Exception):  # pragma: no cover
    """
    Base class for all errors returned by the Canvas API.
    """

    def __init__(self, message):
        if isinstance(message, dict):
            self.error_report_id = message.get("error_report_id", None)

            errors = message.get("errors", False)
            if errors:
                self.message = errors
            else:
                self.message = ("Something went wrong. ", message)
        else:
            self.message = message

    def __str__(self):
        return str(self.message)


class BadRequest(CanvasException):
    """Canvas was unable to understand the request. More information may be needed."""

    pass


class InvalidAccessToken(CanvasException):
    """CanvasAPI was unable to make an API connection."""

    pass


class Unauthorized(CanvasException):
    """CanvasAPI's key is valid, but is unauthorized to access the requested resource."""

    pass


class ResourceDoesNotExist(CanvasException):
    """Canvas could not locate the requested resource."""

    pass


class RequiredFieldMissing(CanvasException):
    """A required field is missing."""

    pass


class Forbidden(CanvasException):
    """Canvas has denied access to the resource for this user."""

    pass


class RateLimitExceeded(Forbidden):
    """
    Canvas has recieved to many requests from this access token and is
    throttling this request. Try again later.
    """

    pass


class Conflict(CanvasException):
    """Canvas had a conflict with an existing resource."""

    pass


class UnprocessableEntity(CanvasException):
    """Canvas was unable to process the entity."""

    pass
