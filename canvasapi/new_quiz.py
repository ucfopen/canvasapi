from canvasapi.canvas_object import CanvasObject


class NewQuiz(CanvasObject):
    def __str__(self):
        return "{} ({})".format(self.title, self.id)
