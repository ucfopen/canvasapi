from canvasapi.canvas_object import CanvasObject
from canvasapi.paginated_list import PaginatedList
from canvasapi.util import combine_kwargs, obj_or_id
from canvasapi.course import Course
from canvasapi.exceptions import RequiredFieldMissing

class LTIResourceLink(CanvasObject):
    def __init__(self, requester, attributes):
        super(LTIResourceLink, self).__init__(requester, attributes)
    
    def __str__(self):
        return "{} ({})".format(self.url, self.title)