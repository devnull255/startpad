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
    _mEntities = {}
    
    def __new__(cls, name):
        """
        Share instances of Entity for a given name
        """
        if name in cls._mEntities:
            return cls._mEntities[name]
        e = super(Entity, cls).__new__(cls)
        cls._mEntities[name] = e
        return e

    def __init__(self, name):
        self.name = name
        self._props = []
        self._mProps = {}
        
    def add_prop(self, prop):
        if prop not in self._props:
            self._props.append(prop)
            
    def new(self):
        """
        Return an instance of this Entity type
        """
        return Instance(self)

"""
The allowed cardinalities of a property
"""             
card = enum('single', # 0..1
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
    def __init__(self, entity, tag=None, card=card.single):
        self.entity = entity
        self.tag = tag
        self.card = card
        
class Instance(object):
    """
    An instance of an Entity definition.
    
    instance.x - get the value of the property defined to an x type (or tagged x)
    """
    idNext = 0

    def __init__(self, entity):
        self.__dict__['_entity'] = entity
        self.__dict__['_mValues'] = {}
        self.__dict__['_id'] = Instance.idNext
        Instance.idNext += 1
        
    def __getattr__(self, prop_name):
        return self._mValues[prop_name]
    
    def __setattr__(self, prop_name, value):
        if value is None:
            del self._mValues[prop_name]
            return
        
        self._mValues[prop_name] = value
        
    def __repr__(self):
        return simplejson.dumps(self._mValues, indent=4)
        
        
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
    
    code.interact("", local=globals())
    
if __name__ == '__main__':
    interactive()
