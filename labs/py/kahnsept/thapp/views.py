
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseForbidden
from django import shortcuts
from google.appengine.ext import db
import logging
import random
import cgi
import simplejson

import util
import reqfilter
import models

def build_sample(req):
    committee = models.Committee()
    committee.put()
    return reqfilter.RenderResponse('sample.html', {'committee':committee})