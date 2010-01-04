import cProfile
import pstats
import BaseHTTPServer
import SimpleHTTPServer

counter = 0

#handler = SimpleHTTPServer.SimpleHTTPRequestHandler;
class TestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        
    def do_GET(self):
        global counter
        if self.path is not "/":
            self.not_found()
            return

        counter += 1
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("Hello, world: %d" % counter)
        
    def not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("Nobody, home")

if __name__ == '__main__':
    server = BaseHTTPServer.HTTPServer(("", 8010), TestHandler);
    server.serve_forever()
    
    try:
        cProfile.run("server.serve_forever()", "WebServer")
    except:
        p = pstats.Stats("WebServer")
        p.sort_stats('time').print_stats(10)
