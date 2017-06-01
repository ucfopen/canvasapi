from canvasapi.canvas_object import CanvasObject


class ExternalFeed(CanvasObject):

    def __str__(self):
        return str(self.display_name)
