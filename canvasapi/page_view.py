from canvasapi.canvas_object import CanvasObject


class PageView(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.context_type, self.id)
