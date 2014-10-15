#!/usr/bin/env python3

import argparse

import sys
import socket
import itertools
from socket import socket as Socket

BUFFER_SIZE = 4096

def main():

    # Command line arguments. Use port 8080 by default: widely used for proxys
    # and >1024 so we don't need sudo to run.
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=8080, type=int,
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
        # no multithreaded yet, would need to set up atomic updates to dict.
        # Might be automatic in python?

        # Create empty dict for cached pages
        cache_dict = {}

        print("Proxy server ready")

        while True:
            # Accept TCP connection from client
            with server_socket.accept()[0] as connection_socket:
                
                request_string = connection_socket.recv(BUFFER_SIZE).decode().replace('\r\n', '\n')
                http_dict = http_parse(request_string)
                full_url = http_dict['Host'] + http_dict['Url']

                # Check cache for page
                cached_page = cache_dict.get(full_url)

                # If it's not in the cache then get the page
                if cached_page is None:
                    cached_page = get_page(http_dict['Host'], request_string).replace('\r\n', '\n').encode()
                    cache_dict[full_url] = cached_page
                    
                    print("Serving page", full_url, "from cache")
                    print(cached_page)
                    
                else:
                    print("Got page from", full_url, "and cached it")

                connection_socket.send(cached_page)

                # handle updating old cached pages here?
    
    return 0


# Taken from the web server code
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

def http_port():
    return 80

def get_page(server_address, request):

    with Socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

        # Connect to server
        client_socket.connect((server_address, http_port()))

        # Get the page
        client_socket.send(request.encode())
        reply = client_socket.recv(BUFFER_SIZE).decode()
        reply2 = client_socket.recv(BUFFER_SIZE).decode()

    return reply + reply2


def http_format_request(request_dict): 
    return """GET {1} HTTP/1.1
Host: {2}""".format(request_dict['Url'], request_dict['Host'])


if __name__ == "__main__":
    sys.exit(main())
