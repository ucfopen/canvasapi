from canvasapi.canvas_object import CanvasObject


class Avatar(CanvasObject):
    def __str__(self):  # pragma: no cover
        return "{}".format(self.display_name)
