from __future__ import absolute_import, division, print_function, unicode_literals

import inspect
import operator
import os
import sys

sys.path.append(os.path.join(sys.path[0], ".."))

import canvasapi  # noqa


def main():
    error_count = 0

    for _, module in inspect.getmembers(canvasapi, inspect.ismodule):
        # print(module.__name__)
        for class_name, theclass in inspect.getmembers(module, inspect.isclass):
            # Only process classes in this module
            if inspect.getmodule(theclass).__name__ != module.__name__:
                continue

            functions = list()
            for func_name, func in inspect.getmembers(theclass, inspect.isfunction):
                # Only add function if it is part of this class.
                # Get function's class name from qualified name.
                if func.__qualname__.split(".")[0] == class_name:
                    functions.append((func_name, inspect.getsourcelines(func)[1]))

            error_count += check_alphabetical(
                functions, theclass.__module__, theclass.__name__
            )

    return error_count


def check_alphabetical(methods, module_name, class_name):
    """
    Verify that the methods are in alphabetical order

    :param methods: A list of tuples with the method name and line
        number of each method.
    :type methods: list
    :param module_name: The name of the module being checked
    :type module_name: str

    :returns: The number of mis-ordered methods found
    :rtype int:
    """
    prev_func = ""
    prev_line = 0
    error_count = 0

    methods = sorted(methods, key=operator.itemgetter(0))

    for func_name, line_no in methods:
        if line_no < prev_line:
            if error_count == 0:
                print("\n" + module_name + "." + class_name + "\n-----------")

            print(
                (
                    "{func_name} ({module_name}:{line_no}) came before "
                    "{prev_func} ({module_name}:{prev_line})"
                ).format(
                    func_name=func_name,
                    line_no=line_no,
                    prev_func=prev_func,
                    prev_line=prev_line,
                    module_name=module_name,
                )
            )
            error_count += 1

        prev_func = func_name
        prev_line = line_no

    return error_count


if __name__ == "__main__":
    error_count = main()
    if error_count:
        print(
            "\nFound {error_count} method(s) not in alphabetical order.".format(
                error_count=error_count
            )
        )
    else:
        print("All methods are alphabetical!")
    sys.exit(error_count > 0)
