from canvasapi.canvas_object import CanvasObject


class AccountCalendar(CanvasObject):
    def __str__(self):
        return "{} {} ({})".format(self.name, self.visible, self.calendar_event_url)
