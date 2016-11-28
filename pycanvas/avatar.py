from pycanvas.canvas_object import CanvasObject


class Avatar(CanvasObject):

    def __str__(self):  # pragma: no cover
        return "type: %s, display_name: %s, url: %s" % (
            self.type,
            self.display_name,
            self.url,
        )
