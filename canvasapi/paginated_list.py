import re


class PaginatedList(object):
    """
    Abstracts `pagination of Canvas API \
    <https://canvas.instructure.com/doc/api/file.pagination.html>`_.
    """

    def __getitem__(self, index):
        assert isinstance(index, (int, slice))
        if isinstance(index, int):
            if index < 0:
                raise IndexError("Cannot negative index a PaginatedList")
            self._get_up_to_index(index)
            return self._elements[index]
        else:
            return self._Slice(self, index)

    def __init__(
        self,
        content_class,
        requester,
        request_method,
        first_url,
        extra_attribs=None,
        _root=None,
        **kwargs
    ):

        self._elements = list()

        self._requester = requester
        self._content_class = content_class
        self._first_url = first_url
        self._first_params = kwargs or {}
        self._first_params["per_page"] = kwargs.get("per_page", 100)
        self._next_url = first_url
        self._next_params = self._first_params
        self._extra_attribs = extra_attribs or {}
        self._request_method = request_method
        self._root = _root

    def __iter__(self):
        for element in self._elements:
            yield element
        while self._has_next():
            new_elements = self._grow()
            for element in new_elements:
                yield element

    def __repr__(self):
        return "<PaginatedList of type {}>".format(self._content_class.__name__)

    def _get_next_page(self):
        response = self._requester.request(
            self._request_method, self._next_url, **self._next_params
        )
        data = response.json()
        self._next_url = None

        next_link = response.links.get("next")
        regex = r"{}(.*)".format(re.escape(self._requester.base_url))

        self._next_url = (
            re.search(regex, next_link["url"]).group(1) if next_link else None
        )

        self._next_params = {}

        content = []

        if self._root:
            try:
                data = data[self._root]
            except KeyError:
                # TODO: Fix this message to make more sense to an end user.
                raise ValueError("Invalid root value specified.")

        for element in data:
            if element is not None:
                element.update(self._extra_attribs)
                content.append(self._content_class(self._requester, element))

        return content

    def _get_up_to_index(self, index):
        while len(self._elements) <= index and self._has_next():
            self._grow()

    def _grow(self):
        new_elements = self._get_next_page()
        self._elements += new_elements
        return new_elements

    def _has_next(self):
        return self._next_url is not None

    def _is_larger_than(self, index):
        return len(self._elements) > index or self._has_next()

    class _Slice(object):
        def __init__(self, the_list, the_slice):
            self._list = the_list
            self._start = the_slice.start or 0
            self._stop = the_slice.stop
            self._step = the_slice.step or 1

            if self._start < 0 or self._stop < 0:
                raise IndexError("Cannot negative index a PaginatedList slice")

        def __iter__(self):
            index = self._start
            while not self._finished(index):
                if self._list._is_larger_than(index):
                    try:
                        yield self._list[index]
                    except IndexError:
                        return
                    index += self._step
                else:
                    return

        def _finished(self, index):
            return self._stop is not None and index >= self._stop
