"""
Kahnsept - Entity/Relationship system

"""

import datetime
import simplejson as json

from enum import *
import parse_date
import interactive
import pickle

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

class World(object):
    """
    All Kahnsept objects are stored relative to a give World.
    """
    current_world = None
    
    def __init__(self, entity_map=None):
        if entity_map is None:
            entity_map = {}
        self.entities = entity_map
        self.instances = []
        World.current_world = self 

        BuiltIn.init_all()
        
    def save_json(self, file_name="kahnsept"):
        file = open("%s.json" % file_name, 'w')
        try:
            json.dump(json.JSONFunction('Kahnsept', {'entities':self.entities, 'instances':self.instances}),
                       file, cls=JSONEncoder, indent=4)
        finally:
            file.close()
            
    def save(self, file_name="kahnsept"):
        file = open("%s.bin" % file_name, 'w')
        pickle.dump(self, file, 2)
        file.close()
        
    def load(self):
        pass

class Entity(object):
    """
    Entities are the definitions of all Instances in Kahnsept.
    
    They are collections of Properties.
    """
    def __new__(cls, name, world=None):
        if world is None:
            world = World.current_world

        """
        Share instances of Entity for a given name
        """
        assert(type(name) == str)
        if name in world.entities:
            return world.entities[name]
        e = super(Entity, cls).__new__(cls)
        
        return e

    def __init__(self, name, world=None):
        if world is None:
            world = World.current_world
            
        assert(type(name) == str)

        self.name = name
        self.world = world
        self._mProps = {}
        world.entities[name] = self
        
    def __repr__(self):
        return "Entity('%s') - Props: %s" % (self.name, key_summary(self._mProps))
    
    def JSON(self, json_context):
        """ return a JSON serializable structure """
        if json_context.first_visit(self):
            return json.JSONFunction('Entity', self.name, self._mProps)
        else:
            return json.JSONFunction('Entity', self.name)            
    
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
        rel = Relation(self, entity, card=card, tagL=tag)

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

    def __init__(self, name, world=None):
        self.builtin_type = self.builtin_types(name)
        super(BuiltIn, self).__init__(name, world)        

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
            BuiltIn(bi)
        
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
    
    def JSON(self, json_context):
        return json.JSONFunction('Property', dict_nonnull(self.__dict__))
        
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
    def __init__(self, entityL, entityR, card=Card.many_many, tagL=None, tagR=None):
        self.entities = (entityL, entityR)
        self.tags = (tagL, tagR)
        
        self.names = [self.tags[side] or self.entities[1-side].name for side in range(2)]
        self.cards = [card, card_inverse[card]]
        self.props = [Property(self.entities[1-side], self.names[side], self.cards[side], relation=self, side=side) \
                      for side in range(2)]
        
        if entityL == entityR and self.names[0] == self.names[1]:
            raise Exception("Self-Relations MUST have distinct tag names (%s != %s)" % tuple(self.names))
        
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
    
    def JSON(self, json_context):
        return json_context.JSONFunctionObject('Relation', self.__dict__)
        
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
        assert(self.prop.is_multi());
        return len(self.values)
    
    def __getitem__(self, index):
        assert(self.prop.is_multi());
        return self.values[index]
    
    def __contains__(self, value):
        assert(self.prop.is_multi());
        return value in self.values
        
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
    
class JSONEncoder(json.JSONEncoder):
    """
    Handle networks of object via depth-first pre-order traversal.
    
    Keep track of visited state and pass in context object to determine
    when an object is first visited.  Later visits can dump out an
    abbreviated object reference instead of the complete object. 
    """
    class JSONContext():
        def __init__(self):
            self.visited = set()
            
        @staticmethod
        def uid(obj):
            return id(obj)
            
        def first_visit(self, obj):
            key = self.uid(obj)
            f = key not in self.visited
            self.visited.add(key)
            return f
    
    def __init__(self, **kw):
        self.context = self.JSONContext()
        super(JSONEncoder, self).__init__(**kw)

    def default(self, obj):
        if hasattr(obj, 'JSON'):
            return obj.JSON(self.context)
        return super(JSONEncoder, self).default(obj)
    
class InteractiveEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Entity, Property, Relation, Instance)):
            return json.JSONString(repr(obj))
        return super(InteractiveEncoder, self).default(obj)
    
def dict_nonnull(d):
    return dict([(key,value) for (key,value) in d.items() if value is not None])

if __name__ == '__main__':
    world = World()
    interactive.interactive(ext_map=globals(), locals=world.entities, encoder=InteractiveEncoder)
