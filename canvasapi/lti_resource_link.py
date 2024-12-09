from canvasapi.canvas_object import CanvasObject


class LTIResourceLink(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.url, self.title)
