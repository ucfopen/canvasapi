from canvasapi.canvas_object import CanvasObject


class Tab(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.label, self.id)
