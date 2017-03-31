from datetime import datetime
import json
import re

DATE_PATTERN = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z')


class CanvasObject(object):
    """
    Base class for all classes representing objects returned by the API.

    This makes a call to :func:`canvasapi.canvas_object.CanvasObject.set_attributes`
    to dynamically construct this object's attributes with a JSON object.
    """

    def __init__(self, requester, attributes):
        """
        :param requester: The requester to pass HTTP requests through.
        :type requester: :class:`canvasapi.requester.Requester`
        :param attributes: The JSON object to build this object with.
        :type attributes: dict
        """
        self._requester = requester
        self.set_attributes(attributes)

    def __repr__(self):  # pragma: no cover
        classname = self.__class__.__name__
        attrs = ', '.join(['%s=%s' % (attr, val) for attr, val in self.__dict__.iteritems() if attr != 'attributes'])  # noqa
        return '%s(%s)' % (classname, attrs)

    def to_json(self):
        """
        Return the original JSON response from the API that was used to
        construct the object.
        """
        return json.dumps(self.attributes)

    def set_attributes(self, attributes):
        """
        Load this object with attributes.

        This method attempts to detect special types based on the field's content
        and will create an additional attribute of that type.

        Consider a JSON response with the following fields::

            {
                "name": "New course name",
                "course_code": "COURSE-001",
                "start_at": "2012-05-05T00:00:00Z",
                "end_at": "2012-08-05T23:59:59Z",
                "sis_course_id": "12345"
            }

        The `start_at` and `end_at` fields match a date in ISO8601 format,
        so two additional datetime attributes are created, `start_at_date`
        and `end_at_date`.

        :param attributes: The JSON object to build this object with.
        :type attributes: dict
        """
        self.attributes = attributes

        for attribute, value in attributes.iteritems():
            self.__setattr__(attribute, value)

            try:
                # datetime field
                if DATE_PATTERN.match(str(value)):
                    date = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
                    self.__setattr__(attribute + '_date', date)
            # Non-unicode character. We can skip over this attribute.
            except UnicodeEncodeError:
                continue
