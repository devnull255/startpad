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
        self.assertEqual(p.card, kahnsept.card.single)
        
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
        num = kahnsept.Entity('number')
        text = kahnsept.Entity('text')
        bool = kahnsept.Entity('boolean')
        date = kahnsept.Entity('date')
        
        e = kahnsept.Entity('Test')
        e.add_prop(num)
        e.add_prop(text)
        e.add_prop(bool)
        e.add_prop(date)
        
        e.num = 1
        self.assertEqual(e.num, 1)
        
        e.text = "hello"
        self.assertEqual(e.text, "hello")
        
        e.bool = True
        self.assertEqual(e.bool, True)
        
        e.date = now = datetime.datetime.now()
        self.assertEqual(e.date, now)

if __name__ == '__main__':
    unittest.main()