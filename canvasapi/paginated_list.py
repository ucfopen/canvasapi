from __future__ import annotations

import re
import typing as t
from itertools import islice

from requests.models import Response

if t.TYPE_CHECKING:
    from canvasapi.requester import Requester  # pragma: no cover

ContentClass = t.TypeVar("ContentClass")


class PaginatedList(t.Generic[ContentClass]):
    """
    Abstracts `pagination of Canvas API \
    <https://canvas.instructure.com/doc/api/file.pagination.html>`_.
    :param content_class: The expected type to return in the list.
    :type content_class: class
    :param requester: The requester to pass HTTP requests through.
    :type requester: :class:`canvasapi.requester.Requester`
    :param request_method: HTTP request method
    :type request_method: str
    :param first_url: Canvas endpoint for the initial request
    :type first_url: str
    :param extra_attribs: Extra data to include in the request
    :type extra_attribs: dict
    :param _root: Specify a nested property from Canvas to use for the resulting list.
    :type _root: str
    :param _url_override: "new_quizzes" or "graphql" for specific Canvas endpoints.
    Other URLs may be specified for third-party requests.
    :type _url_override: str
    :rtype: :class:`canvasapi.paginated_list.PaginatedList` of type content_class
    """

    @t.overload
    def __getitem__(self, index: int) -> ContentClass:  # pragma: no cover
        ...

    @t.overload
    def __getitem__(self, index: slice) -> t.List[ContentClass]:  # pragma: no cover
        ...

    def __getitem__(self, index: int | slice):
        assert isinstance(
            index, (int, slice)
        ), "`index` must be either an integer or a slice."
        if isinstance(index, int):
            if index < 0:
                return list(self)[index]
            return list(islice(self, index + 1))[index]
        # if no negatives, islice can be used
        if not any(
            v is not None and v < 0 for v in (index.start, index.stop, index.step)
        ):
            return list(islice(self, index.start, index.stop, index.step))
        return list(self)[index]

    def __init__(
        self,
        content_class: type[ContentClass],
        requester: "Requester",
        request_method: str,
        first_url: str,
        extra_attribs: t.Optional[t.Dict[str, t.Any]] = None,
        _root: t.Optional[str] = None,
        _url_override: t.Optional[str] = None,
        **kwargs: t.Any,
    ):

        self._elements: list[ContentClass] = []
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
        self._url_override = _url_override

    def __iter__(self) -> t.Generator[ContentClass, None, None]:
        if self._has_next_page():
            current_index = 0
            while self._has_next_page():
                self._elements.extend(self._get_next_page())
                for index, element in enumerate(self._elements):
                    if index == current_index:
                        yield element
                        current_index += 1
        else:
            yield from iter(self._elements)

    def __repr__(self):
        return f"<PaginatedList of type {self._content_class.__name__}>"

    def _get_next_page(self):
        data = self._request_next_page()
        if self._root is not None:
            try:
                data = data[self._root]
            except KeyError:
                raise ValueError(
                    "The specified _root value was not found in the response."
                )
        return [self._init_content_class(elem) for elem in data]

    def _has_next_page(self):
        """Check whether another page of results can be requested."""
        return self._next_url is not None

    def _init_content_class(self, attributes: t.Dict[str, t.Any]):
        """Instantiate a new content class."""
        return self._content_class(
            self._requester, {**attributes, **self._extra_attribs}
        )

    def _request_next_page(self):
        response: t.Any = self._requester.request(
            self._request_method,
            self._next_url,
            _url=self._url_override,
            **self._next_params,
        )
        self._next_params = {}
        # Check the response headers first. This is the normal Canvas convention
        # for pagination, but there are endpoints which return a `meta` property
        # for pagination instead.
        # See https://github.com/ucfopen/canvasapi/discussions/605
        if response.links:
            next_link = response.links.get("next")
        elif isinstance(response, Response) and "meta" in response.json():
            data = response.json()
            # requests parses headers into dicts, this returns the same
            # structure so the regex will still work.
            try:
                next_link = {
                    "url": data["meta"]["pagination"]["next"],
                    "rel": "next",
                }
            except KeyError:
                next_link = None
        else:
            next_link = None

        self._set_next_url(next_link)
        response_json: t.Any = response.json()
        return response_json

    def _set_next_url(self, next_link: t.Optional[t.Dict[str, str]]):
        """Set the next url to request, if on exists."""
        if next_link is None:
            self._next_url = None
            return

        regex = rf"{re.escape(self._requester.base_url)}(.*)"
        match = re.search(regex, next_link["url"])
        if match is not None:
            self._next_url = match.group(1)
