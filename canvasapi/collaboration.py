from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import RequiredFieldMissing
from canvasapi.util import combine_kwargs


@python_2_unicode_compatible
class Collaboration(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.document_id, self.id)
