Unfortunately gmail [no longer accepts unencrypted smtp connections](http://stackoverflow.com/questions/1516754/connecting-to-smtp-gmail-com-via-command-line), so we can't use it to test our client.

The only alternative I've found is to run your own mail server. I've chosen to run it in a local mail only mode, which limits the amount of interesting stuff we can do but at least means we can't be used as a spam relay! I used `postfix`, which can be set up on Ubuntu 13.10 (and probably most other Debian-based Linux distributions) by running

    sudo apt-get install postfix
    
and in the curses dialog that appears choose to run in local mode. The server should now be running, you can test it by running

    telnet localhost 25
    
and following the instructions on pg. 123 of the textbook. Note that you can only send mail to users that exist, i.e. `$USER@localhost` (where `$USER` is your username). For me this interation looks like this:

    telnet localhost 25
    Trying 127.0.0.1...
    Connected to localhost.
    Escape character is '^]'.
    220 david-simulations ESMTP Postfix (Ubuntu)
    helo localhost
    250 david-simulations
    mail from: david@localhost
    250 2.1.0 Ok
    rcpt to: david@localhost
    250 2.1.5 Ok
    data
    354 End data with <CR><LF>.<CR><LF>
    hello
    . 
    250 2.0.0 Ok: queued as 015D3120C36
    quit
    221 2.0.0 Bye
    Connection closed by foreign host.
    
Then we can check that the mail was delivered with `cat /var/mail/david`:

    From david@localhost  Tue Oct 14 11:34:26 2014
    Return-Path: <david@localhost>
    X-Original-To: david@localhost
    Delivered-To: david@localhost
    Received: from localhost (localhost [127.0.0.1])
        by david-simulations (Postfix) with SMTP id 015D3120C36
        for <david@localhost>; Tue, 14 Oct 2014 11:34:11 +0100 (BST)
    Message-Id: <20141014103421.015D3120C36@david-simulations>
    Date: Tue, 14 Oct 2014 11:34:11 +0100 (BST)
    From: david@localhost

    hello
    

Great! Now we just need to implement this in python.
