"""
Kahnsept - Entity/Relationship system

"""

import simplejson
import code
import sys
import re
import shelve
import datetime

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
    
    def is_instance(self, inst):
        return isinstance(inst, self)
    

class BuiltIn(Entity):
    builtin_types = enum('Number', 'Text', 'Date', 'Boolean')
    py_types = [[int, long, float],
                [str, unicode],
                [datetime.datetime, datetime.date],
                [bool]]
    type_defaults = [0, '', datetime.datetime.now(), False]

    def __init__(self, builtin_type):
        self.builtin_type = builtin_type
        name = self.builtin_types(builtin_type)
        super(BuiltIn, self).__init__(name)
        self._value = self.type_defaults[builtin_type]
        globals()[name] = self
        
    def is_instance(self, inst):
        return isinstance(inst, self.py_types[self.builtin_type])
        
    @staticmethod
    def init_all():
        for bi in BuiltIn.builtin_types.values():
            BuiltIn(bi)
        
    def add_prop(self, name):
        raise Exception("Can't add properties to builtin types")


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
    def __init__(self, entity, tag=None, card=card.single, default=None):
        self.entity = entity
        self.tag = tag
        self.card = card
        self.default = default
        
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
        if prop_name not in self._mValues:
            return None
        return self._mValues[prop_name]
    
    def __setattr__(self, prop_name, value):
        if value is None:
            del self._mValues[prop_name]
            return
        
        self._mValues[prop_name] = value
        
    def JSON(self):
        json = {'id': self._id,
                'type': self._entity}
        json.update(self._mValues)
        return json
    
class KahnseptEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entity):
            return JSONString("Entity('%s')" % obj.name)
        if isinstance(obj, Instance):
            return JSONString("%s<%d>" % (obj._entity.name, obj._id))
        return super(KahnseptEcoder, self).default(self, obj)
    
class JSONString(simplejson.encoder.Atomic):
    def __init__(self, s):
        self.s = s
        
    def __str__(self):
        return self.s
    
"""
Initialize the builtin types once
"""
BuiltIn.init_all()
    
def interactive():
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
    
    code.interact("", local=globals())
    
if __name__ == '__main__':
    interactive()
