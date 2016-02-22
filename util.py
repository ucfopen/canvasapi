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