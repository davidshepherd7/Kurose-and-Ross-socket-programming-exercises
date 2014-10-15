I tested this code by using `curl` to grab a website via the proxy. If the proxy is running on the same computer the correct command to do this is

    curl --proxy localhost:8080 http://orgmode.org/manual/Introduction.html

where I've used the url of the introduction to emacs' org-mode because it's short and mostly text, and so won't fill your terminal with junk.

My implementation is only partially complete: 

* It only forwards the first chunk of the recived data (i.e. `recv(..)` is only called once) because the rules for receiving later chunks are [complex](http://greenbytes.de/tech/webdav/draft-ietf-httpbis-p1-messaging-24.html#message.body.length). 
* It isn't multithreaded because this would be more complex to implement in ways that have nothing to do with network protocols.
* It doesn't handle updating the results when they are out of date because it would be tricky to test (I guess we would need to fake the data and the current time, bit more fiddly).
