from __future__ import absolute_import, division, print_function, unicode_literals

from six import text_type


def combine_kwargs(**kwargs):
    """
    Combines a list of keyword arguments into a single dictionary.

    :rtype: dict
    """
    def flatten_dict(prefix, key, value):
        new_prefix = prefix + '[' + text_type(key) + ']'
        if isinstance(value, dict):
            d = {}
            for k, v in value.items():
                d.update(flatten_dict(new_prefix, k, v))
            return d
        else:
            return {new_prefix: value}

    combined_kwargs = {}

    # Loop through all kwargs.
    for kw, arg in kwargs.items():
        if isinstance(arg, dict):
            # If the argument is a dictionary, flatten it.
            for key, value in arg.items():
                combined_kwargs.update(flatten_dict(text_type(kw), key, value))
        else:
            combined_kwargs.update({text_type(kw): arg})
    return combined_kwargs


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
