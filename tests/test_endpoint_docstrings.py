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
    call_lines = re.findall("`(POST|GET|PUT|PATCH|DELETE)([^<]*)<([^>]*)>`_", inspect.getdoc(testMethod))
    if len(call_lines) == 0:
        if not quiet:
            # Docstring exists, has a :calls: line, contains a URL, but could
            # not be parsed;
            print "%s Failed to parse :calls: line." % (method_string)
        return False
    for call_line in call_lines:
        if not test_docString(method_string, call_line, quiet):
            return False
    return True

def test_docString(method_string, call_line, quiet):
    docstring_verb, api_URL, doc_URL = call_line
    api_URL = ''.join(api_URL.split())
    if api_URL[-1] == '/':
        api_URL = api_URL[0:-1]
    docfile_URL, endpointName = re.search("([^#]*)#(.*)",doc_URL).groups()
    html_doc_response = requests.get(docfile_URL)
    if html_doc_response.status_code != requests.codes.ok:
        if not quiet:
            print "%s docstring URL request returned %d" % (method_string, html_doc_response.status_code)
        return False

    endpoint_h2 = re.search("name=[\'\"]%s[\'\"]" % endpointName, html_doc_response.text)
    if not endpointName:
        if not quiet:
            print "%s docstring URL does not contain an endpoint name in link to API documentation" \
            % method_string
        return False
    if not endpoint_h2:
        if not quiet:
            print "%s docstring refers to %s in %s, not found" % (method_string, endpointName, docfile_URL)
        return False

    endpoint_element_re = re.compile('<h3 class=[\"\']endpoint[\"\']>[^<]*<\/h3>')
    endpoint_search_start_pos = endpoint_element_re.search(html_doc_response.text, endpoint_h2.end()).start()
    after_endpoint_re = re.compile('<[^h\/]')
    endpoint_search_end = after_endpoint_re.search(html_doc_response.text, endpoint_search_start_pos)
    if not endpoint_search_end:
        endpoint_search_stop_pos = len(html_doc_response.text)
    else:
        endpoint_search_stop_pos = endpoint_search_end.start()
    endpoint_element_match = endpoint_element_re.search(html_doc_response.text, endpoint_search_start_pos, endpoint_search_stop_pos)
    endpoint_element_list = []
    while endpoint_element_match:
        endpoint_element_list.append(endpoint_element_match.group())
        endpoint_element_match = endpoint_element_re.search(html_doc_response.text, endpoint_element_match.end(), endpoint_search_stop_pos)
    if len(endpoint_element_list) == 0:
        if not quiet:
            print "Found no endpoint after %s in %s" % (endpointName, docfile_URL)
        return False
    docfile_lines = []
    for endpoint_element_str in endpoint_element_list:
        docfile_match = re.search("(POST|GET|PUT|PATCH|DELETE) (.*)", endpoint_element_str)
        docfile_lines.append(docfile_match.group())
        docfile_verb, docfile_API_URL = docfile_match.groups()
        if docfile_verb != docstring_verb:
            continue
        if docfile_API_URL != api_URL:
            continue
        return True
    if not quiet:
        print "%s docstring %s not found in %s (found %s)" \
            % (method_string, docstring_verb + " " + api_URL, docfile_URL, str(docfile_lines))
    return False

def test_methods():
    methods = set()
    for _, module in inspect.getmembers(canvasapi, inspect.ismodule):
        for _, theclass in inspect.getmembers(module, inspect.isclass):
            for _, method in inspect.getmembers(theclass, inspect.ismethod):
                methods.add(method)
    for methodToTest in methods:
        test_method(methodToTest)
