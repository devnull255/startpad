"""
Models for Theta-Chi sample application.

We are striving to ultimately be able to generate an application like this sample
purely by interpreting the application description language.

Committee
Brother
Position
Duty
Task
Term (just use a string)

"""
from google.appengine.ext import db

import logging
import util

import settings
import reqfilter
import mixins

class Brother(db.Model):
    phone = db.StringProperty()
    address = db.TextProperty()
    email = db.StringProperty()
    # Position_set
    # Tasks_owner
    # Tasks_supervisor

class Position(db.Model):
    term = db.StringProperty()
    brother = db.ReferenceProperty(Brother)
    # Duties_owner
    # Duties_supervisor
    
class Committee(db.Model):
    chair = db.ReferenceProperty(Position)
    members = db.ListProperty(db.Key) # Position
    # Duty_set

class Duty(db.Model):
    owner = db.ReferenceProperty(Position, collection_name="Duties_owner")
    supervisor = db.ReferenceProperty(Position, collection_name="Duties_supervisor")
    committee = db.ReferenceProperty(Committee)
    no_of_bothers = db.IntegerProperty()
    # Task_set
  
class Task(db.Model):
    owner = db.ReferenceProperty(Brother, collection_name="Tasks_owner")
    supervisor = db.ReferenceProperty(Brother, collection_name="Tasks_supervisor")
    assigned_to = db.ListProperty(db.Key) # Brother
    duty = db.ReferenceProperty(Duty)
    due_date = db.DateProperty()
    budget = db.FloatProperty()
    prior_task = db.ReferenceProperty() # Key
"""
"""   