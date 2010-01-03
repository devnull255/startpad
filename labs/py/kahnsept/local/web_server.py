import cProfile
import pstats
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from StringIO import StringIO
import cgi

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


        self.open_content()
        string_file = StringIO()
        world.write_json(string_file)
        self.write(html % {'body':string_file.getvalue()})
        self.close_content()
        
    def open_content(self, code=200, mime_type="text/html"):
        self.send_response(code)
        self.send_header("Content-type", mime_type)
        self.buffer = StringIO()
        
    def write(self, s):
        self.buffer.write(s)
        
    def close_content(self):
        self.send_header("Content-Length", len(self.buffer.getvalue()))
        self.end_headers()
        self.wfile.write(self.buffer.getvalue())
        
    def do_POST(self):
        global count, world

        if self.path != "/command":
            self.not_found()
            return
        
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                 environ={'REQUEST_METHOD':'POST',
                                          'CONTENT_TYPE':self.headers['Content-Type']})
        
        command = form['command'].value
        self.log_message("Command: %s" % command)
        
        exec command

        self.redirect("/")
        
    def not_found(self):
        self.open_content(404, "text/plain")
        self.write("Nobody, home")
        self.close_content()
        
    def redirect(self, url):
        self.open_content(302)
        self.send_header("Location", url)
        self.close_content()

if __name__ == '__main__':
    server = HTTPServer(("", 8010), KHandler);
    while keep_running:
        server.handle_request()

