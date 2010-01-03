import cProfile
import pstats
import BaseHTTPServer
import SimpleHTTPServer

handler = SimpleHTTPServer.SimpleHTTPRequestHandler;
server = BaseHTTPServer.HTTPServer(("", 8010), handler);

try:
    cProfile.run("server.serve_forever()", "WebServer")
except:
    p = pstats.Stats("WebServer")
    p.sort_stats('time').print_stats(10)
