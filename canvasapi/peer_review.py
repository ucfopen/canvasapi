from canvasapi.canvas_object import CanvasObject


class PeerReview(CanvasObject):
    def __str__(self):
        return "{} {} ({})".format(self.asset_id, self.user_id, self.id)
