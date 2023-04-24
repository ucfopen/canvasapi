import inspect
import os
import sys

sys.path.append(os.path.join(sys.path[0], ".."))

import canvasapi  # noqa

exempt_files = ("__init__",)


def find_missing_modules():
    # get all modules visile to inspect from `canvasapi.__init__`
    module_names = [
        module_name
        for module_name, module in inspect.getmembers(canvasapi, inspect.ismodule)
    ]

    # get all .py files in canvasapi dir (without .py extension)
    path = "canvasapi"
    filenames = [fname[:-3] for fname in os.listdir(path) if fname.endswith(".py")]

    missing_modules = list()

    for filename in filenames:
        # ignore exempt files
        if filename in exempt_files:
            continue

        # check for missing files against module names
        if filename not in module_names:
            missing_modules.append(filename)

    return missing_modules


if __name__ == "__main__":
    missing_modules = find_missing_modules()
    num_missing = len(missing_modules)
    missing_module_str = ", ".join(missing_modules)

    if missing_modules:
        print(f"Missing {num_missing} modules from inspect. 💥")
        for module in missing_modules:
            print(f"  - {module}")
        print("Ensure the above modules are imported (even indirectly) to __init__")
    else:
        print("All modules accounted for! 👍")
    sys.exit(num_missing > 0)
