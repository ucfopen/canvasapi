from canvas_object import CanvasObject


class Assignment(CanvasObject):

    def __str__(self):
        return "id: %s, name: %s, description: %s" % (
            self.id,
            self.name,
            self.description
        )
