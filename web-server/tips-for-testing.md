
* It's much easier to test parsing functions on a python string, without any involvement of sockets (i.e. unit test them)

* You should test the socket code is working locally using e.g.

    `telnet localhost 8011`

  and then inputting the request as shown in the text book.

* Trying it out using a real web browser can be more tricky. First run the server as `sudo ./web-server.py -p 80` (sudo is needed for low number ports). Secondly you will need to make sure that port 80 is accessible from outside your local network, look up information on "port forwarding" for this.
