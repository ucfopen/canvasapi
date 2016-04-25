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
    except:
        for obj_type in object_types:
            if isinstance(parameter, obj_type):
                try:
                    return int(parameter.id)
                except:
                    break

        obj_type_list = ",".join([obj_type.__name__ for obj_type in object_types])
        message = 'Parameter %s must be of type %s or int.' % (param_name, obj_type_list)
        raise TypeError(message)
