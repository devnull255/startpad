import cProfile
import pstats
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from StringIO import StringIO

from kahnsept import *

keep_running = True

html = """\
<html>
<head>
<style>
#command {
width: 700px;
}
</style>
<title>Kahnsept - Knowledge Management System</title>
</head>
<body>
<h1><script>document.write(document.title)</script></h1>
<pre>
%(body)s
</pre>
<form action="/command" method="post">
<label for="command">Command: </label><input id="command" name="command"/> <input type="submit" value="Go"/>
</form>
</html>
"""

# We want a persisent global Kahnsept world for all web requests!
world = World()
count = 0

#handler = SimpleHTTPServer.SimpleHTTPRequestHandler;
class KHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def do_GET(self):
        global keep_running, world

        if self.path == "/stop":
            keep_running = False

        if self.path is not "/":
            self.not_found()
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        string_file = StringIO()
        world.write_json(string_file)
        self.wfile.write(html % {'body':string_file.getvalue()})
        
    def do_POST(self):
        global count, world

        if self.path != "/command":
            self.not_found()
            return

        count += 1
        Entity("New%d" % count, world)
        
        self.redirect("/")
        
    def not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("Nobody, home")
        
    def redirect(self, url):
        self.send_response(302)
        self.send_header("Location", url)
        self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(("", 8010), KHandler);
    while keep_running:
        server.handle_request()

