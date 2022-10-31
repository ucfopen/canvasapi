from canvasapi import CanvasObject

class JWT(CanvasObject):
    def __str__(self):
        return self.token
