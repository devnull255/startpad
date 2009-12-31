"""
Kahnsept - Entity/Relationship system

"""

import simplejson
import code2
import sys
import re
import shelve
import datetime

from enum import *
import parse_date

local_cache = "kahnsept.bin"

TRACE = True

"""
The allowed cardinalities of a property or relation
"""             
card = enum('one',
            'many',
            'one_one',   # 1:1 - matched (e.g. spouse)
            'one_many',  # 1:* - partition (e.g., children)
            'many_one',  # *:1 - reference (e.g., father)
            'many_many', # *:* - multi-set (e.g., siblings)
            many_one=0,  # synonym for 'one'
            many_many=1 # synonym for 'many'
            )

card_inverse = (card.one_many, card.many_many, card.one_one, card.many_one)

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
        self._mProps = {}
    
    @classmethod    
    def all_entities(cls):
        return cls._mEntities
        
    def add_prop(self, entity, tag=None, cd=None, default=None):
        """
        Add a new property or Relation to the Entity.  We require that all properties be uniquely identifiable:
        if two properties of the same type exist, they must BOTH be tagged.
        """
        if isinstance(entity, BuiltIn):
            if cd is None:
                cd = card.one
            prop = Property(entity, tag, cd, default)
            self._add_prop(prop)
            return prop
        
        # Define a Relation with another Entity
        if cd is None:
            cd = card.many_many
        rel = Relation(self, entity, cd, tag)

        # Add both (or neither) properties to each entity - atomically
        (propL, propR) = rel.get_props()
        pL = None
        try:
            pL = self._add_prop(propL)
            entity._add_prop(propR)
        except Exception, e:
            if pL is not None:
                self.del_prop(pL)
            raise e
        
        return rel
        
    def _add_prop(self, prop):
        name = prop.name()
        if self.get_prop(name):
            raise Exception("Duplicate property name: %s" % prop.name)
        self._mProps[name] = prop
        if TRACE:
            print "Adding prop %s to %s." % (name, self.name)
        return prop
        
    def del_prop(self, prop):
        name = prop.name
        if name in self._mProps:
            del self.mProps[name]

    def get_prop(self, name):
        if name is None:
            return None
        return self._mProps.get(name, None)
            
    def new(self):
        """
        Return an instance of this Entity type
        """
        return Instance(self)
    
    def is_instance(self, inst):
        return isinstance(inst, Instance) and inst._entity is self
    
    def coerce_value(self, value):
        if self.is_instance(value):
            return value
        return None

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
        
    def is_instance(self, inst):
        return isinstance(inst, self.py_types[self.builtin_type])
    
    def coerce_value(self, value):
        """
        coerce the given value to be storable in the current type
        """
        if self.builtin_type == self.builtin_types.Date and type(value) == str:
            dt = parse_date.parse_date(value)
            return dt
            
        for target in self.py_types[self.builtin_type]:
            convert = None
            try:
                convert = target(value)
            except:
                pass
            if convert is not None:
                return convert
        return None

    @staticmethod
    def init_all():
        for bi in BuiltIn.builtin_types:
            globals()[bi] = BuiltIn(BuiltIn.builtin_types(bi))
        
    def add_prop(self, name):
        raise Exception("Can't add properties to builtin types")


class Property(object):
    """
    Properties definitions contain:
    
    - type (entity)
    - tag (name) - optional
    - cardinality (min and max values allowed)
    """
    def __init__(self, entity, tag=None, cd=card.many_one, default=None):
        self.entity = entity
        self.tag = tag
        self.card = cd
        self.default = default
        
    def name(self):
        return self.tag or self.entity.name
    
class Relation(object):
    """
    A description of a (bi-directional) relationship between two Entities
    """
    def __init__(self, entityL, entityR, cd=card.many_many, tagL=None, tagR=None):
        self.entityL = entityL
        self.entityR = entityR
        self.card = cd
        self.tagL = tagL
        self.tagR = tagR
        
    def name_from(self, entity):
        if entity is self.entityL:
            return self.tagL or self.entityR.name
        if entity is self.entityR:
            return self.tagR or self.entityR.name
        raise "%s is not a member of the %s-%s Relation" % (entity.name, self.entityL.name, self.entityR.name)
    
    def get_props(self):
        return (Property(self.entityR, self.tagL, self.card),
                Property(self.entityL, self.tagR, card_inverse[self.card]))
        
class Instance(object):
    """
    An instance of an Entity definition.
    
    instance.x - get the value of the property defined to an x type (or tagged x)
    """
    def __init__(self, entity):
        self.__dict__['_entity'] = entity
        self.__dict__['_mValues'] = {}
        
    def __getattr__(self, prop_name):
        if prop_name not in self._mValues:
            return None
        return self._mValues[prop_name]
    
    def __setattr__(self, prop_name, value):
        if value is None:
            if prop_name in self._mValues:
                del self._mValues[prop_name]
            return
        
        prop = self._entity.get_prop(prop_name)
        if prop is None:
            raise Exception("No such property: %s" % prop_name)
        
        target_entity = prop.entity
        save_value = target_entity.coerce_value(value)
        if save_value is None:
            raise Exception("Can't save a value of type %s into a property of type %s" % (type(value), target_entity.name))
        
        self._mValues[prop_name] = save_value
        
    def JSON(self):
        json = {'id': id(self),
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
    
    code2.interact("", globals=globals(), local=Entity.all_entities())
    
if __name__ == '__main__':
    interactive()
