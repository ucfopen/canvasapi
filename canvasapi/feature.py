from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject


@python_2_unicode_compatible
class Feature(CanvasObject):
    def __str__(self):
        return "{} {}".format(self.display_name, self.applies_to)


@python_2_unicode_compatible
class FeatureFlag(CanvasObject):
    def __str__(self):
        return "{} {} {} {}".format(
            self.context_type, self.context_id, self.feature, self.state
        )
