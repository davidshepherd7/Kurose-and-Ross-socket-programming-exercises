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

    # Fill in the code to talk to the mail server here. Read the file
    # read-first.md to find out how to set up a mail server for testing. A log
    # of a telnet session with your mail server may be (very) useful here.

    raise NotImplementedError

    return
    


if __name__ == "__main__":
    sys.exit(main())
