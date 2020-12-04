from canvasapi.canvas_object import CanvasObject


class PairingCode(CanvasObject):
    def __str__(self):
        return "{} - {}".format(self.user_id, self.code)
