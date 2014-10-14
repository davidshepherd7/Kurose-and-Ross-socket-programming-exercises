#!/usr/bin/env python3

import sys
import argparse

import time
import socket
from socket import socket as Socket

def main():

    # Command line arguments. Use a server_port > 1024 by default so that we can run
    # server without sudo.
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--server-port', '-p', default=2081, type=int,
                        help='Server_Port to use')
    
    parser.add_argument('--run-server', '-s', action='store_true',
                        help='Run a ping server')
    
    parser.add_argument('server_address', default='localhost',
                        help='Server to ping, no effect if running as a server.')
    
    args = parser.parse_args()


    if args.run_server:
        return run_server(args.server_port)
    else:
        return run_client(args.server_address, args.server_port,)




def run_server(server_port):
    """Run the UDP pinger server
    """

    # Create the server socket (to handle UDP requests using ipv4), make sure
    # it is always closed by using with statement.
    with Socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:

        # The socket stays connected even after this script ends. So in order
        # to allow the immediate reuse of the socket (so that we can kill and
        # re-run the server while debugging) we set the following option. This
        # is potentially dangerous in real code: in rare cases you may get junk
        # data arriving at the socket.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Set the server port
        server_socket.bind(('', server_port))

        # Start accepting ping requests
        print("Ping server ready on port", server_port)
        while True:
            # Receive message and send one back
            _, client_address = server_socket.recvfrom(1024)
            server_socket.sendto("".encode(), client_address)

    return 0


def run_client(server_address, server_port):
    """Ping a UDP pinger server running at the given address
    """

    with Socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:

        # The socket stays connected even after this script ends. So in order
        # to allow the immediate reuse of the socket (so that we can kill and
        # re-run the server while debugging) we set the following option. This
        # is potentially dangerous in real code: in rare cases you may get junk
        # data arriving at the socket.
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # We don't care what port the client uses, leave it as the default

        # Time out after 1 second
        client_socket.settimeout(1.0)

        # Send 10 empty UDP packets to the server
        print("Pinging", str(server_address), "on port", server_port)
        for i in range(10):

            # Send packet to server
            client_socket.sendto("".encode(), (server_address, server_port))

            # Receive packet and print results
            try:
                timer_start = time.time()
                _, _ = client_socket.recvfrom(1024)
                timer_stop = time.time()

                # Note: for timing of cpu-bound functions the timeit module
                # should be used to avoid issues with garbage collection. Since
                # we are measuring network times this should be fine.

            except socket.timeout:
                print("Packet lost")

            else:
                print("Round trip time: {:.3f}ms".format((timer_stop - timer_start)*1000))
            

    return 0

if __name__ == "__main__":
    sys.exit(main())
