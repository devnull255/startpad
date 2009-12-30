import kahnsept

import unittest
import datetime

class TestBasics(unittest.TestCase):
    def test_entity(self):
        e = kahnsept.Entity('Test')
        self.assertEqual(e.name, 'Test')
        
        e2 = kahnsept.Entity('Test')
        self.assert_(e is e2)
        
    def test_property(self):
        e = kahnsept.Entity('Test')
        p = kahnsept.Property(e)
        self.assertEqual(p.card, kahnsept.card.multiple)
        
        p = kahnsept.Property(e, 'fred')
        self.assertEqual(p.tag, 'fred')
        
        e.add_prop(p)
        self.assertEqual(len(e._props), 1)
        
    def test_instance(self):
        e = kahnsept.Entity('Test')
        p = kahnsept.Property(e)
        e.add_prop(p)
        i = e.new()
        
        self.assertEqual(i._entity, e)
        
class TestBuiltins(unittest.TestCase):
    def test_builtin(self):
        e = kahnsept.Entity('Test')
        e.add_prop(kahnsept.Number)
        e.add_prop(kahnsept.Text)
        e.add_prop(kahnsept.Boolean)
        e.add_prop(kahnsept.Date)
        
        e.Number = 1
        self.assertEqual(e.Number, 1)
        
        e.Text = "hello"
        self.assertEqual(e.Text, "hello")
        
        e.Boolean = True
        self.assertEqual(e.Boolean, True)
        
        e.Date = now = datetime.datetime.now()
        self.assertEqual(e.Date, now)

if __name__ == '__main__':
    unittest.main()