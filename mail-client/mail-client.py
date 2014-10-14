#!/usr/bin/env python3

import argparse

import sys
import socket
from socket import socket as Socket


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('my_address', type=str)
    parser.add_argument('mail_server', type=str)
    parser.add_argument('their_address', type=str)
    parser.add_argument('message', type=str)
    args = parser.parse_args()


    send_mail(args.my_address, args.mail_server, args.their_address, args.message)
    

    # success
    return 0


def send_mail(my_address, mail_server, their_address, message):

    # Create the socket
    with Socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

        # Set a 1 second timeout
        client_socket.settimeout(1.0)

        # Connect to mail server
        client_socket.connect((mail_server, 25))

        # Define some helper functions
        def send(string):
            """Helper function: fix newlines, encode and send a string"""
            final = string.replace('\n', '\r\n').encode('ascii')
            print("Sending:", final)
            client_socket.send(final)

            return

        def recv_and_check(expected=250):
            """Helper function: recive reply and check it's ok"""
            reply = client_socket.recv(2048)
            print("Got:", reply)
            
            # Check it's the code we expected
            code = int(reply.rstrip().split()[0]) 
            if code != expected:
                raise Exception(reply)

            return

        
        # Get initial message from server
        recv_and_check(220)

        # Send greeting
        send('HELO {}\n'.format(my_address.split('@')[1]))
        recv_and_check()

        # Set our address
        send('MAIL FROM: {}\n'.format(my_address))
        recv_and_check()

        # Set their address
        send('RCPT TO: {}\n'.format(their_address))
        recv_and_check()

        # Prepare to send message
        send('DATA\n')
        recv_and_check(354)

        # Send the message itself followed by terminator
        send('{}\n.\n'.format(message))
        recv_and_check()

        # Done, quit
        send('QUIT\n')
        recv_and_check(221)

    return
    


if __name__ == "__main__":
    sys.exit(main())
