import canvasapi
import inspect
import re
import requests


def test_method(testMethod, quiet=False):
    # No docstring means no erroneous docstrings
    if not inspect.getdoc(testMethod):
        return True

    # Docstrings without API calls can't be checked this way
    if not re.search(":calls:", inspect.getdoc(testMethod)):
        return True
    if not re.search("<\S*>", inspect.getdoc(testMethod)):
        return True

    method_string = inspect.getfile(testMethod) +" "+ testMethod.__name__
    callLines = re.findall("`(POST|GET|PUT|PATCH|DELETE)([^<]*)<([^>]*)>`_", inspect.getdoc(testMethod))
    if len(callLines) == 0:
        if not quiet:
            # Docstring exists, has a :calls: line, contains a URL, but could
            # not be parsed;
            print "%s Failed to parse :calls: line." % (method_string)
        return False
    for callLine in callLines:
        if not test_docString(method_string, callLine, quiet):
            return False
    return True

def test_docString(method_string, callLine, quiet):
    docStringVerb, apiURL, docURL = callLine
    apiURL = ''.join(apiURL.split())
    if apiURL[-1] == '/':
        apiURL = apiURL[0:-1]
    fileURL, endpointName = re.search("([^#]*)#(.*)",docURL).groups()
    docResponse = requests.get(fileURL)
    if docResponse.status_code != requests.codes.ok:
        if not quiet:
            print "%s Docstring URL request returned %d" % (method_string, docResponse.status_code)
        return False

    endpointHeading = re.search("name=[\'\"]%s[\'\"]" % endpointName, docResponse.text)
    if not endpointName:

        if not quiet:
            print "%s Docstring URL does not contain an endpoint name in link to API documentation" \
            % method_string
        return False
    if not endpointHeading:
        if not quiet:
            print "%s Docstring refers to %s in %s, not found" % (method_string, endpointName, fileURL)
        return False

    endpointRegex = re.compile('<h3 class=[\"\']endpoint[\"\']>[^<]*<\/h3>')
    endpointStart = endpointRegex.search(docResponse.text, endpointHeading.end()).start()
    endpointEndRegex = re.compile('<[^h\/]')
    endpointEnd = endpointEndRegex.search(docResponse.text, endpointStart)
    if not endpointEnd:
        endpointEndPos = len(docReseponse.text)
    else:
        endpointEndPos = endpointEnd.start()
    endpointElement = endpointRegex.search(docResponse.text, endpointStart, endpointEndPos)
    endpointElements= []
    while endpointElement:
        endpointElements.append(endpointElement.group())
        endpointElement = endpointRegex.search(docResponse.text, endpointElement.end(), endpointEndPos)
    if len(endpointElements) == 0:
        if not quiet:
            print "Found no endpoint after %s in %s" % (endpointName, fileURL)
        return False
    docLines = []
    for endpointElementStr in endpointElements:
        docMatch = re.search("(POST|GET|PUT|PATCH|DELETE) (.*)", endpointElementStr)
        docLines.append(docMatch.group())
        docVerb, docEndpointURL = docMatch.groups()
        if docVerb != docStringVerb:
            continue
        if docEndpointURL != apiURL:
            continue
        return True
    if not quiet:
        print "%s Docstring %s not found in %s (found %s)" \
            % (method_string, docStringVerb + " " + apiURL, fileURL, str(docLines))
    return False

def test_methods():
    methods = set()
    for _, module in inspect.getmembers(canvasapi, inspect.ismodule):
        for _, theclass in inspect.getmembers(module, inspect.isclass):
            for _, method in inspect.getmembers(theclass, inspect.ismethod):
                methods.add(method)
    for methodToTest in methods:
        test_method(methodToTest)
