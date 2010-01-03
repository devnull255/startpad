"""
Kahnsept - Entity/Relationship system

"""

import datetime
import simplejson as json

from enum import *
import parse_date
import pickle

import dyn_dict

local_cache = "kahnsept.bin"

TRACE = True

__all__ = ['Card', 'World', 'Entity', 'Property', 'Relation', 'Instance']

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

def key_summary(map, limit=7):
    sum = map.keys()[0:limit]
    if len(map) > limit:
        sum.append("and %d others." % (len(map) - limit))
    return ", ".join(sum)

class World(object):
    """
    All Kahnsept objects are stored relative to a give World.
    """
    current = None
    scope = dyn_dict.DynDict()
    
    def __init__(self):
        # Keep a shadow copy of created Entities in the entity_map (e.g., globals())
        self.entities = {}
        self.relations = []
        self.make_current(self)
        BuiltIn.init_all()
        
    def __repr__(self):
        return "World - Entities: %s" % key_summary(self.entities, 15)
    
    def _register_entity(self, entity):
        self.entities[entity.name] = entity
        
        # Make entities available as attributes of the World object
        setattr(self, entity.name, entity)
    
    @classmethod    
    def make_current(cls, world):
        if cls.current == world:
            return
        if cls.current is not None:
            cls.scope.remove_dict(cls.current.entities)
        cls.current = world
        cls.scope.add_dict(world.entities)
        
    def save_json(self, file_name="kahnsept"):
        """
        Save Schema and Data in JSON format in this order:
        
        - Entities (names) - with non-relation properties
        - Relationships
        - Instances
        """
        file = open("%s.json" % file_name, 'w')
        try:
            js = {}

            ent_map = {}
            for (name, ent) in self.entities.items():
                if isinstance(ent, BuiltIn):
                    continue
                ent_map[name] = ent
            if len(ent_map) > 0:
                js['entities'] = ent_map

            if len(self.relations) > 0:
                js['relations'] = self.relations

            inst = []
            for ent in self.entities.values():
                if isinstance(ent, BuiltIn):
                    continue
                if len(ent.all()) > 0:
                    inst.extend(ent.all())
            if len(inst) > 0:
                js['instances'] = inst

            json.dump(json.JSONFunction('Kahnsept', js),
                       file, cls=JSONEncoder, indent=4, check_circular=False)
        finally:
            file.close()
            
    def save(self, file_name="kahnsept"):
        file = open("%s.kpt" % file_name, 'w')
        pickle.dump(self, file)
        file.close()
    
    @classmethod    
    def load(cls, file_name="kahnsept"):
        file = open("%s.kpt" % file_name)
        world = pickle.load(file)
        file.close
        cls.make_current(world)
        return world

class Entity(object):
    """
    Entities are the definitions of all Instances in Kahnsept.
    
    They are collections of Properties.
    """
    def __new__(cls, name, world=None):
        if world is None:
            world = World.current

        """
        Share instances of Entity for a given name
        """
        assert(type(name) == str)
        
        # world.entities is not initialized on un-pickling
        if hasattr(world, 'entities') and name in world.entities:
            return world.entities[name]
        e = super(Entity, cls).__new__(cls)
        
        return e
    
    def __getnewargs__(self):
        """ for pickling """
        return (self.name, self.world)

    def __init__(self, name, world=None):
        if hasattr(self, 'inited'):
            return
        self.inited = True

        if world is None:
            world = World.current
            
        assert(type(name) == str)

        self.name = name
        self.world = world
        self._mProps = {}
        self.idMax = 0
        self.instance_map = {}

        world._register_entity(self)
        
    def __repr__(self):
        return "Entity('%s') - Props: %s" % (self.name, key_summary(self._mProps))
    
    def JSON(self, json_context):
        """ return a JSON serializable structure """
        if json_context.full_json(self) and len(self._mProps) != 0:
            js = {}
            props = {}
            for (name, prop) in self._mProps.items():
                if prop.relation is None:
                    props[name] = prop
            if len(props) > 0:
                js['properties'] = props
            return js
        else:
            return self.name            
    
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
        
    def del_prop(self, name):
        if name in self._mProps:
            del self._mProps[name]

    def get_prop(self, name):
        if name is None:
            return None
        return self._mProps.get(name, None)
            
    def new(self):
        """
        Return an instance of this Entity type
        """
        self.idMax += 1
        i = Instance(self, self.idMax)
        self.instance_map[self.idMax] = i
        return i
    
    def all(self):
        return self.instance_map.values()
    
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
        js = {'type':self.entity.name}
        if self.is_multi():
            js['multi'] = True
        if self.default is not None:
            js['default'] = self.default
        return js
        
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
    def __init__(self, entityL, entityR, card=Card.many_many, tagL=None, tagR=None, world=None):
        if world is None:
            world = World.current

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
        
        world.relations.append(self)
        
    def __repr__(self):
        return "Relation: %r <=> %r" % (self.props[0], self.props[1])
    
    def JSON(self, json_context):
        """ Relation({"left":{"entity":<name>, "name":<name>},
                      "right":{"entity":<name>},
                      "card":<type>)
        """
        js = {'left':{'entity':self.entities[0].name},
              'right':{'entity':self.entities[1].name},
              'card': Card(self.cards[0])}
        for side in range(2):
            if self.names[side] != self.entities[1-side].name:
                js['right' if side else 'left']['name'] = self.names[side]
        return json.JSONFunction('Relation', js)
        
class Instance(object):
    """
    An instance of an Entity definition.
    
    instance.x - get the value of the property defined to an x type (or tagged x)
    """
    def __init__(self, entity, id):
        self.__dict__['_entity'] = entity
        self.__dict__['_id'] = id
        self.__dict__['_mValues'] = {}
        
    def __getstate__(self):
        return self.__dict__;
    
    def __setstate__(self, d):
        for (key,value) in d.items():
            self.__dict__[key] = value
        
    def __repr__(self):
        return "%s<%X>: Values: %s" % (self._entity.name, self._id, key_summary(self._mValues))
        
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
                raise AttributeError
            value = Value(prop, self)
            self._mValues[prop_name] = value
        return value

    def JSON(self, json_context):
        if json_context.full_json(self):
            def free_instances():
                json_context.full_instances = True
            json_context.full_instances = False
                
            return json.JSONFunction(self._entity.name, self._id, self._mValues).set_callback(free_instances)
        else:
            return json.JSONFunction(self._entity.name, self._id)
    
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
    
    def JSON(self, json_context):
        if self.prop.is_multi():
            return self.values
        else:
            return self.value
        
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
            self.full_instances = True
            
        @staticmethod
        def uid(obj):
            return id(obj)
            
        def full_json(self, obj):
            if isinstance(obj, Instance) and not self.full_instances:
                return False
            
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

def dict_nonnull(d):
    return dict([(key,value) for (key,value) in d.items() if value is not None])
