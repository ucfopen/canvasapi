"""A collection of useful methods."""


def combine_kwargs(**kwargs):
    """
    Combines a list of keyword arguments into a single dictionary.

    :rtype: dict
    """
    data = {}
    for key, value in kwargs.iteritems():
        if isinstance(value, dict):
            for subkey, subvalue in value.iteritems():
                data[key + '[' + subkey + ']'] = subvalue
            continue

        data[key] = value

    return data


def list_objs(obj_class, requester, data):
    """
    Converts a list of dictionaries into a list of objects

    :param obj_class: The class of object to create
    :type obj_class: class
    :param requester: Requester for object to use
    :type requester: Requester
    :param data: List of dictionaries - usually direct from Canvas
    :type data: list
    :rtype: list: list of objects of type `obj_class`
    """
    return [obj_class(requester, obj) for obj in data]
