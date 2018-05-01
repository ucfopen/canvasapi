import inspect
import re
import requests
import os
import sys

def test_method(testMethod, quiet=False):
    # Check if docstring contains a calls line; automatic pass if not
    if not inspect.getdoc(testMethod):
        return True
    if re.search(":calls:", inspect.getdoc(testMethod)):
        callGroups = re.search("`(POST|GET|PUT|PATCH|DELETE) ([\S<]*)[\S\s]*<([^>`]*)>?`_",inspect.getdoc(testMethod))
        if not callGroups:
            print "%s Syntax error in :calls: line: %s" % (inspect.getfile(testMethod) +" "+ testMethod.__name__, callLine)
            return False
        docStringVerb, apiURL, docURL = callGroups.groups()
        fileURL, endpointName = re.search("([^#]*)#(.*)",docURL).groups()
        docResponse = requests.get(fileURL)
        if docResponse.status_code != requests.codes.ok:
            if not quiet:
                print "%s Docstring URL request returned %d" % (inspect.getfile(testMethod) +" "+ testMethod.__name__, docResponse.status_code)
            return False

        endpointHeading = re.search("name=[\'\"]%s[\'\"]" % endpointName, docResponse.text)
        if not endpointName:

            if not quiet:
                print "%s Docstring URL does not contain an endpoint name in link to API documentation" \
                % inspect.getfile(testMethod) +" "+ testMethod.__name__
            return False
        if not endpointHeading:
            if not quiet:
                print "%s Docstring refers to %s in %s, not found" % (inspect.getfile(testMethod) +" "+ testMethod.__name__, endpointName, fileURL)
            return False

        endpointRegex = re.compile('<h3 class=[\"\']endpoint[\"\']>[\S\s]*<\/h3>')
        endpointStart = endpointHeading.end()
        endpointEnd =
        endpointElement = endpointRegex.search(docResponse.text, endpointHeading.end())
        if not endpointElement:
            if not quiet:
                print "Found no endpoint after %s in %s" % (endpointName, fileURL)
            return False
        docVerb, docEndpointURL = re.search("(POST|GET|PUT|PATCH|DELETE) (.*)", endpointElement.group()).groups()
        if docVerb != docStringVerb:
            if not quiet:
                print "%s Docstring verb is %s, corresponding API documentation is %s" \
                % (inspect.getfile(testMethod) +" "+ testMethod.__name__, docStringVerb, docVerb)
            return False
        if docEndpointURL != apiURL:

            if not quiet:
                print "%s Docstring API URL is %s, corresponding API documentation is %s" \
                % (inspect.getfile(testMethod) +" "+ testMethod.__name__, apiURL, docEndpointURL)
            return False
        return True
        source = inspect.getsource(testMethod)
        implementation = re.search("request\([\s\S]*[\'\"](POST|GET|PUT|PATCH|DELETE)[\'\"],[^\'\"]*[\'\"]([^\'\"]*)[\'\"]",source)
        if not implementation:
            if not quiet:
                print "%s Docstring refers to %s %s but implementation was not found." % (inspect.getfile(testMethod) +" "+ testMethod.__name__, docStringVerb, apiURL)
            return False
        if implementation.group(1) != docVerb:
            if not quiet:
                print "%s Docstring verb is %s but implementation is %s" % (inspect.getfile(testMethod) +" "+ testMethod.__name__, docStringVerb, implementation.group(1))
            return False
        apiShortURL = re.sub("\/api\/v[0-9]*\/","",apiURL)
        if implementation.group(2) != re.sub(":[^\/]*","{}",apiShortURL):
            if not quiet:
                print "%s Docstring refers to %s URL but implementation is %s" %(inspect.getfile(testMethod) +" "+ testMethod.__name__, apiShortURL, implementation.group(2))
            return False
    return True

def test_methods():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"canvasapi")

    for py in [f[:-3] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py']:
        mod = __import__('canvasapi.'+py)
        classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
        for cls in classes:
            setattr(sys.modules[__name__], cls.__name__, cls)
            methods = inspect.getmembers(cls, inspect.ismethod)
            for methodname, method in methods:
                test_method(method)
