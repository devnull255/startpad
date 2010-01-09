from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

import reqfilter
import jscomposer
import views

urlpatterns = []
urlpatterns.extend(reqfilter.json_urls())

urlpatterns.extend(patterns('',
    (r'^$', direct_to_template, {'template':'home.html'}),
    
    (r'^build-sample$', views.build_sample),
    
    (jscomposer.ScriptPattern(), jscomposer.ScriptFile),
    
    (r'^unit-tests$', 'test.run_tests'),
))
