import math

class LetterSquareSolver():
    """ Find all words that are present in a square array of characters. """
    
    def __init__(self, sInit):
        """ Initialize the board characters - assumed square.
        .dim - size of each dimension
        .board[][] - array of characters
        .mp{ch}[] - position(s) of each letter in the square
        """
        
        self.dim = int(math.sqrt(len(sInit)))
        if self.dim < 2:
            raise Exception("Letter Square must be 2x2 or larger.")
        if len(sInit) != self.dim*self.dim:
            raise Exception("Non-square Letter Square")

        self.board = [[sInit[row*self.dim + col] for col in range(self.dim)] for row in range(self.dim)]
        self.mp = {}

        # Build array of positions for each letter in the square (can be duplicate characters)
        for row in range(self.dim):
            for col in range(self.dim):
                ch = self.board[row][col]
                if not self.mp.get(ch):
                    self.mp[ch] = []
                self.mp[ch].append((row,col))

    def FindWords(self, dict, fRepeats=True):
        words = []
        for word in dict:
            word = word.strip()
            if self.InSquare(word, fRepeats):
                words.append(word)
        words.sort(lambda x,y: len(y)-len(x))
        return words

    def InSquare(self, word, fRepeats):
        starts = self.mp.get(word[0])
        if starts is None:
            return False

        # Keep track of the paths of each starting point
        paths = []
        for start in starts:
            path = set()
            path.add(start)
            paths.append(path)

        # Find a feasible path from the current start through the rest of the word
        for ch in word[1:]:
            # Parallel arrays keep track of the current position AND all used squares
            # so far in the paths we are exploring
            startsNext = []
            pathsNext = []
            for i in range(len(paths)):
                start = starts[i]
                path = paths[i]
                
                row = start[0]
                col = start[1]

                rowMin = max(0, row-1)
                rowMax = min(self.dim-1, row+1)
                colMin = max(0, col-1)
                colMax = min(self.dim-1, col+1)
                    
                for rowT in range(rowMin, rowMax+1):
                    for colT in range(colMin, colMax+1):
                        if rowT == row and colT == col:
                            continue
                        if self.board[rowT][colT] == ch:
                            if not fRepeats and (rowT, colT) in path:
                                continue
                            startsNext.append((rowT, colT))
                            path.add((rowT, colT))
                            pathsNext.append(path)

            if len(startsNext) == 0:
                return False
            starts = startsNext
            paths = pathsNext

        return True

def Puzzazz(s):
    dict = open("mbsingle.txt")
    lss = LetterSquareSolver(s)
    words = lss.FindWords(dict, True)
    for word in words:
        if len(word) >= 5:
            print "%s (%d)" % (word, len(word))

def Boggle(s):
    dict = open("mbsingle.txt")
    lss = LetterSquareSolver(s)
    words = lss.FindWords(dict, False)
    for word in words:
        if len(word) >= 3:
            print "%s (%d)" % (word, len(word))

# --------------------------------------------------------------------
# Unit Tests
# --------------------------------------------------------------------
import unittest

class TestLSS(unittest.TestCase):
    def test_Errors(self):
        self.assertRaises(Exception, LetterSquareSolver, "")
        self.assertRaises(Exception, LetterSquareSolver, "xxx")

    def test_Basic(self):
        lss = LetterSquareSolver("fitrendpg")
        words = lss.FindWords(["finger", "printed"])
        self.assertEqual(2, len(words))

import sys, getopt, os

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hb:p:t")
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    if len(opts) == 0:
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == '-h':
            usage()
            sys.exit()
        if o == '-p':
            Puzzazz(a)
        if o == '-b':
            Boggle(a)
        if o == '-t':
            suite = unittest.TestLoader().loadTestsFromTestCase(TestLSS)
            unittest.TextTestRunner(verbosity=2).run(suite)

def usage():
    print "Usage: %s [-h | -b <letters> | -p <letters>]\n" % os.path.basename(sys.argv[0])
    print "Options\n"
    print "-h\t\t: help"
    print "-b <letters>\t: Boggle-style solutions"
    print "-p <letters>\t: Puzzazz-style solutions"
    print "-t\t\t: Run Unit tests"

if __name__ == "__main__":
    main()

