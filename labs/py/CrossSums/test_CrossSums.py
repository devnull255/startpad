import unittest
import CrossSums as CS

class CrossSumsTest(unittest.TestCase):

    def Example(self):
        self.cs = CS.CrossSum()

        # Integers denote number of skipped cells.
        # Tuples are sums followed by number of cells in sum
        self.cs.RowSums(((2,(16,2),(3,2),(13,2),(5,2)),
                    (1,(16,3),(4,2),(7,2),(17,2)),
                    ((3,2),(10,2),(12,3),1,(14,2)),
                    ((8,2),1,(10,2),(17,2),(14,2)),
                    (1,(16,2),1,(6,3),(9,2)),
                    (1,(10,2),1,(7,2),(28,5)),
                    ((4,2),1,(31,5),1,(3,2)),
                    ((27,5),(15,2),1,(3,2)),
                    (2,(12,2),(13,3),1,(3,2)),
                    (1,(3,2),(17,2),(4,2),1,(7,2)),
                    ((16,2),1,(9,3),(9,2),(17,2)),
                    ((9,2),(9,2),(5,2),(13,3)),
                    ((10,2),(15,2),(12,2),(6,2))))

        self.cs.ColSums(((2,(4,2),1,(10,2),1,(11,3)),
                    (1,(35,7),(26,4)),
                    ((15,2),1,(11,2),(6,3)),
                    ((21,3),3,(12,2),1,(8,2)),
                    (2,(12,2),1,(9,2),(29,4)),
                    ((4,2),(17,4),(18,3)),
                    ((11,3),(24,5),(15,3)),
                    (2,(11,3),(14,4),(5,2)),
                    ((17,4),(12,2),1,(3,2)),
                    ((15,2),1,(4,2),3,(11,3)),
                    (3,(22,3),(11,2),1,(6,2)),
                    ((25,4),(38,7)),
                    ((20,3),1,(8,2),1,(10,2))))

    def testCsumsCount(self):
        cs1 = CS.CrossSum()
        self.assertEqual(len(cs1.csums), 0)
        

    def textExample(self):
        self.Example()
        self.assertEqual(len(self.cs.csums), 84)
        self.cs.DumpSums()

if __name__=='__main__':
    unittest.main()
