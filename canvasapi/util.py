from __future__ import absolute_import, division, print_function, unicode_literals

from six import text_type


def combine_kwargs(**kwargs):
    combined_kwargs = []

    # Loop through all kwargs provided
    for kw, arg in kwargs.items():
        if isinstance(arg, (dict, list, tuple)):
            for k, v in arg.items():
                for x in recursive_function(k, v):
                    combined_kwargs.append(('{}{}'.format(kw, x[0]), x[1]))
            # do stuff with kw probably
            # loop over list and add to combined_kwargs
        else:
            combined_kwargs.append((text_type(kw), arg))

    return combined_kwargs


def recursive_function(key, obj):
    """
    :param obj: The object to translate into a kwarg

    :returns: A list of tuples that...
    :rtype: list
    """
    if isinstance(obj, dict):
        # Add the word (e.g. "[key]")
        new_list = []

        for k, v in obj.items():
            for x in recursive_function(k, v):
                new_list.append(('[{}]{}'.format(key, x[0]), x[1]))
        return new_list

    elif isinstance(obj, (list, tuple)):
        # Add empty brackets (i.e. "[]")
        new_list = []
        for i in obj:
            for x in recursive_function(key, i):
                new_list.append(('[]' + x[0], x[1]))
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
        message = 'Parameter %s must be of type %s or int.' % (param_name, obj_type_list)
        raise TypeError(message)
