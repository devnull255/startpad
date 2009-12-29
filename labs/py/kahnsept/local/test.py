import kahnsept

import unittest

class TestKahnsept(unittest.TestCase):
    def test_entity(self):
        e = kahnsept.Entity('Test')
        self.assertEqual(e.name, 'Test')
        
    def test_property(self):
        e = kahnsept.Entity('Test')
        p = kahnsept.Property(e)
        self.assertEqual(p.card, kahnsept.card.single)
        
        p = kahnsept.Property(e, 'fred')
        self.assertEqual(p.tag, 'fred')
        
        e.add_prop(p)
        self.assertEqual(len(e._props), 1)
        
    def test_entity(self):
        e = kahnsept.Entity('Test')
        p = kahnsept.Property(e)
        e.add_prop(p)
        i = e.new()
        
        self.assertEqual(i._entity, e)

if __name__ == '__main__':
    unittest.main()