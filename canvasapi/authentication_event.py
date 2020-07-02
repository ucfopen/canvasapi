from canvasapi.canvas_object import CanvasObject


class AuthenticationEvent(CanvasObject):
    def __str__(self):
        return "{} {} ({})".format(self.created_at, self.event_type, self.pseudonym_id)
