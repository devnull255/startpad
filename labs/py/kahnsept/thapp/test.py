import logging
import sys
import os
import random
import unittest
import StringIO

from django.http import HttpResponse
from google.appengine.ext import db

import settings
import reqfilter
import mixins
import models
import reqfilter
import timescore

def assert_classes(test_case, instance, classes):
    test_case.assertTrue(instance is not None)
    for cls in classes:
        test_case.assertTrue(isinstance(instance, cls))
        
def assert_scores(test_case, scores):
    test_case.assert_(len(scores) == 4)
    for name, value in scores.items():
        test_case.assert_(type(name) == str)
        test_case.assert_(type(value) == float)

class TestCommunity(unittest.TestCase):
    """
    Unit tests for the Community Model
    
    Also tests timescore used in Community
    """
    
    def is_community(self, c):
        assert_classes(self, c, [db.Model,
                                 models.Community,
                                 mixins.Migratable])

    def test_creation(self):
        name = 'test-community-%04d' % random.randint(0,10000)
        c1 = models.Community.create(name)
        self.is_community(c1)
        c2 = models.Community.find(name)
        self.is_community(c2)
        self.assertEqual(c2.schema, models.Community.schema_current)
        
    def test_defaults(self):
        self.assert_(len(settings.DEFAULT_COMMUNITIES) > 1)
        for s in settings.DEFAULT_COMMUNITIES:
            c = models.Community.find(s)
            self.is_community(c)
            
class TestLink(unittest.TestCase):
    """
    Unit tests for the Link Model
    """
    
    def is_link(self, l):
        assert_classes(self, l, [db.Model,
                                 models.Link,
                                 mixins.Migratable,
                                 mixins.Moderatable])
        self.assert_(type(l.TS_hrs) == float)
        
    def setUp(self):
        self.general = models.Community.find('general')
        self.l = self.random_link()
        
    def random_link(self, seed="startpad.org", tag=None):
        link_info = {'url':"http://%s/%04d" % (seed, random.randint(0,10000))}
        if tag is not None:
            link_info['tags'] = [tag]
        return models.Link.register_link_info(self.general, dict(link_info))
    
    def test_creation(self):
        self.is_link(self.l)
        scores = self.l.named_scores()
        for score,value in scores.items():
            self.assertAlmostEqual(value, 10.0, 2)
        
        link_info = {}
        link_info['url'] = "http://startpad.org/%04d" % random.randint(0,10000)
        link_info['title'] = "This is a sample title"
        link_info['tags'] = ['tag-1', 'tag-2', 'tag 3', ' ', '  tag    .1 .. ']
        l = models.Link.register_link_info(self.general, dict(link_info))
        self.is_link(l)
        
        self.assert_(len(l.tags) == 3)
        
        for tag in l.tags:
            logging.info("tag: %s" % tag)
            self.assert_(' ' not in tag)
        
        link_info['title'] = u"   A new title  "    
        link_info['tags'] = ['a new tag', 'fucker', 'little cunt']
        l = models.Link.register_link_info(self.general, dict(link_info))
        logging.info("title: %s" % l.title)
        self.assert_(l.title == "A new title")
        self.assert_(len(l.tags) == 4)
        
    def test_scores(self):
        self.assert_(type(self.l.TS_day_score) == float)
        self.assert_(type(self.l.TS_week_score) == float)
        self.assert_(type(self.l.TS_month_score) == float)
        self.assert_(type(self.l.TS_year_score) == float)
        
    def test_named_scores(self):
        scores = self.l.named_scores()
        assert_scores(self, scores)

    def test_score_update(self):
        scores1 = self.l.named_scores()
        assert_scores(self, scores1)
        self.l.update_scores(1)
        scores2 = self.l.named_scores()
        assert_scores(self, scores2)
        
        for name in scores1:
            self.assertAlmostEqual(scores1[name]+1, scores2[name])
            
    def test_deferred_writes(self):
        count_writes = 0
        for i in range(100):
            self.l.update_scores(1)
            self.l.deferred_put()
            if self.l._cache_state == self.l.cache_state.clean:
                count_writes += 1
                
        logging.info("count_writes: %d" % count_writes)
        self.assert_(count_writes >= 30 and count_writes <= 35)
        
    def test_deferred_scores(self):
        links = []
        tag = "defer-%04d" % random.randint(0, 10000)
        for i in range(10):
            links.append(self.random_link("defer_test.com", tag))
            for j in range(0,i+1):
                links[j].update_scores(1)
        
        mixins.write_deferred_cache()
        
        query = models.Link.all().filter("tags =", tag) 
        best = timescore.order_by_score(query, timescore.hrsDay).fetch(10)
        self.assert_(len(best) == 10)
        for i in range(10):
            logging.info("b: %s l: %s" % (best[i].key().name(), links[i].key().name()))
                         
        for i in range(10):
            self.assert_(best[i].key() == links[i].key())
            self.assert_(best[i] is not links[i])

        
class TestSite(unittest.TestCase):
    """
    Unit tests for the Site Model
    """
    def is_site(self, s):
        assert_classes(self, s, [db.Model,
                                 models.Site,
                                 mixins.Migratable,
                                 mixins.Moderatable])
        
    def test_creation(self):
        general = models.Community.find('general')
        site = models.Site.register_domain(general, 'www.foo.com')
        self.is_site(site)
        
        site2 = models.Site.register_domain(general, 'foo.com')
        self.is_site(site2)
        self.assert_(site2.domain == 'www.foo.com') 
        
class TestTag(unittest.TestCase):
    """
    Unit tests for the Tag Model
    """
    
    def is_tag(self, t):
        assert_classes(self, t, [db.Model,
                                 models.Tag,
                                 mixins.Migratable,
                                 mixins.Moderatable])
        self.assert_(type(t.TS_hrs) == float)
        
    def test_creation(self):
        general = models.Community.find('general')
        t = models.Tag.register_tag(general, 'shit')
        self.assert_(t is None)
        
        t = models.Tag.register_tag(general, 'technology')
        self.is_tag(t)
        
    def test_alias(self):
        general = models.Community.find('general')
        t = models.Tag.register_tag(general, 'technology')
        t.make_alias('tech')
        
        t2 = models.Tag.register_tag(general, 'tech')
        self.assert_(t2.canonical == 'technology')
        
@reqfilter.admin_only
def run_tests(req, *args, **kwargs):
    """
    Run all the tests in this module and send the output to the web browser
    as a text file
    """
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    results = StringIO.StringIO()
    unittest.TextTestRunner(stream=results).run(suite)
    return HttpResponse(results.getvalue(), mimetype="text")

