"""
Kahnsept - Entity/Relationship system

"""

import simplejson
import code
import sys
import re
import shelve

from enum import *

local_cache = "kahnsept.bin"

TRACE = True

class Entity(object):
    """
    Entities are the definitions of all Instances in Kahnsept.
    
    They are collections of Properties.
    """
    def __init__(self, name):
        self.name = name
        self._props = []
        
    def add_prop(self, prop):
        if prop not in self._props:
            self._props.append(prop)

"""
The allowed cardinalities of a property
"""             
arity = enum('single', # 0..1
             'multiple', # 0..n
             'one', # 1..1 
             'many' # 1..n
             )
        
class Property(object):
    """
    Properties definitions contain:
    
    - type (entity)
    - tag (name) - optional
    - cardinality (min and max values allowed)
    """
    def __init__(self, entity, tag=None, arity=arity.single):
        self.entity = entity
        self.tag = tag
        self.arity = arity
        
        
class MapWrapper(object):
    """
    Wrap a mapping object, and return an object where the keys
    of the object can be accessed via attribute notation (much as in
    javascript: d.prop rather than d['prop'].
    
    We also make the json format be the repr for these objects.
    """
    _m = None
    _m_wrappers = {}
    
    def __new__(cls, m):
        """
        Share instances of MapWrapper for a given identify of map
        """
        if id(m) in cls._m_wrappers:
            return cls._m_wrappers[id(m)]
        mp = super(MapWrapper, cls).__new__(cls)
        cls._m_wrappers[id(m)] = mp
        mp._m = m
        return mp

    def __getattr__(self, name):
        value = self._m[name]
        if type(value) == dict:
            value = MapWrapper(value)
        return value
    
    def __setattr__(self, name, value):
        # We must initialize ._m as our first act!
        if self._m is None:
            super(MapWrapper, self).__setattr__(name, value)
            return
        
        if value is None:
            del self._m[name]
            return

        self._m[name] = value
        
    def __repr__(self):
        return simplejson.dumps(self._m, indent=4)
    
def interactive():
    sys_display = sys.displayhook
    
    def json_display(value):
        try:
            s = simplejson.dumps(value, indent=4)
            print s
        except:
            sys_display(value)
            
    sys.displayhook = json_display
    
    d = {}
    
    code.interact("", local=d)
    
if __name__ == '__main__':
    interactive()
