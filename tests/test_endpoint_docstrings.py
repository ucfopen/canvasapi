import inspect
import re
def test_methods(*testMethods):
    failures = 0
    for testMethod in testMethods:
        # Check if docstring contains a calls line
        if re.search(":calls:", inspect.getdoc(testMethod)):
            callLine = re.search(":calls:[^_]*_", inspect.getdoc(testMethod)).group()
            callGroups = re.search("(POST |GET |PUT |PATCH |DELETE )[^/]*(/[^ ]*)[^<]*<([^>]*)>",callLine).groups()
            if checkUsage(callGroups) or checkAPIDoc(callGroups)
                failures += 1

    #TODO change to error codes based on results
    return False

#TODO implement
def checkAPIDoc(groups):
    verb, apiURL, docURL = groups
    return False

#TODO implement
def checkUsage(groups):
    return False
