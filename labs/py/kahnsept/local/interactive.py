"""
Interactive console - displays results using JSON format

TODO: Make this module generic - run interactive kahnsept from a "shell.py" using this module
"""

import simplejson as json
import code2
import sys
import re

from kahnsept import *

import dyn_dict
    
def interactive(ext_map=None, locals=None, encoder=None):
    sys_display = sys.displayhook
    
    def json_display(value):
        try:
            if isinstance(value, Command):
                value.go()
                return
            
            s = json.dumps(value, cls=encoder, indent=4)
            print s
        except Exception, e:
            print "Exception %r" % e
            sys_display(value)
            
    sys.displayhook = json_display
    
    code2.interact("", globals=ext_map, local=dyn_dict.DynDict({}, locals, Command.all_commands))
    
class Command(object):
    rePrefix = re.compile(r"^[ \t]*", re.M)
    short_text = "replace this text with description of your command"
    all_commands = {}
    
    def __init__(self, short_text):
        self.short_text = short_text
        self.name = self.__class__.__name__.lower()
        Command.all_commands[self.name] = self

    def go(self):
        print "Base class for interactive commands"
        
    def help(self, size="short"):
        print "%s - %s " % (self.name, self.short_text)
        if size != "short" and self.long_text is not None:
            print self.trim_prefix(self.long_text)

    @staticmethod
    def trim_prefix(s):
        return Command.rePrefix.sub('', s)
            
class Help(Command):
    def __init__(self):
        super(Help, self).__init__("type this command to print this message")

    def go(self):
        s = """
        Kahnsept Interactive Interpreter Commands:
        -----------------------------------------"""
        print Command.trim_prefix(s)
        for cmd in Command.all_commands:
            Command.all_commands[cmd].help()
            
class InteractiveEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (World, Entity, Property, Relation, Instance)):
            return json.JSONString(repr(obj))
        return super(InteractiveEncoder, self).default(obj)
    
def quick_test():
    t = Entity('Test')
    t.add_prop(world.Text, 'title')
    q = Entity("Question")
    q.add_prop(world.Text, 'prompt')
    Relation(t, q, Card.one_many)

    x = t.new()
    x.title = "My title"
    y = q.new()
    y.prompt = "What is your favorite color?"
    y.Test = x
    
    world.save_json()

if __name__ == '__main__':
    world = World()
    interactive(ext_map=globals(), locals=World.scope, encoder=InteractiveEncoder)
