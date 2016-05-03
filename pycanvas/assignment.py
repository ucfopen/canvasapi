from canvas_object import CanvasObject


class Assignment(CanvasObject):

    def __str__(self):  # pragma: no cover
        return "id: %s, name: %s, description: %s" % (
            self.id,
            self.name,
            self.description
        )
