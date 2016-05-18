from datetime import datetime

import string
import re

DATE_PATTERN = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z')
COURSE_PATTERN = re.compile('\/courses\/[0-9]+\/')


class CanvasObject(object):
    """
    Base class for all classes representing objects returned by the API.
    """

    def __init__(self, requester, attributes):
        """
        :param requester: Requester
        :param attributes: dict
        """
        self._requester = requester
        self.set_attributes(attributes)

    def __repr__(self):  # pragma: no cover
        classname = self.__class__.__name__
        attrs = ', '.join(['%s=%s' % (attr, val) for attr, val in self.__dict__.iteritems()])
        return '%s(%s)' % (classname, attrs)

    def set_attributes(self, attributes):
        """
        Load this object with attributes.

        :param attributes: dict
        """
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
