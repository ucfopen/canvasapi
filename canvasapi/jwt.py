from canvasapi.canvas_object import CanvasObject


class JWT(CanvasObject):
    def __str__(self):
        return self.token
