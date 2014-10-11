#!/usr/bin/env python3

import argparse

import sys
import itertools
import socket
from socket import socket as Socket

# A simple web server

# Issues:
# Unicode files only
# Ignores 'Connection' header
# Ignores CRLF requirement
# Header must be < 1024 bytes
# ...
# probabaly loads more


def main():

    # Command line arguments. Use a port > 1024 by default so that we can run
    # without sudo, for use as a real server you need to use port 80.
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=2080, type=int,
                        help='Port to use')
    args = parser.parse_args()

    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # The socket stays connected even after this script ends. So in order
        # to allow the immediate reuse of the socket (so that we can kill and
        # re-run the server while debugging) we set the following option. This
        # is potentially dangerous in real code: in rare cases you may get junk
        # data arriving at the socket.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind(('', args.port))
        server_socket.listen(1)

        print("server ready")

        while True:
            connection_socket, _ = server_socket.accept()
            try: 
                request = connection_socket.recv(1024).decode('ascii')
                reply = http_handle(request)
                connection_socket.send(reply.encode('ascii'))

            # Make sure the socket gets closed no matter what
            finally:
                connection_socket.close()

            print("Received request:\n", request.rstrip())
            print("Replied with:\n", reply.rstrip())
    
    return 0


def http_handle(request_string):
    """Given a http requst return a response

    Both request and response are unicode strings with platform standard
    line endings.
    """

    assert not isinstance(request_string, bytes)

    request = http_parse(request_string)

    # Only handle simple case
    assert request['Method'] == "GET"
    assert request['Version'] == "HTTP/1.1"

    filepath = request['Url']


    try:
        with open(filepath) as f:
            body = f.read()
    
    except FileNotFoundError:
        status = 404
        body = 'File not found'
        
    except UnicodeDecodeError:
        status = 400
        body = 'Cannot handle binary files'
        
    else:
        status = 200

    response = {'Version' : "HTTP/1.1",
                'Status' : status,
                'Body' : body,
                'Content-Type': 'text/plain',
                } 

    return http_response_from_dict(response)


def http_parse(request_string):
    """Given a request return a dict containing the request data

    Members of dict are: Method, Url, Version, Body, and any other
    headers supplied by the request.
    """

    try:
        [header, body] = request_string.split('\n\n')
    except ValueError:
        header = request_string
        body = 'nothing'
    
    header_lines = header.rstrip().split('\n')

    # Get the first line into a dict
    method, url, version = header_lines[0].split()
    firstline_dict = {'Method' : method,
                      'Url' : url,
                      'Version' : version,
                      'Body' : body}

    # And the rest
    headers = [l.split(': ') for l in header_lines[1:]]

    # Make the dict combining all these parts
    return dict(itertools.chain(firstline_dict.items(),
                                headers,
                                [('Body', body)]))


def status_code_to_phrase(code):
    phrases = {200: 'OK',
               404: 'Not Found',
               400: 'Bad Request',
               }

    return phrases[code]
               


def http_response_from_dict(message_dict):
    """Given a dictionary of parameters create a http response

    """

    status_line = "{0} {1} {2}\n".format\
      (message_dict['Version'], message_dict['Status'],
       status_code_to_phrase(message_dict['Status']))

    header_items = [(k,v) for k, v in message_dict.items()
                    if k not in ['Version', 'Status', 'Body']]

    header_lines = "\n".join(["{0}: {1}".format(k, v) for k, v in header_items])

    return ''.join([status_line, header_lines,
                    "\n\n", message_dict['Body'], "\n"])




# Testing
# ============================================================
# test with `nosetests3 web-server.py`

def test_http_parse():
    """Test parsing function for a sample request"""

    # Lack of indentation must be preserved!
    test_string = """GET aurl/b HTTP/1.1
Host: www.someschool.edu
Connection: close
User-agent: Mozilla/5.0
Accept-language: fr

body"""

    header_dict = http_parse(test_string)

    assert header_dict['Method'] == 'GET'
    assert header_dict['Url'] == 'aurl/b'
    assert header_dict['Version'] == 'HTTP/1.1'
    assert header_dict['Host'] == 'www.someschool.edu'
    assert header_dict['Connection'] == 'close'
    assert header_dict['User-agent'] == 'Mozilla/5.0'
    assert header_dict['Body'] == 'body'

    return


def test_http_form_response():

    test_dict = {'Version' : 'HTTP/1.1',
                 'Status' : 200,
                 'Connection' : 'close',
                 
                 'Body' : 'body\n',
                 }


    response = http_response_from_dict(test_dict)
    assert response == """HTTP/1.1 200 OK
Connection: close

body
"""


if __name__ == "__main__":
    sys.exit(main())
