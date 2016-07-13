from canvas_object import CanvasObject


class Conversation(CanvasObject):

    def __str__(self):
        return "%s %s" % (self.id, self.subject)
