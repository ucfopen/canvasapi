from canvasapi.canvas_object import CanvasObject


class Todo(CanvasObject):
    def __str__(self):
        return "Todo List ({})".format(self.id)
