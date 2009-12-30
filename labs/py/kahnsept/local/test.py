from kahnsept import *
from parse_date import *

import unittest
import datetime

class TestDateParse(unittest.TestCase):
    def test_dates(self):
        for test in ['01/01/09', '1/1/09', '1/1/2009', 'Jan 1, 09', 'Jan 1, 2009', 'January 1, 2009',
                     '2009-01-01', '1.1.09']:
            dt = parse_date(test)
            self.assertNotEqual(dt, None, test)
            if dt is not None:
                self.assertEqual(dt.date(), datetime.date(2009,1,1), test)
                
    def test_times(self):
        for test in ['1/1/09 13:17', '1/1/09 1:17 pm']:
            dt = parse_date(test)
            self.assertNotEqual(dt, None, test)
            if dt is not None:
                self.assertEqual(dt, datetime.datetime(2009,1,1,13,17))

class TestBasics(unittest.TestCase):
    def test_entity(self):
        e = Entity('Test')
        self.assertEqual(e.name, 'Test')
        
        e2 = Entity('Test')
        self.assert_(e is e2)
        
    def test_property(self):
        e = Entity('Test')
        p = Property(e)
        self.assertEqual(p.card, card.multiple)
        
        p = Property(e, 'fred')
        self.assertEqual(p.tag, 'fred')
        
        e.add_prop(p)
        self.assertNotEqual(e.get_prop('fred'), None)
        
    def test_instance(self):
        e = Entity('Test')
        p = Property(e)
        e.add_prop(p)
        i = e.new()
        
        self.assertEqual(i._entity, e)
        
class TestBuiltins(unittest.TestCase):
    def test_builtin(self):
        e = Entity('Test')
        e.add_prop(Property(Number))
        e.add_prop(Property(Text))
        e.add_prop(Property(Boolean))
        e.add_prop(Property(Date))
        
        e.Number = 1
        self.assertEqual(e.Number, 1)
        
        e.Text = "hello"
        self.assertEqual(e.Text, "hello")
        
        e.Boolean = True
        self.assertEqual(e.Boolean, True)
        
        e.Date = now = datetime.datetime.now()
        self.assertEqual(e.Date, now)
        
class TestCoercion(unittest.TestCase):
    def test_pass(self):
        e = Entity('Test')
        e.add_prop(Property(Number))
        e.add_prop(Property(Text))
        e.add_prop(Property(Boolean))
        e.add_prop(Property(Date))
        e.add_prop(Property(e, 'parent'))
        
        i = e.new()
        i2 = e.new()
        i.Number = "7"
        i.Text = 1
        i.Boolean = 1
        i.Date = "1/1/2009"
        i.parent = i2
        self.assertEqual(i.Number, 7)
        self.assertEqual(i.Text, "1")
        self.assertEqual(i.Boolean, True)
        self.assertEqual(i.Date.date(), datetime.date(2009,1,1))
        self.assertEqual(i.parent, i2)
        
    def test_fail(self):
        e = Entity('Test')
        e.add_prop(Property(Number))
        i = e.new()
        
        def throws():
            i.Number = "a"
            
        self.assertRaises(Exception, throws)


if __name__ == '__main__':
    unittest.main()