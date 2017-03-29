import re


class PaginatedList(object):
    """
    Abstracts `pagination of Canvas API \
    <https://canvas.instructure.com/doc/api/file.pagination.html>`_.
    """

    def __init__(
        self, content_class, requester, request_method, first_url, extra_attribs=None,
            **kwargs):

        self.__elements = list()

        self.__requester = requester
        self.__content_class = content_class
        self.__first_url = first_url
        self.__first_params = kwargs or {}
        self.__first_params['per_page'] = kwargs.get('per_page', 100)
        self.__next_url = first_url
        self.__next_params = self.__first_params
        self.__extra_attribs = extra_attribs or {}
        self.__request_method = request_method

    def __getitem__(self, index):
        assert isinstance(index, (int, slice))
        if isinstance(index, (int, long)):
            self.__get_up_to_index(index)
            return self.__elements[index]
        else:
            return self._Slice(self, index)

    def __iter__(self):
        for element in self.__elements:
            yield element
        while self._has_next():
            new_elements = self._grow()
            for element in new_elements:
                yield element

    def __repr__(self):
        return "<PaginatedList of type %s>" % (self.__content_class.__name__)

    def _is_larger_than(self, index):
        return len(self.__elements) > index or self._has_next()

    def __get_up_to_index(self, index):
        while len(self.__elements) <= index and self._has_next():
            self._grow()

    def _grow(self):
        new_elements = self._get_next_page()
        self.__elements += new_elements
        return new_elements

    def _has_next(self):
        return self.__next_url is not None

    def _get_next_page(self):
        response = self.__requester.request(
            self.__request_method,
            self.__next_url,
            **self.__next_params
        )
        data = response.json()
        self.__next_url = None

        next_link = response.links.get('next')
        regex = r'%s(.*)' % (re.escape(self.__requester.base_url))

        self.__next_url = re.search(regex, next_link['url']).group(1) if next_link else None

        self.__next_params = {}

        content = []
        for element in data:
            if element is not None:
                element.update(self.__extra_attribs)
                content.append(self.__content_class(self.__requester, element))

        return content

    class _Slice:
        def __init__(self, the_list, the_slice):
            self.__list = the_list
            self.__start = the_slice.start or 0
            self.__stop = the_slice.stop
            self.__step = the_slice.step or 1

        def __iter__(self):
            index = self.__start
            while not self.__finished(index):
                if self.__list._is_larger_than(index):
                    yield self.__list[index]
                    index += self.__step

        def __finished(self, index):
            return self.__stop is not None and index >= self.__stop
