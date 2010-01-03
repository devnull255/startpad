import cherrypy
expose = cherrypy.expose

import os.path
from StringIO import StringIO

from kahnsept import *

html = """\
<html>
<head>
<style>
#command {
width: 700px;
}
div {
margin: 0;
padding: 0;
}
.error {
color: red;
margin: auto;
width: 700px;
}
</style>
<script>
function Loaded()
{
    document.getElementById('command').focus();
}
</script>
<title>Kahnsept - Knowledge Management System</title>
</head>
<body>
<h1><script>document.write(document.title)</script></h1>
<pre>
%(body)s
</pre>
<div class="error">%(error)s</div>
<form action="/command" method="post">
<label for="command">Command: </label><input id="command" name="command"/> <input type="submit" value="Go"/>
</form>
<script>Loaded()</script>
</html>
"""

# We want a persisent global Kahnsept world for all web requests - this only works if
# all requests share the same process space (single thread?)
world = World()
error = ""
keep_running = True

class KHandler(object):
    """ Handle web requests for Kahnsept commands """

    @expose
    def index(self):
        global world, error
        
        string_file = StringIO()
        world.write_json(string_file)
        return html % {'body':string_file.getvalue(), 'error':error}
        
    @expose
    def command(self, command=None):
        global world, error

        try:
            error = ""
            exec command in globals(), World.scope
        except Exception, e:
            error = "Eval error: %r" % e

        raise cherrypy.HTTPRedirect('/')
    
    @expose
    def stop(self):
        raise SystemExit
                
if __name__ == '__main__':
    conf = os.path.join(os.path.dirname(__file__), 'web_server.conf')
    cherrypy.quickstart(KHandler(), config=conf)
