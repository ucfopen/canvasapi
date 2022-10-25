import inspect
import os
import sys

sys.path.append(os.path.join(sys.path[0], ".."))

import canvasapi  # noqa

# Qualfied names of functions that are exempt from requiring kwargs
WHITELIST = (
    "Canvas.get_current_user",
    "CanvasObject.set_attributes",
    "File.download",
    "File.get_contents",
    "Uploader.request_upload_token",
    "Uploader.start",
    "Uploader.upload",
    "OutcomeGroup.context_ref",
    "OutcomeLink.context_ref",
)


def find_missing_kwargs():
    missing_count = 0

    for _, module in inspect.getmembers(canvasapi, inspect.ismodule):
        for class_name, theclass in inspect.getmembers(module, inspect.isclass):
            # Only process classes in this module
            if inspect.getmodule(theclass).__name__ != module.__name__:
                continue

            for func_name, func in inspect.getmembers(theclass, inspect.isfunction):
                # Only process function if it is part of this class.
                # Get function's class name from qualified name.
                if func.__qualname__.split(".")[0] == class_name:
                    # ignore "private" and dunder methods
                    if func_name.startswith("_"):
                        continue

                    # ignore functions in whitelist
                    if func.__qualname__ in WHITELIST:
                        continue

                    if not accepts_kwargs(func):
                        print(f"{func.__qualname__} is missing **kwargs")
                        missing_count += 1

    return missing_count


def accepts_kwargs(function):
    """
    Determine whether or not the provided function accepts arbritrary keyword arguments.

    :param function: The function to look for **kwargs in
    :type function: <class 'function'>

    :rtype: bool
    :returns: True if the function signature contains **kwargs. False otherwise.
    """
    return "**kwargs" in str(inspect.signature(function))


if __name__ == "__main__":
    missing_count = find_missing_kwargs()
    if missing_count:
        print(f"---\nFound {missing_count} functions missing **kwargs. 💥")
    else:
        print("All functions have **kwargs! 👍")
    sys.exit(missing_count > 0)
