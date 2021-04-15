import re

import pytz
from dateutil import parser

DATE_PATTERN = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")


class CanvasObject(object):
    """
    Base class for all classes representing objects returned by the API.

    This makes a call to :func:`canvasapi.canvas_object.CanvasObject.set_attributes`
    to dynamically construct this object's attributes with a JSON object.
    """

    def __getattribute__(self, name):
        return super(CanvasObject, self).__getattribute__(name)

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
        attrs = ", ".join(
            [
                "{}={}".format(attr, val)
                for attr, val in self.__dict__.items()
                if attr != "attributes"
            ]
        )  # noqa
        return "{}({})".format(classname, attrs)

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
        for attribute, value in attributes.items():
            self.__setattr__(attribute, value)

            # datetime field
            try:
                naive = parser.isoparse(str(value))
                # UTC or no timezone offset, so set accordingly
                if "Z" in str(value) or "T" not in str(value) or len(str(value)) <= 6:
                    aware = naive.replace(tzinfo=pytz.utc)

                # otherwise, localize and use astimezone to fix time to UTC
                # credit to https://bit.ly/3abuvOf
                else:
                    # get timezone offset
                    timezone_offset = str(value)[-6:]

                    # using https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
                    # to create string to localize the timezone
                    local_string = "Etc/GMT"

                    # flip for GMT+/-
                    if timezone_offset[0] == "+":
                        local_string += "-"
                    else:
                        local_string += "+"

                    # if the first character is 1, then we need both hour digits
                    if timezone_offset[1] == "1":
                        local_string = local_string + timezone_offset[1:3]
                    # otherwise, we only need the second hour digit
                    else:
                        local_string += timezone_offset[2]

                    local_time = pytz.timezone(local_string)
                    naive = naive.replace(tzinfo=None)
                    local_datetime = local_time.localize(naive)
                    aware = local_datetime.astimezone(pytz.utc)

                self.__setattr__(attribute + "_date", aware)

            except ValueError:
                pass
