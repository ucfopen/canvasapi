from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs, obj_or_id, obj_or_str


class PairingCode(CanvasObject):
    def __str__(self):
        return "{} - {}".format(self.user_id, self.code)
