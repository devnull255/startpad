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
Card = enum('one',
            'many',
            'one_one',   # 1:1 - matched (e.g. spouse)
            'one_many',  # 1:* - partition (e.g., children)
            'many_one',  # *:1 - reference (e.g., father)
            'many_many', # *:* - multi-set (e.g., siblings)
            many_one=0,  # synonym for 'one'
            many_many=1 # synonym for 'many'
            )

card_inverse = (Card.one_many, Card.many_many, Card.one_one, Card.many_one)

def key_summary(map, max=5):
    sum = map.keys()[0:max]
    if len(map) > max:
        sum.append("and %d others." % max - len(map))
    return ", ".join(sum)

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
        
    def __repr__(self):
        return "Entity('%s') - Props: %s" % (self.name, key_summary(self._mProps))
    
    @classmethod    
    def all_entities(cls):
        return cls._mEntities
        
    def add_prop(self, entity, tag=None, card=None, default=None):
        """
        Add a new property or Relation to the Entity.  We require that all properties be uniquely identifiable:
        if two properties of the same type exist, they must BOTH be tagged.
        """
        if isinstance(entity, BuiltIn):
            if card is None:
                card = Card.one
            prop = Property(entity, tag, card, default)
            self._add_prop(prop)
            return prop
        
        # Define a Relation with another Entity
        if card is None:
            card = Card.many_many
        rel = Relation(self, entity, cardL=card, tagL=tag)

        return rel
        
    def _add_prop(self, prop):
        name = prop.name()
        if self.get_prop(name):
            raise Exception("Duplicate property name: %s" % prop.name)
        self._mProps[name] = prop
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
    def __init__(self, entity, tag=None, card=Card.many_one, default=None, relation=None, side=None):
        self.entity = entity
        self.tag = tag
        self.card = card
        self.default = default
        self.relation = relation
        self.side = side
        
    def __repr__(self):
        return "Property('%s')->%s (%s)" % (self.name(), self.entity.name, "many" if self.is_multi() else "1")
        
    def name(self):
        return self.tag or self.entity.name
    
    def is_multi(self):
        return self.card in (Card.one_many, Card.many_many)
    
    def related_value(self, instance):
        if self.relation is None or not isinstance(instance, Instance):
            return None
        return instance._get_value(self.relation.names[1-self.side])

class Relation(object):
    """
    A description of a (bi-directional) relationship between two Entities
    """
    def __init__(self, entityL, entityR, cardL=Card.many_many, tagL=None, tagR=None):
        self.entities = (entityL, entityR)
        self.tags = (tagL, tagR)
        
        self.names = [self.tags[side] or self.entities[1-side].name for side in range(2)]
        self.cards = [cardL, card_inverse[cardL]]
        self.props = [Property(self.entities[1-side], self.names[side], self.cards[side], relation=self, side=side) \
                      for side in range(2)]
        
        if entityL == entityR and self.names[0] == self.names[1]:
            raise Exception("Self-Relations MUST have distinct tag names (%s != %s)" % self.names)
        
        # Add both (or neither) properties to each entity - atomically
        pL = None
        try:
            pL = entityL._add_prop(self.props[0])
            entityR._add_prop(self.props[1])
        except Exception, e:
            if pL is not None:
                entityL.del_prop(pL)
            raise e
        
    def __repr__(self):
        return "Relation: %r ~ %r" % (self.props[0], self.props[1])
        
class Instance(object):
    """
    An instance of an Entity definition.
    
    instance.x - get the value of the property defined to an x type (or tagged x)
    """
    def __init__(self, entity):
        self.__dict__['_entity'] = entity
        self.__dict__['_mValues'] = {}
        
    def __repr__(self):
        return "%s<%X>: Values: %s" % (self._entity.name, id(self), key_summary(self._mValues))
        
    def _get_value(self, prop_name):
        return self._ensure_value(prop_name)
        
    def __getattr__(self, prop_name):
        return self._ensure_value(prop_name).get()
    
    def __setattr__(self, prop_name, value):
        self._ensure_value(prop_name).set(value)
        
    def _ensure_value(self, prop_name):
        value = self._mValues.get(prop_name, None)
        if value is None:
            prop = self._entity.get_prop(prop_name)
            if prop is None:
                raise Exception("No property '%s' in %s" % (prop_name, self._entity.name))
            value = Value(prop, self)
            self._mValues[prop_name] = value
        return value

    def JSON(self):
        json = {'id': id(self),
                'type': self._entity}
        json.update(self._mValues)
        return json
    
class Value(object):
    """
    A value can hold 1 or more values for an instance property.  It's behavior is driven
    by it's corresponding Property definition.
    
    TODO: Pretty storage inefficient to store instance pointers in every value!
    """
    def __init__(self, prop, instance):
        self.prop = prop
        self.instance = instance
        
        assert(prop is not None and instance is not None)

        self.values = []
        self.value = None
        
    def __len__(self):
        if self.prop.is_multi():
            return len(self.values)
        return 0 if self.value is None else 1
    
    def __getitem__(self, index):
        return self.values[index]
    
    def __contains__(self, value):
        if self.prop.is_multi():
            return value in self.values
        return value == self.value
        
    def set(self, value):
        save_value = self.prop.entity.coerce_value(value)

        if save_value is None and value is not None:
            if isinstance(value, Instance):
                type_name = value._entity.name
            else:
                type_name = str(type(value))
            raise Exception("Can't save a value of type %s into a property of type %s" % (type_name, self.prop.entity.name))
        
        # If value is already here, there is nothing to do
        if self._has_value(save_value):
            return save_value
        
        # May need to set our own as well as the other side of the relation's value
        valueOther = self.prop.related_value(save_value)
        if valueOther is not None:
            valueOther._set(self.instance)
        self._set(save_value)
        return save_value
    
    def add(self, value):
        return self.set(value)
    
    def get(self):
        if self.prop.is_multi():
            return self
        else:
            return self.value
    
    def remove(self, value):
        if not self._has_value(value):
            return
        
        valueOther = self.prop.related_value(value)
        if valueOther is not None:
            valueOther._remove(self.instance)
        self._remove(value)
        
    def _set(self, value):
        if self.prop.is_multi(): 
            self.values.append(value)
        else:
            self.remove(self.value)
            self.value = value
               
    def _remove(self, value):
        if self.prop.is_multi():
            self.values.remove(value)
        else:
            self.value = None
        
    def _has_value(self, value):
        if value is None:
            return True

        if self.prop.is_multi():
            return value in self.values
        
        return value == self.value
    
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
