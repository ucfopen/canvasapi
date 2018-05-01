import inspect
import re
import requests

def test_methods(testMethod, quiet=False):
    # Check if docstring contains a calls line; automatic pass if not
    if re.search(":calls:", inspect.getdoc(testMethod)):
        callLine = re.search(":calls:[^_]*_", inspect.getdoc(testMethod)).group()
        docStringVerb, apiURL, docURL = re.search("(POST|GET|PUT|PATCH|DELETE)[^/]*(/[^ ]*)[^<]*<([^>]*)>",callLine).groups()
        fileURL, endpointName = re.search("([^#]*)#(.*)",docURL).groups()
        docResponse = requests.get(fileURL)
        if docResponse.status_code != requests.codes.ok:
            if not quiet:
                print "%s Docstring URL request returned %d" % (testMethod.__name__, docResponse.status_code)
            return False

        endpointHeading = re.search("name=[\'\"]%s[\'\"]" % endpointName, docResponse.text)
        if not endpointName:

            if not quiet:
                print "%s Docstring URL does not contain an endpoint name in link to API documentation" \
                % testMethod.__name__
            return False
        if not endpointHeading:
            if not quiet:
                print "%s Docstring refers to %s in %s, not found" % (testMethod.__name__, endpointName, fileURL)
            return False

        endpointRegex = re.compile('<h3 class=[\"\']endpoint[\"\']>[\S\s]*<\/h3>')

        endpointElement = endpointRegex.search(docResponse.text, endpointHeading.end())
        if not endpointElement:
            if not quiet:
                print "Found no endpoint after %s in %s" % (endpointName, fileURL)
            return False
        docVerb, docEndpointURL = re.search("(POST|GET|PUT|PATCH|DELETE) (.*)", endpointElement.group()).groups()
        if docVerb != docStringVerb:
            if not quiet:
                print "%s Docstring verb is %s, corresponding API documentation is %s" \
                % (testMethod.__name__, docStringVerb, docVerb)
            return False
        if docEndpointURL != apiURL:

            if not quiet:
                print "%s Docstring API URL is %s, corresponding API documentation is %s" \
                % (testMethod.__name__, apiURL, docEndpointURL)
            return False

        source = inspect.getsource(testMethod)
        implementation = re.search("request\([\s\S]*[\'\"](POST|GET|PUT|PATCH|DELETE)[\'\"],[^\'\"]*[\'\"]([^\'\"]*)[\'\"]",source)
        if not implementation:
            if not quiet:
                print s
                print "%s Docstring refers to %s %s but implementation was not found." % (testMethod.__name__, docStringVerb, apiURL)
            return False
        if implementation.group(1) != docVerb:
            if not quiet:
                print "%s Docstring verb is %s but implementation is %s" % (testMethod.__name__, docStringVerb, implementation.group(1))
            return False
        apiShortURL = re.sub("\/api\/v[0-9]*\/","",apiURL)
        if implementation.group(2) != re.sub(":[^\/]*","{}",apiShortURL):
            if not quiet:
                print "%s Docstring refers to %s URL but implementation is %s" %(testMethod.__name__, apiShortURL, implementation.group(2))
            return False
    return True
