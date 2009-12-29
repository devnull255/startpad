import kahnsept

import unittest

class TestKahnsept(unittest.TestCase):
    def test_entity(self):
        e = kahnsept.Entity('Test')
        self.assertEqual(e.name, 'Test')
        
    def test_property(self):
        e = kahnsept.Entity('Test')
        p = kahnsept.Property(e)
        self.assertEqual(p.arity, kahnsept.arity.single)

if __name__ == '__main__':
    unittest.main()