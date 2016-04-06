from canvas_object import CanvasObject

class Quiz(CanvasObject):


    def __str__(self):
        return "id %s, title: %s" % (
            self.id,
            self.title
        )


