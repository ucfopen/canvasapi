from canvas_object import CanvasObject


class Role(CanvasObject):

    def __str__(self):
        return "id: %s" % (
            self.id
        )
