from canvasapi.canvas_object import CanvasObject


class UsageRights(CanvasObject):
    def __str__(self):
        return "{} {}".format(self.use_justification, self.license)
