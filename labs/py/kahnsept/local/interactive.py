import simplejson
import code2
import sys
    
def interactive(globals=None, locals=None):
    sys_display = sys.displayhook
    
    def json_display(value):
        try:
            if isinstance(value, Instance):
                value = value.JSON()
            s = simplejson.dumps(value, cls=KahnseptEncoder, indent=4)
            print s
        except Exception, e:
            sys_display(value)
            
    sys.displayhook = json_display
    
    code2.interact("", globals=globals, local=locals)
    
class KahnseptEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entity, Property, Relation, Instance):
            return JSONString(repr(obj))
        return super(KahnseptEcoder, self).default(self, obj)
    
class JSONString(simplejson.encoder.Atomic):
    def __init__(self, s):
        self.s = s
        
    def __str__(self):
        return self.s