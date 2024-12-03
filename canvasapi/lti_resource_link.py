from canvasapi.canvas_object import CanvasObject


class LTIResourceLink(CanvasObject):
    def __init__(self, requester, attributes):
        super(LTIResourceLink, self).__init__(requester, attributes)

    def __str__(self):
        return "{} ({})".format(self.url, self.title)
