from canvas_object import CanvasObject
from util import combine_kwargs
from paginated_list import PaginatedList
# from exceptions import RequiredFieldMissing


class ExternalTool(CanvasObject):

    def __str__(self):
        return "%s %s %s" % (self.id, self.name, self.description)
