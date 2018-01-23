from __future__ import absolute_import, division, print_function, unicode_literals

from collections import Iterable
from six import binary_type, string_types, text_type


def is_multivalued(value):
    """
    Determine whether the given value should be treated as a sequence
    of multiple values when used as a request parameter.

    In general anything that is iterable is multivalued.  For example,
    `list` and `tuple` instances are multivalued.  Generators are
    multivalued, as are the iterable objects returned by `zip`,
    `itertools.chain`, etc.  However, a simple `int` is single-valued.
    `str` and `bytes` are special cases: although these are iterable,
    we treat each as a single value rather than as a sequence of
    isolated characters or bytes.
    """

    # special cases: iterable, but not multivalued
    if isinstance(value, (string_types, binary_type)):
        return False

    # general rule: multivalued if iterable
    return isinstance(value, Iterable)


def combine_kwargs(**kwargs):
    """
    Flatten a series of keyword arguments from complex combinations of
    dictionaries and lists into a list of tuples representing
    properly-formatted parameters to pass to the Requester object.

    :param kwargs: A dictionary containing keyword arguments to be
        flattened into properly-formatted parameters.
    :type kwargs: dict

    :returns: A list of tuples that represent flattened kwargs. The
        first element is a string representing the key. The second
        element is the value.
    :rtype: `list` of `tuple`
    """
    combined_kwargs = []

    # Loop through all kwargs provided
    for kw, arg in kwargs.items():
        if isinstance(arg, dict):
            for k, v in arg.items():
                for tup in flatten_kwarg(k, v):
                    combined_kwargs.append(('{}{}'.format(kw, tup[0]), tup[1]))
        elif is_multivalued(arg):
            for i in arg:
                for tup in flatten_kwarg('', i):
                    combined_kwargs.append(('{}{}'.format(kw, tup[0]), tup[1]))
        else:
            combined_kwargs.append((text_type(kw), arg))

    return combined_kwargs


def flatten_kwarg(key, obj):
    """
    Recursive call to flatten sections of a kwarg to be combined

    :param key: The partial keyword to add to the full keyword
    :type key: str
    :param obj: The object to translate into a kwarg. If the type is
        `dict`, the key parameter will be added to the keyword between
        square brackets and recursively call this function. If the type
        is `list`, or `tuple`, a set of empty brackets will be appended
        to the keyword and recursively call this function. Otherwise,
        the function returns with the final keyword and value.

    :returns: A list of tuples that represent flattened kwargs. The
        first element is a string representing the key. The second
        element is the value.
    :rtype: `list` of `tuple`
    """
    if isinstance(obj, dict):
        # Add the word (e.g. "[key]")
        new_list = []
        for k, v in obj.items():
            for tup in flatten_kwarg(k, v):
                new_list.append(('[{}]{}'.format(key, tup[0]), tup[1]))
        return new_list

    elif is_multivalued(obj):
        # Add empty brackets (i.e. "[]")
        new_list = []
        for i in obj:
            for tup in flatten_kwarg(key, i):
                new_list.append((tup[0] + '[]', tup[1]))
        return new_list
    else:
        # Base case. Return list with tuple containing the value
        return [('[{}]'.format(text_type(key)), obj)]


def obj_or_id(parameter, param_name, object_types):
    """
    Accepts either an int (or long or str representation of an integer)
    or an object. If it is an int, return it. If it is an object and
    the object is of correct type, return the object's id. Otherwise,
    throw an exception.

    :param parameter: int, str, long, or object
    :param param_name: str
    :param object_types: tuple
    :rtype: int
    """
    try:
        return int(parameter)
    except (ValueError, TypeError):
        for obj_type in object_types:
            if isinstance(parameter, obj_type):
                try:
                    return int(parameter.id)
                except Exception:
                    break

        obj_type_list = ",".join([obj_type.__name__ for obj_type in object_types])
        message = 'Parameter {} must be of type {} or int.'.format(param_name, obj_type_list)
        raise TypeError(message)


def get_institution_url(base_url):
    """
    Clean up a given base URL.

    :param base_url: The base URL of the API.
    :type base_url: str
    :rtype: str
    """
    base_url = base_url.rstrip('/')
    index = base_url.find('/api/v1')

    if index != -1:
        return base_url[0:index]

    return base_url
