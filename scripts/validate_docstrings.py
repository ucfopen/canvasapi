from __future__ import absolute_import, division, print_function, unicode_literals

import inspect
import os
import re
import sys

import requests

sys.path.append(os.path.join(sys.path[0], '..'))

import canvasapi  # noqa


def validate_method(themethod, quiet=False):
    # No docstring means no erroneous docstrings
    if not inspect.getdoc(themethod):
        return True

    # Docstrings without API calls can't be checked this way
    if not re.search(r':calls:', inspect.getdoc(themethod)):
        return True
    if not re.search(r'<\S*>', inspect.getdoc(themethod)):
        return True

    method_string = inspect.getfile(themethod) + " " + themethod.__name__
    call_lines = re.findall(
        '`(POST|GET|PUT|PATCH|DELETE)([^<]*)<([^>]*)>`_',
        inspect.getdoc(themethod)
    )
    if not call_lines:
        if not quiet:
            # Docstring exists, has a :calls: line, contains a URL, but could
            # not be parsed;
            print('{} Failed to parse :calls: line.'.format(method_string))
        return False
    for call_line in call_lines:
        if not validate_docstring(method_string, call_line, quiet):
            return False
    return True


def validate_docstring(method_string, call_line, quiet):
    docstring_verb, api_URL, doc_URL = call_line
    api_URL = ''.join(api_URL.split())
    if api_URL[-1] == '/':
        api_URL = api_URL[0:-1]
    docfile_URL, endpoint_name = re.search('([^#]*)#?(.*)', doc_URL).groups()
    html_doc_response = requests.get(docfile_URL)
    if html_doc_response.status_code != requests.codes.ok:
        if not quiet:
            print('{} docstring URL request returned {}'.format(
                method_string,
                html_doc_response.status_code
            ))
        return False

    endpoint_h2 = re.search(
        r'<h2[^>]*name=[\'\"]{}[\'\"]'.format(endpoint_name),
        html_doc_response.text
    )
    if not endpoint_name:
        if not quiet:
            print((
                '{} docstring URL does not contain an endpoint name in link'
                ' to API documentation'
            ).format(method_string))
        return False
    if not endpoint_h2:
        if not quiet:
            print('{} docstring refers to {} in {}, not found'.format(
                method_string, endpoint_name, docfile_URL
            ))
        return False

    endpoint_element_re = re.compile(
        r'<h3 class=[\"\']endpoint[\"\']>[^<]*<\/h3>'
    )

    endpoint_search_start_match = endpoint_element_re.search(
        html_doc_response.text,
        endpoint_h2.end()
    )
    if not endpoint_search_start_match:
        if not quiet:
            print('Found no endpoint after {} in {}'.format(
                endpoint_name,
                docfile_URL
            ))
        return False

    endpoint_search_start_pos = endpoint_search_start_match.start()
    after_endpoint_re = re.compile(r'<[^h\/]')
    endpoint_search_end = after_endpoint_re.search(html_doc_response.text,
                                                   endpoint_search_start_pos)
    if not endpoint_search_end:
        endpoint_search_stop_pos = len(html_doc_response.text)
    else:
        endpoint_search_stop_pos = endpoint_search_end.start()
    endpoint_element_match = endpoint_element_re.search(
        html_doc_response.text,
        endpoint_search_start_pos,
        endpoint_search_stop_pos
    )
    endpoint_element_list = []
    while endpoint_element_match:
        endpoint_element_list.append(endpoint_element_match.group())
        endpoint_element_match = endpoint_element_re.search(
            html_doc_response.text,
            endpoint_element_match.end(),
            endpoint_search_stop_pos
        )

    if not endpoint_element_list:
        if not quiet:
            print('Found no endpoint after {} in {}'.format(
                endpoint_name,
                docfile_URL
            ))
        return False
    docfile_lines = []
    for endpoint_element_str in endpoint_element_list:
        docfile_match = re.search(
            '(POST|GET|PUT|PATCH|DELETE) (.*)',
            endpoint_element_str
        )
        docfile_lines.append(docfile_match.group())
        docfile_verb, docfile_API_URL = docfile_match.groups()
        if docfile_verb != docstring_verb:
            continue
        if docfile_API_URL != api_URL:
            continue
        return True
    if not quiet:
        print('{} docstring {} not found in {} (found {})'.format(
            method_string,
            docstring_verb + ' ' + api_URL,
            doc_URL,
            str(docfile_lines)
        ))
    return False


def test_methods():
    methods = set()
    for _, module in inspect.getmembers(canvasapi, inspect.ismodule):
        for _, theclass in inspect.getmembers(module, inspect.isclass):
            for _, method in inspect.getmembers(theclass, inspect.isroutine):
                methods.add(method)
    for method_to_test in methods:
        validate_method(method_to_test)


if __name__ == '__main__':
    test_methods()
